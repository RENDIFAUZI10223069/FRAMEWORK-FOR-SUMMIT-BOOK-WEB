from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta

def home(request):
    """Landing page view"""
    context = {
        'current_date': timezone.now(),
    }
    return render(request, 'core/home.html', context)

def about(request):
    return render(request, 'core/about.html')

def contact(request):
    return render(request, 'core/contact.html')