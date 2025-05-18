from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.report_list, name='list'),
    path('<int:report_id>/', views.report_detail, name='report_detail'),
    path('<int:report_id>/status/', views.update_report_status, name='update_status'),
]
