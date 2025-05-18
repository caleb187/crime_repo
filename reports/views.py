from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Report, ReportUpdate
from .forms import ReportUpdateForm
from notifications.models import Notification

@login_required
def report_detail(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    updates = report.reportupdate_set.all().order_by('-created_at')
    
    if request.method == 'POST':
        form = ReportUpdateForm(request.POST)
        if form.is_valid():
            update = form.save(commit=False)
            update.report = report
            update.updated_by = request.user
            update.save()
            
            # Create notification
            Notification.objects.create(
                recipient=report.reporter,
                title=f'Update on Report #{report.id}',
                message=update.update_text[:100],
                link=f'/reports/{report.id}/'
            )
            
            return redirect('report_detail', report_id=report.id)
    else:
        form = ReportUpdateForm()
        
    return render(request, 'reports/detail.html', {
        'report': report,
        'updates': updates,
        'form': form
    })

@login_required
def report_list(request):
    reports = Report.objects.filter(reporter=request.user).order_by('-report_date')
    return render(request, 'reports/list.html', {'reports': reports})

@login_required
def update_report_status(request, report_id):
    if not request.user.is_staff:
        return redirect('reports:report_list')
    
    report = get_object_or_404(Report, id=report_id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Report.STATUS_CHOICES):
            report.status = new_status
            report.save()
            
            Notification.objects.create(
                recipient=report.reporter,
                title=f'Status Update: Report #{report.id}',
                message=f'Your report status has been updated to {new_status}',
                link=f'/reports/{report.id}/'
            )
    return redirect('reports:report_detail', report_id=report.id)
