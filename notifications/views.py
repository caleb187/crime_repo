from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Notification

@login_required
def notification_list(request):
    notifications = Notification.objects.filter(
        recipient=request.user
    ).order_by('-created_at')
    return render(request, 'notifications/list.html', {
        'notifications': notifications
    })

@login_required
def mark_as_read(request, notification_id):
    notification = Notification.objects.get(
        id=notification_id, 
        recipient=request.user
    )
    notification.is_read = True
    notification.save()
    return redirect(notification.link or 'notifications:list')
