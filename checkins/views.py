from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from bookings.models import Booking
from .models import CheckIn
from .forms import CheckInForm
from .utils import generate_qr_code, verify_qr_code

@login_required
def checkin_form(request, booking_id):
    """Form check-in untuk semua peserta dalam booking"""
    booking = get_object_or_404(
        Booking,
        id=booking_id,
        user=request.user,
        status='confirmed'
    )
    
    if request.method == 'POST':
        participant_id = request.POST.get('participant_id')
        
        if not participant_id:
            messages.error(request, 'Pilih peserta terlebih dahulu.')
            return redirect('checkins:form', booking_id=booking.id)
        
        participant = get_object_or_404(
            booking.participants,
            id=participant_id
        )
        
        # Check if already checked in
        if CheckIn.objects.filter(booking=booking, participant=participant).exists():
            messages.warning(request, f'{participant.full_name} sudah melakukan check-in.')
            return redirect('checkins:form', booking_id=booking.id)
        
        form = CheckInForm(request.POST, request.FILES)
        if form.is_valid():
            # Create check-in
            checkin = form.save(commit=False)
            checkin.booking = booking
            checkin.participant = participant
            checkin.save()
            
            # Generate QR code
            generate_qr_code(checkin)
            
            messages.success(
                request,
                f'Check-in {participant.full_name} berhasil! QR code telah digenerate.'
            )
            return redirect('checkins:success', checkin_id=checkin.id)
    else:
        form = CheckInForm()
    
    # Get participants and their check-in status
    participants_status = []
    for p in booking.participants.all():
        checkin = CheckIn.objects.filter(booking=booking, participant=p).first()
        participants_status.append({
            'participant': p,
            'checkin': checkin
        })
    
    context = {
        'booking': booking,
        'form': form,
        'participants_status': participants_status,
        'page_title': f'Check-in - {booking.booking_code}'
    }
    return render(request, 'checkins/form.html', context)


@login_required
def checkin_success(request, checkin_id):
    """Halaman sukses check-in dengan QR code"""
    checkin = get_object_or_404(
        CheckIn,
        id=checkin_id,
        booking__user=request.user
    )
    
    context = {
        'checkin': checkin,
        'page_title': 'Check-in Berhasil'
    }
    return render(request, 'checkins/success.html', context)


@login_required
def checkin_download_qr(request, checkin_id):
    """Download QR code sebagai file"""
    checkin = get_object_or_404(
        CheckIn,
        id=checkin_id,
        booking__user=request.user
    )
    
    if not checkin.qr_code:
        messages.error(request, 'QR Code belum digenerate.')
        return redirect('checkins:form', booking_id=checkin.booking.id)
    
    # Return file download
    response = HttpResponse(checkin.qr_code, content_type='image/png')
    response['Content-Disposition'] = f'attachment; filename="qr_{checkin.booking.booking_code}_{checkin.participant.full_name}.png"'
    return response


@login_required
def checkin_group_status(request, booking_id):
    """Status check-in untuk seluruh grup"""
    booking = get_object_or_404(
        Booking,
        id=booking_id,
        user=request.user
    )
    
    checkins = CheckIn.objects.filter(booking=booking).select_related('participant')
    
    # Statistics
    total_participants = booking.participants.count()
    total_checkins = checkins.count()
    verified_count = checkins.filter(status='verified').count()
    pending_count = checkins.filter(status='pending').count()
    rejected_count = checkins.filter(status='rejected').count()
    
    context = {
        'booking': booking,
        'checkins': checkins,
        'total_participants': total_participants,
        'total_checkins': total_checkins,
        'verified_count': verified_count,
        'pending_count': pending_count,
        'rejected_count': rejected_count,
        'progress_percentage': (total_checkins / total_participants * 100) if total_participants > 0 else 0,
        'page_title': f'Status Check-in Grup'
    }
    return render(request, 'checkins/group_status.html', context)


def scan_qr(request):
    """Scan QR code (untuk admin/petugas)"""
    if request.method == 'POST':
        qr_data = request.POST.get('qr_data')
        
        if not qr_data:
            return render(request, 'checkins/scan.html', {
                'error': 'QR Code tidak terbaca'
            })
        
        result = verify_qr_code(qr_data)
        
        return render(request, 'checkins/scan.html', {
            'result': result
        })
    
    return render(request, 'checkins/scan.html')