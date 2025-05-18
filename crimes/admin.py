from django.contrib import admin
from django.utils.html import format_html
from django.urls import path
from django.template.response import TemplateResponse
from django.db.models import Count, Q
from django.db.models.functions import TruncMonth
from django.utils import timezone
from datetime import timedelta
from .models import Crime, Evidence

class EvidenceInline(admin.TabularInline):
    model = Evidence
    extra = 1
    readonly_fields = ['file_preview']
    
    def file_preview(self, obj):
        if obj.file:
            if obj.file.url.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                return format_html('<img src="{}" style="max-height: 50px;"/>', obj.file.url)
            return format_html('<a href="{}">View File</a>', obj.file.url)
        return "No file"

@admin.register(Crime)
class CrimeAdmin(admin.ModelAdmin):
    list_display = ['title', 'crime_type', 'location', 'date_occurred', 'status', 'reported_by', 'priority_flag']
    list_filter = ['status', 'crime_type', 'date_occurred', 'priority']
    search_fields = ['title', 'description', 'location', 'reported_by__username']
    readonly_fields = ['created_at']  # removed reported_by from here
    inlines = [EvidenceInline]
    actions = ['mark_as_investigating', 'mark_as_resolved', 'mark_as_closed', 'set_high_priority']
    
    fieldsets = [
        ('Crime Information', {
            'fields': ['title', 'crime_type', 'description', 'location']
        }),
        ('Status & Priority', {
            'fields': ['status', 'priority'],
            'classes': ['collapse']
        }),
        ('Report Details', {
            'fields': ['reported_by', 'date_occurred', 'created_at'],
            'classes': ['collapse']
        }),
    ]

    def priority_flag(self, obj):
        priority_colors = {
            1: 'green',
            2: 'orange',
            3: 'red',
            4: 'darkred'
        }
        return format_html(
            '<span style="color: {};">⚠️ {}</span>',
            priority_colors.get(obj.priority, 'black'),
            obj.get_priority_display()
        )
    priority_flag.short_description = 'Priority'

    def mark_as_investigating(self, request, queryset):
        queryset.update(status='INVESTIGATING')
    mark_as_investigating.short_description = "Mark selected crimes as under investigation"

    def mark_as_resolved(self, request, queryset):
        queryset.update(status='RESOLVED')
    mark_as_resolved.short_description = "Mark selected crimes as resolved"

    def mark_as_closed(self, request, queryset):
        queryset.update(status='CLOSED')
    mark_as_closed.short_description = "Mark selected crimes as closed"

    def set_high_priority(self, request, queryset):
        queryset.update(priority=3)
    set_high_priority.short_description = "Set selected crimes as high priority"

    class Media:
        css = {
            'all': ('css/admin.css',)
        }

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('analytics/', self.admin_site.admin_view(self.admin_dashboard_view), name='crime_analytics'),
        ]
        return my_urls + urls

    def admin_dashboard_view(self, request):
        context = self.get_analytics_context(request)
        return TemplateResponse(
            request, 
            'admin/crimes/dashboard.html',  # Updated template path
            context
        )

    def _get_case_trend(self):
        now = timezone.now()
        month_ago = now - timedelta(days=30)
        current = Crime.objects.filter(created_at__gte=month_ago).count()
        previous = Crime.objects.filter(
            created_at__lt=month_ago,
            created_at__gte=month_ago - timedelta(days=30)
        ).count()
        if previous == 0:
            return 0
        return round(((current - previous) / previous) * 100, 1)

    def _get_resolution_rate(self):
        total = Crime.objects.count()
        if total == 0:
            return 0
        resolved = Crime.objects.filter(status='RESOLVED').count()
        return round((resolved / total) * 100, 1)

    def _get_priority_status(self):
        return dict(
            Crime.objects.filter(priority__gte=3)
            .values_list('status')
            .annotate(count=Count('id'))
        )

    def get_analytics_context(self, request):
        today = timezone.now()
        month_ago = today - timedelta(days=30)
        
        # Calculate statistics
        total_cases = Crime.objects.count()
        resolved_cases = Crime.objects.filter(status='RESOLVED').count()
        resolution_rate = (resolved_cases / total_cases * 100) if total_cases > 0 else 0
        
        # Get trends
        current_month_cases = Crime.objects.filter(created_at__gte=month_ago).count()
        previous_month_cases = Crime.objects.filter(
            created_at__lt=month_ago,
            created_at__gte=month_ago - timedelta(days=30)
        ).count()
        
        case_trend = (
            ((current_month_cases - previous_month_cases) / previous_month_cases * 100)
            if previous_month_cases > 0 else 0
        )
        
        return {
            'total_cases': total_cases,
            'resolution_rate': resolution_rate,
            'case_trend': case_trend,
            'high_priority_cases': Crime.objects.filter(priority__gte=3).count(),
            'priority_by_status': self.get_priority_status_counts(),
            'chart_data': {
                'crime_types': list(Crime.objects.values('crime_type')
                    .annotate(count=Count('id'))
                    .order_by('-count')),
                'monthly_trends': list(Crime.objects.filter(
                    created_at__gte=month_ago
                ).values('created_at__date')
                    .annotate(count=Count('id'))
                    .order_by('created_at__date'))
            }
        }

    def get_priority_status_counts(self):
        return dict(
            Crime.objects.filter(priority__gte=3)
            .values_list('status')
            .annotate(count=Count('id'))
        )

    def save_model(self, request, obj, form, change):
        if not change:  # if creating new object
            obj.reported_by = request.user
        super().save_model(request, obj, form, change)
