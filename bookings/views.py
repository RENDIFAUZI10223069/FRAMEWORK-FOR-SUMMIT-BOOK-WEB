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
            selected_route = Route.objects.get(
                slug=package_mapping[package_type], 
                is_active=True
            )
        except Route.DoesNotExist:
            messages.warning(request, 'Paket yang dipilih tidak tersedia.')
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.price_per_person = booking.route.price_per_person
            
            # Calculate end date based on route duration
            booking.end_date = booking.start_date + timedelta(
                days=booking.route.duration_days - 1
            )
            
            booking.save()
            
            messages.success(
                request, 
                'Booking berhasil dibuat. Silakan lengkapi data peserta.'
            )
            return redirect('bookings:participants', booking_id=booking.id)
        else:
            messages.error(
                request, 
                'Terjadi kesalahan. Periksa kembali data yang Anda masukkan.'
            )
    else:
        # Pre-fill route jika ada package yang dipilih
        initial = {}
        if selected_route:
            initial['route'] = selected_route.id
        
        form = BookingForm(initial=initial)
    
    context = {
        'form': form,
        'routes': Route.objects.filter(is_active=True).select_related('mountain'),
        'selected_route': selected_route,
        'page_title': 'Buat Booking Baru'
    }
    return render(request, 'bookings/create_step1.html', context)


@login_required
def booking_participants_step2(request, booking_id):
    """Step 2: Isi data peserta"""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    # Cek apakah booking masih pending
    if booking.status not in ['pending', 'paid']:
        messages.warning(request, 'Booking ini sudah tidak dapat diubah.')
        return redirect('bookings:detail', booking_id=booking.id)
    
    # Check if already has participants
    existing_count = booking.participants.count()
    
    # Redirect ke payment jika semua peserta sudah lengkap
    if existing_count >= booking.num_participants:
        messages.info(request, 'Semua data peserta sudah lengkap.')
        return redirect('bookings:payment', booking_id=booking.id)
    
    if request.method == 'POST':
        form = BookingParticipantForm(request.POST, request.FILES)
        if form.is_valid():
            participant = form.save(commit=False)
            participant.booking = booking
            participant.save()
            
            current_count = booking.participants.count()
            
            if current_count < booking.num_participants:
                messages.success(
                    request, 
                    f'Peserta {current_count} berhasil ditambahkan. '
                    f'Silakan isi data peserta ke-{current_count + 1}.'
                )
                return redirect('bookings:participants', booking_id=booking.id)
            else:
                messages.success(
                    request, 
                    'Semua data peserta sudah lengkap. Lanjut ke pembayaran.'
                )
                return redirect('bookings:payment', booking_id=booking.id)
        else:
            messages.error(
                request, 
                'Terjadi kesalahan. Periksa kembali data yang Anda masukkan.'
            )
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
    
    # Cek apakah sudah dibayar
    if booking.status in ['paid', 'confirmed', 'completed']:
        messages.info(request, 'Booking ini sudah dibayar.')
        return redirect('bookings:detail', booking_id=booking.id)
    
    if request.method == 'POST':
        form = PaymentForm(request.POST, request.FILES, instance=booking)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.status = 'paid'
            booking.paid_at = timezone.now()
            booking.save()
            
            messages.success(
                request, 
                'Bukti pembayaran berhasil diupload. Menunggu konfirmasi admin.'
            )
            return redirect('bookings:detail', booking_id=booking.id)
        else:
            messages.error(
                request, 
                'Terjadi kesalahan saat upload bukti pembayaran.'
            )
    else:
        form = PaymentForm(instance=booking)
    
    context = {
        'booking': booking,
        'form': form,
        'page_title': 'Pembayaran',
        'total_price': booking.total_price,
        'participants': booking.participants.all()
    }
    return render(request, 'bookings/payment_step3.html', context)


@login_required
def booking_detail(request, booking_id):
    """Detail booking"""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    context = {
        'booking': booking,
        'participants': booking.participants.all(),
        'page_title': f'Booking {booking.booking_code}',
        'can_edit': booking.status == 'pending',
        'can_cancel': booking.status in ['pending', 'paid']
    }
    return render(request, 'bookings/detail.html', context)


