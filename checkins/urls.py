from django.urls import path
from . import views

app_name = 'checkins'

urlpatterns = [
    path('<int:booking_id>/form/', views.checkin_form, name='form'),
    path('<int:checkin_id>/success/', views.checkin_success, name='success'),
    path('<int:checkin_id>/download-qr/', views.checkin_download_qr, name='download-qr'),
    path('<int:booking_id>/group-status/', views.checkin_group_status, name='group-status'),
    path('scan/', views.scan_qr, name='scan'),
]