from django.contrib import admin
from .models import Report, ReportUpdate

class ReportUpdateInline(admin.TabularInline):
    model = ReportUpdate
    extra = 0

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'crime', 'reporter', 'status', 'assigned_officer', 'report_date')
    list_filter = ('status', 'priority', 'report_date')
    search_fields = ('crime__title', 'reporter__username', 'assigned_officer__username')
    inlines = [ReportUpdateInline]
