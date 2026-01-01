from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('register/pendaki/', views.register_pendaki_view, name='register_pendaki'),
    path('register/admin/', views.register_admin_view, name='register_admin'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    
]