from django.db import models
from accounts.models import CustomUser

class Crime(models.Model):
    CRIME_TYPES = [
        ('THEFT', 'Theft'),
        ('ASSAULT', 'Assault'),
        ('FRAUD', 'Fraud'),
        ('OTHER', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('INVESTIGATING', 'Under Investigation'),
        ('RESOLVED', 'Resolved'),
        ('CLOSED', 'Closed')
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    date_occurred = models.DateTimeField()
    crime_type = models.CharField(max_length=20, choices=CRIME_TYPES)
    reported_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    priority = models.IntegerField(
        default=1,
        choices=[
            (1, 'Low'),
            (2, 'Medium'),
            (3, 'High'),
            (4, 'Critical')
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True)

class Evidence(models.Model):
    crime = models.ForeignKey(Crime, on_delete=models.CASCADE)
    file = models.FileField(upload_to='evidence/')
    description = models.TextField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
