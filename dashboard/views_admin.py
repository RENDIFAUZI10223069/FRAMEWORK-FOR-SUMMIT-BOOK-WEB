from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Sum, Count, Q
from django.utils import timezone
from bookings.models import Booking
from checkins.models import CheckIn
from mountains.models import Route
from datetime import date, timedelta

def is_admin(user):
    return user.is_authenticated and user.role == 'admin'

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    """Dashboard utama untuk admin"""
    
    # Date ranges
    today = date.today()
    this_month = today.replace(day=1)
    last_month = (this_month - timedelta(days=1)).replace(day=1)
    
    # Statistics - This Month
    total_bookings_month = Booking.objects.filter(
        created_at__gte=this_month
    ).count()
    
    confirmed_bookings = Booking.objects.filter(
        status='confirmed'
    ).count()
    
    pending_payments = Booking.objects.filter(
        status='paid'
    ).count()
    
    total_revenue_month = Booking.objects.filter(
        status__in=['confirmed', 'completed'],
        created_at__gte=this_month
    ).aggregate(total=Sum('total_price'))['total'] or 0
    
    # Pending check-ins
    pending_checkins = CheckIn.objects.filter(status='pending').count()
    
    # Recent bookings
    recent_bookings = Booking.objects.select_related(
        'user',
        'route__mountain'
    ).order_by('-created_at')[:10]
    
    # Upcoming climbs (next 7 days)
    upcoming_climbs = Booking.objects.filter(
        status='confirmed',
        start_date__gte=today,
        start_date__lte=today + timedelta(days=7)
    ).select_related('user', 'route__mountain').order_by('start_date')
    
    # Popular routes
    popular_routes = Route.objects.annotate(
        booking_count=Count('bookings')
    ).order_by('-booking_count')[:5]
    
    context = {
        'total_bookings_month': total_bookings_month,
        'confirmed_bookings': confirmed_bookings,
        'pending_payments': pending_payments,
        'total_revenue_month': total_revenue_month,
        'pending_checkins': pending_checkins,
        'recent_bookings': recent_bookings,
        'upcoming_climbs': upcoming_climbs,
        'popular_routes': popular_routes,
        'page_title': 'Dashboard Admin'
    }
    return render(request, 'dashboard/admin/home.html', context)


@login_required
@user_passes_test(is_admin)
def admin_manage_bookings(request):
    """Kelola semua booking"""
    
    bookings = Booking.objects.select_related(
        'user',
        'route__mountain'
    ).order_by('-created_at')
    
    # Filters
    status = request.GET.get('status')
    if status:
        bookings = bookings.filter(status=status)
    
    search = request.GET.get('search')
    if search:
        bookings = bookings.filter(
            Q(booking_code__icontains=search) |
            Q(user__email__icontains=search) |
            Q(user__first_name__icontains=search) |
            Q(user__last_name__icontains=search)
        )
    
    date_from = request.GET.get('date_from')
    if date_from:
        bookings = bookings.filter(start_date__gte=date_from)
    
    date_to = request.GET.get('date_to')
    if date_to:
        bookings = bookings.filter(start_date__lte=date_to)
    
    context = {
        'bookings': bookings,
        'status': status,
        'search': search,
        'date_from': date_from,
        'date_to': date_to,
        'page_title': 'Kelola Booking'
    }
    return render(request, 'dashboard/admin/manage_bookings.html', context)


@login_required
@user_passes_test(is_admin)
def admin_verify_booking(request, booking_id):
    """Verifikasi pembayaran booking"""
    
    booking = get_object_or_404(Booking, id=booking_id)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'confirm':
            booking.status = 'confirmed'
            booking.confirmed_at = timezone.now()
            booking.save()
            messages.success(
                request,
                f'Booking {booking.booking_code} berhasil dikonfirmasi!'
            )
        
        elif action == 'reject':
            booking.status = 'cancelled'
            booking.cancelled_at = timezone.now()
            booking.cancellation_reason = request.POST.get('reason', 'Pembayaran tidak valid')
            booking.save()
            messages.warning(
                request,
                f'Booking {booking.booking_code} ditolak.'
            )
        
        return redirect('dashboard:admin-bookings')
    
    context = {
        'booking': booking,
        'page_title': 'Verifikasi Booking'
    }
    return render(request, 'dashboard/admin/verify_booking.html', context)


