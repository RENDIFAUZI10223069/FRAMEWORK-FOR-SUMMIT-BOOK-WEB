from django.urls import path
from . import views

app_name = 'mountains'

urlpatterns = [
    path('', views.MountainListView.as_view(), name='list'),
    path('rinjani-senaru/', views.rinjani_senaru_detail, name='rinjani-senaru'),
    path('<slug:slug>/', views.MountainDetailView.as_view(), name='detail'),
    path('<slug:mountain_slug>/<slug:route_slug>/', views.RouteDetailView.as_view(), name='route-detail'),
]