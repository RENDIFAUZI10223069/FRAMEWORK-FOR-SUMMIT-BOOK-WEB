from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('create/', views.booking_create_step1, name='create'),
    path('<int:booking_id>/participants/', views.booking_participants_step2, name='participants'),
    path('<int:booking_id>/payment/', views.booking_payment_step3, name='payment'),
    path('<int:booking_id>/', views.booking_detail, name='detail'),
    path('', views.booking_list, name='list'),
]