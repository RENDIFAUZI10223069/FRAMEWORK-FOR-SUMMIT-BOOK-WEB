from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q, Sum
from bookings.models import Booking
from checkins.models import CheckIn
from datetime import date, timedelta

@login_required
def pendaki_dashboard(request):
    """Dashboard utama untuk pendaki"""
    user = request.user
    
    # Redirect if admin
    if user.role == 'admin':
        return redirect('dashboard:admin')
    
    # Statistics
    total_bookings = Booking.objects.filter(user=user).count()
    active_bookings = Booking.objects.filter(
        user=user,
        status='confirmed',
        start_date__gte=date.today()
    ).count()
    completed_bookings = Booking.objects.filter(
        user=user,
        status='completed'
    ).count()
    
    # Upcoming trip (most recent)
    upcoming_trip = Booking.objects.filter(
        user=user,
        status='confirmed',
        start_date__gte=date.today()
    ).select_related('route__mountain').order_by('start_date').first()
    
    # Recent bookings
    recent_bookings = Booking.objects.filter(
        user=user
    ).select_related('route__mountain').order_by('-created_at')[:5]
    
    # Check-in status for upcoming trip
    checkin_ready = False
    if upcoming_trip:
        # Check if H-1 or H-0
        days_until = (upcoming_trip.start_date - date.today()).days
        if days_until <= 1:
            checkin_ready = True
    
    context = {
        'total_bookings': total_bookings,
        'active_bookings': active_bookings,
        'completed_bookings': completed_bookings,
        'upcoming_trip': upcoming_trip,
        'recent_bookings': recent_bookings,
        'checkin_ready': checkin_ready,
        'page_title': 'Dashboard Pendaki'
    }
    return render(request, 'dashboard/pendaki/home.html', context)


@login_required
def pendaki_bookings(request):
    """List semua bookings pendaki dengan filter"""
    user = request.user
    
    if user.role == 'admin':
        return redirect('dashboard:admin')
    
    bookings = Booking.objects.filter(user=user).select_related('route__mountain').order_by('-created_at')
    
    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        bookings = bookings.filter(status=status_filter)
    
    # Filter by date range
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    if date_from:
        bookings = bookings.filter(start_date__gte=date_from)
    if date_to:
        bookings = bookings.filter(start_date__lte=date_to)
    
    context = {
        'bookings': bookings,
        'status_filter': status_filter,
        'date_from': date_from,
        'date_to': date_to,
        'page_title': 'Booking Saya'
    }
    return render(request, 'dashboard/pendaki/bookings.html', context)


@login_required
def pendaki_profile_edit(request):
    """Edit profil pendaki"""
    user = request.user
    
    if user.role == 'admin':
        return redirect('dashboard:admin')
    
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.phone_number = request.POST.get('phone_number')
        
        if request.FILES.get('profile_picture'):
            user.profile_picture = request.FILES.get('profile_picture')
        
        user.save()
        messages.success(request, 'Profil berhasil diupdate!')
        return redirect('dashboard:pendaki')
    
    context = {
        'page_title': 'Edit Profil'
    }
    return render(request, 'dashboard/pendaki/profile_edit.html', context)


@login_required
def pendaki_history(request):
    """Riwayat pendakian yang sudah selesai"""
    user = request.user
    
    if user.role == 'admin':
        return redirect('dashboard:admin')
    
    completed = Booking.objects.filter(
        user=user,
        status='completed'
    ).select_related('route__mountain').order_by('-start_date')
    
    # Statistics
    total_climbs = completed.count()
    total_participants = sum(b.num_participants for b in completed)
    
    context = {
        'completed_bookings': completed,
        'total_climbs': total_climbs,
        'total_participants': total_participants,
        'page_title': 'Riwayat Pendakian'
    }
    return render(request, 'dashboard/pendaki/history.html', context)
    