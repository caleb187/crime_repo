from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.db.models.functions import TruncMonth
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
import csv
import json
from .models import Crime, Evidence, CustomUser
from .forms import CrimeReportForm, EvidenceForm, CrimeAdminForm

@login_required
def crime_list(request):
    crimes = Crime.objects.filter(reported_by=request.user)
    return render(request, 'crimes/list.html', {'crimes': crimes})

@csrf_protect
@login_required
def crime_report(request):
    if request.method == 'POST':
        form = CrimeReportForm(request.POST)
        if form.is_valid():
            crime = form.save(commit=False)
            crime.reported_by = request.user
            crime.save()
            messages.success(request, 'Crime reported successfully')
            return redirect('crimes:crime_detail', pk=crime.pk)
    else:
        form = CrimeReportForm()
    return render(request, 'crimes/report.html', {'form': form})

@login_required
def crime_detail(request, pk):
    crime = get_object_or_404(Crime, pk=pk)
    evidence = Evidence.objects.filter(crime=crime)
    return render(request, 'crimes/detail.html', {
        'crime': crime,
        'evidence': evidence
    })

@csrf_protect
@login_required
def add_evidence(request, pk):
    crime = get_object_or_404(Crime, pk=pk)
    if request.method == 'POST':
        form = EvidenceForm(request.POST, request.FILES)
        if form.is_valid():
            evidence = form.save(commit=False)
            evidence.crime = crime
            evidence.save()
            messages.success(request, 'Evidence added successfully')
            return redirect('crimes:crime_detail', pk=pk)
    else:
        form = EvidenceForm()
    return render(request, 'crimes/evidence_form.html', {
        'form': form,
        'crime': crime
    })

@login_required
def dashboard(request):
    context = {
        'today': timezone.now(),
    }
    
    if request.user.is_staff:
        context.update({
            'total_crimes': Crime.objects.count(),
            'pending_count': Crime.objects.filter(status='PENDING').count(),
            'investigating_count': Crime.objects.filter(status='INVESTIGATING').count(),
            'resolved_count': Crime.objects.filter(status='RESOLVED').count(),
            'recent_crimes': Crime.objects.all().order_by('-created_at')[:5],
        })
    else:
        user_crimes = Crime.objects.filter(reported_by=request.user)
        context.update({
            'user_crimes_count': user_crimes.count(),
            'user_active_cases': user_crimes.exclude(status='CLOSED').count(),
            'user_recent_crimes': user_crimes.order_by('-created_at')[:5],
        })
    
    return render(request, 'crimes/dashboard.html', context)

@csrf_protect
@login_required
@user_passes_test(lambda u: u.is_staff)
def update_status(request, pk):
    crime = get_object_or_404(Crime, pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Crime.STATUS_CHOICES):
            crime.status = new_status
            crime.save()
            messages.success(request, f'Status updated to {new_status}')
    return redirect('crimes:crime_detail', pk=pk)

@user_passes_test(lambda u: u.is_staff)
def manage_cases(request):
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    
    cases = Crime.objects.all()
    if search_query:
        cases = cases.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    if status_filter:
        cases = cases.filter(status=status_filter)
    
    paginator = Paginator(cases.order_by('-created_at'), 10)
    page = request.GET.get('page', 1)
    
    return render(request, 'admin/crimes/manage_cases.html', {
        'cases': paginator.get_page(page),
        'status_choices': Crime.STATUS_CHOICES,
        'search_query': search_query,
        'status_filter': status_filter
    })

@user_passes_test(lambda u: u.is_staff)
def manage_users(request):
    search_query = request.GET.get('search', '')
    users = CustomUser.objects.all()
    
    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) |
            Q(email__icontains=search_query)
        )
    
    paginator = Paginator(users.order_by('-date_joined'), 10)
    page = request.GET.get('page', 1)
    
    return render(request, 'admin/crimes/manage_users.html', {
        'users': paginator.get_page(page),
        'search_query': search_query
    })

@user_passes_test(lambda u: u.is_staff)
def case_detail_admin(request, pk):
    case = get_object_or_404(Crime, pk=pk)
    if request.method == 'POST':
        form = CrimeAdminForm(request.POST, instance=case)
        if form.is_valid():
            form.save()
            messages.success(request, 'Case updated successfully')
            return redirect('crimes:manage_cases')
    else:
        form = CrimeAdminForm(instance=case)
    
    return render(request, 'admin/crimes/case_detail.html', {
        'case': case,
        'form': form,
        'evidence': case.evidence_set.all()
    })

@user_passes_test(lambda u: u.is_staff)
def case_map(request):
    # Get crimes from the last 30 days
    recent_crimes = Crime.objects.filter(
        date_occurred__gte=timezone.now() - timedelta(days=30)
    ).values('title', 'crime_type', 'status', 'date_occurred', 'location')
    
    # Convert the crimes data to JSON for the template
    crimes_json = []
    for crime in recent_crimes:
        # Here you'll need to extract latitude and longitude from your location field
        # This is an example - adjust according to how you store location data
        try:
            # Assuming location is stored as "lat,lng" string
            lat, lng = crime['location'].split(',')
            crimes_json.append({
                'title': crime['title'],
                'crime_type': crime['crime_type'],
                'status': crime['status'],
                'date_occurred': crime['date_occurred'].strftime('%Y-%m-%d'),
                'latitude': float(lat),
                'longitude': float(lng)
            })
        except (ValueError, AttributeError):
            continue

    return render(request, 'crimes/case_map.html', {
        'crimes_json': json.dumps(crimes_json)
    })

@user_passes_test(lambda u: u.is_staff)
def reports_export(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="crime_reports.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Title', 'Type', 'Location', 'Status', 'Date Reported'])
    
    crimes = Crime.objects.all().values_list('title', 'crime_type', 'location', 'status', 'created_at')
    for crime in crimes:
        writer.writerow(crime)
    
    return response

@user_passes_test(lambda u: u.is_staff)
def statistics(request):
    stats = {
        'by_type': Crime.objects.values('crime_type').annotate(count=Count('id')),
        'by_status': Crime.objects.values('status').annotate(count=Count('id')),
        'monthly': Crime.objects.annotate(month=TruncMonth('created_at')).values('month').annotate(count=Count('id'))
    }
    return render(request, 'crimes/statistics.html', stats)

def safety_tips(request):
    context = {
        'emergency_number': '911',
        'police_hotline': '###-###-####',  # Replace with actual number
        'last_updated': timezone.now().date(),
    }
    return render(request, 'crimes/safety_tips.html', context)

def emergency_contacts(request):
    context = {
        'emergency_numbers': {
            'police': '999',
            'toll_free': '0800199099',
            'counter_terrorism': '0800199699',
            'fire_brigade': '0800121222'
        }
    }
    return render(request, 'crimes/emergency_contacts.html', context)

@login_required
def profile(request):
    return render(request, 'crimes/profile.html', {
        'user': request.user,
        'reported_crimes': Crime.objects.filter(reported_by=request.user).order_by('-created_at')
    })