@login_required
def booking_list(request):
    """List semua booking user"""
    bookings = Booking.objects.filter(
        user=request.user
    ).select_related('route__mountain').prefetch_related('participants')
    
    # Filter berdasarkan status jika ada
    status_filter = request.GET.get('status')
    if status_filter and status_filter != 'all':
        bookings = bookings.filter(status=status_filter)
    
    context = {
        'bookings': bookings,
        'page_title': 'Booking Saya',
        'status_filter': status_filter or 'all',
        'status_choices': Booking.STATUS_CHOICES
    }
    return render(request, 'bookings/list.html', context)


@login_required
def booking_cancel(request, booking_id):
    """Batalkan booking"""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    # Hanya bisa cancel jika status pending atau paid
    if booking.status not in ['pending', 'paid']:
        messages.error(request, 'Booking ini tidak dapat dibatalkan.')
        return redirect('bookings:detail', booking_id=booking.id)
    
    if request.method == 'POST':
        cancellation_reason = request.POST.get('cancellation_reason', '')
        booking.status = 'cancelled'
        booking.cancelled_at = timezone.now()
        booking.cancellation_reason = cancellation_reason
        booking.save()
        
        messages.success(request, 'Booking berhasil dibatalkan.')
        return redirect('bookings:detail', booking_id=booking.id)
    
    context = {
        'booking': booking,
        'page_title': 'Batalkan Booking'
    }
    return render(request, 'bookings/cancel_confirm.html', context)


@login_required
def participant_edit(request, participant_id):
    """Edit data peserta"""
    participant = get_object_or_404(BookingParticipant, id=participant_id)
    booking = participant.booking
    
    # Pastikan user adalah pemilik booking
    if booking.user != request.user:
        messages.error(request, 'Anda tidak memiliki akses ke halaman ini.')
        return redirect('bookings:list')
    
    # Hanya bisa edit jika booking masih pending atau paid
    if booking.status not in ['pending', 'paid']:
        messages.warning(request, 'Data peserta tidak dapat diubah.')
        return redirect('bookings:detail', booking_id=booking.id)
    
    if request.method == 'POST':
        form = BookingParticipantForm(request.POST, request.FILES, instance=participant)
        if form.is_valid():
            form.save()
            messages.success(request, 'Data peserta berhasil diperbarui.')
            return redirect('bookings:detail', booking_id=booking.id)
        else:
            messages.error(request, 'Terjadi kesalahan saat memperbarui data.')
    else:
        form = BookingParticipantForm(instance=participant)
    
    context = {
        'form': form,
        'participant': participant,
        'booking': booking,
        'page_title': f'Edit Data Peserta - {participant.full_name}'
    }
    return render(request, 'bookings/participant_edit.html', context)


@login_required
def participant_delete(request, participant_id):
    """Hapus data peserta"""
    participant = get_object_or_404(BookingParticipant, id=participant_id)
    booking = participant.booking
    
    # Pastikan user adalah pemilik booking
    if booking.user != request.user:
        messages.error(request, 'Anda tidak memiliki akses ke halaman ini.')
        return redirect('bookings:list')
    
    # Hanya bisa hapus jika booking masih pending
    if booking.status != 'pending':
        messages.warning(request, 'Data peserta tidak dapat dihapus.')
        return redirect('bookings:detail', booking_id=booking.id)
    
    # Tidak bisa hapus jika hanya tersisa 1 peserta
    if booking.participants.count() <= 1:
        messages.warning(request, 'Minimal harus ada 1 peserta.')
        return redirect('bookings:detail', booking_id=booking.id)
    
    if request.method == 'POST':
        participant_name = participant.full_name
        participant.delete()
        
        # Update jumlah peserta di booking
        booking.num_participants = booking.participants.count()
        booking.save()
        
        messages.success(request, f'Data peserta {participant_name} berhasil dihapus.')
        return redirect('bookings:detail', booking_id=booking.id)
    
    context = {
        'participant': participant,
        'booking': booking,
        'page_title': 'Hapus Peserta'
    }
    return render(request, 'bookings/participant_delete_confirm.html', context)