@login_required
@user_passes_test(is_admin)
def admin_checkins(request):
    """List semua check-in yang perlu verifikasi"""
    
    # Get all checkins with related data
    checkins = CheckIn.objects.select_related(
        'booking',
        'participant',
        'booking__route__mountain',
        'booking__user'
    ).order_by('-created_at')
    
    # Apply status filter (default: pending)
    status = request.GET.get('status', 'pending')
    if status:
        checkins = checkins.filter(status=status)
    
    # Apply search filter
    search = request.GET.get('search')
    if search:
        checkins = checkins.filter(
            Q(participant__full_name__icontains=search) |
            Q(participant__id_number__icontains=search) |
            Q(booking__booking_code__icontains=search) |
            Q(qr_data__icontains=search)
        )
    
    # Calculate statistics for all statuses
    total_pending = CheckIn.objects.filter(status='pending').count()
    total_verified = CheckIn.objects.filter(status='verified').count()
    total_rejected = CheckIn.objects.filter(status='rejected').count()
    
    context = {
        'checkins': checkins,
        'status': status,
        'search': search,
        'total_pending': total_pending,
        'total_verified': total_verified,
        'total_rejected': total_rejected,
        'page_title': 'Verifikasi Check-in'
    }
    return render(request, 'dashboard/admin/checkins.html', context)


@login_required
@user_passes_test(is_admin)
def admin_verify_checkin(request, checkin_id):
    """Verifikasi check-in pendaki"""
    
    # Get checkin with all related data
    checkin = get_object_or_404(
        CheckIn.objects.select_related(
            'booking',
            'participant',
            'booking__route__mountain',
            'booking__user',
            'verified_by'
        ),
        id=checkin_id
    )
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'verify':
            checkin.status = 'verified'
            checkin.verified_by = request.user
            checkin.verified_at = timezone.now()
            checkin.save()
            messages.success(
                request,
                f'Check-in {checkin.participant.full_name} berhasil diverifikasi!'
            )
        
        elif action == 'reject':
            checkin.status = 'rejected'
            checkin.rejection_reason = request.POST.get('reason', 'Dokumen tidak sesuai')
            checkin.save()
            messages.warning(
                request,
                f'Check-in {checkin.participant.full_name} ditolak.'
            )
        
        return redirect('dashboard:admin-checkins')
    
    context = {
        'checkin': checkin,
        'page_title': 'Verifikasi Check-in'
    }
    return render(request, 'dashboard/admin/verify_checkin.html', context)


@login_required
@user_passes_test(is_admin)
def admin_reports(request):
    """Laporan & statistik"""
    from django.db.models.functions import TruncMonth
    from datetime import datetime
    
    # Monthly revenue data (current year)
    monthly_data = Booking.objects.filter(
        status__in=['confirmed', 'completed'],
        created_at__year=datetime.now().year
    ).annotate(
        month=TruncMonth('created_at')
    ).values('month').annotate(
        total=Sum('total_price'),
        count=Count('id')
    ).order_by('month')
    
    # Top routes
    top_routes = Route.objects.annotate(
        booking_count=Count('bookings'),
        total_revenue=Sum('bookings__total_price')
    ).order_by('-booking_count')[:10]
    
    # Statistics by status
    status_stats = Booking.objects.values('status').annotate(
        count=Count('id'),
        total=Sum('total_price')
    ).order_by('-count')
    
    context = {
        'monthly_data': monthly_data,
        'top_routes': top_routes,
        'status_stats': status_stats,
        'page_title': 'Laporan & Statistik'
    }
    return render(request, 'dashboard/admin/reports.html', context)