from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from .models import Booking, BookingParticipant
from .forms import BookingForm, BookingParticipantForm, PaymentForm
from mountains.models import Route

@login_required
def booking_create_step1(request):
    """Step 1: Pilih jadwal & jumlah peserta"""
    
    # Ambil parameter package dari URL
    package_type = request.GET.get('package', None)
    selected_route = None
    
    # Mapping package ke slug route
    package_mapping = {
        'hemat': 'paket-hemat-2h1m',
        'populer': 'jalur-senaru',
        'premium': 'paket-premium-4h3m'
    }
    
    # Cari route berdasarkan package yang dipilih
    if package_type and package_type in package_mapping:
        try:
            selected_route = Route.objects.get(slug=package_mapping[package_type], is_active=True)
        except Route.DoesNotExist:
            pass
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.price_per_person = booking.route.price_per_person
            
            # Calculate end date
            booking.end_date = booking.start_date + timedelta(days=booking.route.duration_days - 1)
            
            booking.save()
            
            messages.success(request, 'Booking berhasil dibuat. Silakan lengkapi data peserta.')
            return redirect('bookings:participants', booking_id=booking.id)
    else:
        # Pre-fill route jika ada package yang dipilih
        initial = {}
        if selected_route:
            initial['route'] = selected_route.id
        
        form = BookingForm(initial=initial)
    
    context = {
        'form': form,
        'routes': Route.objects.filter(is_active=True),
        'selected_route': selected_route,
        'page_title': 'Buat Booking Baru'
    }
    return render(request, 'bookings/create_step1.html', context)

@login_required
def booking_participants_step2(request, booking_id):
    """Step 2: Isi data peserta"""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    # Check if already has participants
    existing_count = booking.participants.count()
    
    if request.method == 'POST':
        form = BookingParticipantForm(request.POST)
        if form.is_valid():
            participant = form.save(commit=False)
            participant.booking = booking
            participant.save()
            
            current_count = booking.participants.count()
            
            if current_count < booking.num_participants:
                messages.success(request, f'Peserta {current_count} berhasil ditambahkan. Isi data peserta ke-{current_count + 1}.')
                return redirect('bookings:participants', booking_id=booking.id)
            else:
                messages.success(request, 'Semua data peserta sudah lengkap. Lanjut ke pembayaran.')
                return redirect('bookings:payment', booking_id=booking.id)
    else:
        form = BookingParticipantForm()
    
    context = {
        'booking': booking,
        'form': form,
        'current_count': existing_count + 1,
        'total_count': booking.num_participants,
        'existing_participants': booking.participants.all(),
        'page_title': f'Data Peserta {existing_count + 1} dari {booking.num_participants}'
    }
    return render(request, 'bookings/participants_step2.html', context)


@login_required
def booking_payment_step3(request, booking_id):
    """Step 3: Upload bukti pembayaran"""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    # Check if all participants are filled
    if booking.participants.count() < booking.num_participants:
        messages.warning(request, 'Lengkapi data peserta terlebih dahulu.')
        return redirect('bookings:participants', booking_id=booking.id)
    
    if request.method == 'POST':
        form = PaymentForm(request.POST, request.FILES, instance=booking)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.status = 'paid'
            booking.paid_at = timezone.now()
            booking.save()
            
            messages.success(request, 'Bukti pembayaran berhasil diupload. Menunggu konfirmasi admin.')
            return redirect('bookings:detail', booking_id=booking.id)
    else:
        form = PaymentForm(instance=booking)
    
    context = {
        'booking': booking,
        'form': form,
        'page_title': 'Pembayaran'
    }
    return render(request, 'bookings/payment_step3.html', context)


@login_required
def booking_detail(request, booking_id):
    """Detail booking"""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    context = {
        'booking': booking,
        'participants': booking.participants.all(),
        'page_title': f'Booking {booking.booking_code}'
    }
    return render(request, 'bookings/detail.html', context)


@login_required
def booking_list(request):
    """List semua booking user"""
    bookings = Booking.objects.filter(user=request.user).select_related('route__mountain')
    
    context = {
        'bookings': bookings,
        'page_title': 'Booking Saya'
    }
    return render(request, 'bookings/list.html', context)