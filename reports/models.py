from django.db import models
from accounts.models import CustomUser
from crimes.models import Crime

class Report(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('INVESTIGATING', 'Under Investigation'),
        ('RESOLVED', 'Resolved'),
        ('CLOSED', 'Case Closed')
    ]
    
    crime = models.ForeignKey(Crime, on_delete=models.CASCADE)
    reporter = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    assigned_officer = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='assigned_reports')
    report_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    priority = models.IntegerField(default=0)

class ReportUpdate(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    update_text = models.TextField()
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
