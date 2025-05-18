from django.urls import path
from . import views

app_name = 'crimes'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),  # Add dashboard URL
    path('', views.crime_list, name='crime_list'),
    path('report/', views.crime_report, name='crime_report'),
    path('<int:pk>/', views.crime_detail, name='crime_detail'),
    path('<int:pk>/evidence/add/', views.add_evidence, name='add_evidence'),
    path('<int:pk>/update-status/', views.update_status, name='update_status'),
    path('manage/cases/', views.manage_cases, name='manage_cases'),
    path('manage/users/', views.manage_users, name='manage_users'),
    path('manage/case/<int:pk>/', views.case_detail_admin, name='case_detail_admin'),
    path('map/', views.case_map, name='case_map'),
    path('reports/export/', views.reports_export, name='reports_export'),
    path('statistics/', views.statistics, name='statistics'),
    path('safety-tips/', views.safety_tips, name='safety_tips'),
    path('emergency-contacts/', views.emergency_contacts, name='emergency_contacts'),
    path('profile/', views.profile, name='profile'),
]
