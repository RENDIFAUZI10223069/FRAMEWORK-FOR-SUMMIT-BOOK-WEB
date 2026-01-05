from django.urls import path
from . import views_pendaki, views_admin

app_name = 'dashboard'

urlpatterns = [
    # Pendaki URLs
    path('pendaki/', views_pendaki.pendaki_dashboard, name='pendaki'),
    path('pendaki/bookings/', views_pendaki.pendaki_bookings, name='pendaki-bookings'),
    path('pendaki/history/', views_pendaki.pendaki_history, name='pendaki-history'),
    path('pendaki/profile/edit/', views_pendaki.pendaki_profile_edit, name='pendaki-profile-edit'),
    
    # Admin URLs
    path('admin/', views_admin.admin_dashboard, name='admin'),
    path('admin/bookings/', views_admin.admin_manage_bookings, name='admin-bookings'),
    path('admin/bookings/<int:booking_id>/verify/', views_admin.admin_verify_booking, name='admin-verify-booking'),
    path('admin/checkins/', views_admin.admin_checkins, name='admin-checkins'),
    path('admin/checkins/<int:checkin_id>/verify/', views_admin.admin_verify_checkin, name='admin-verify-checkin'),
    path('admin/reports/', views_admin.admin_reports, name='admin-reports'),
]