from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CheckIn
from .utils import generate_qr_code
from bookings.models import Booking

@login_required
def checkin_form(request, booking_id):
    """Form check-in untuk semua peserta"""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user, status='confirmed')
    
    if request.method == 'POST':
        participant_id = request.POST.get('participant_id')
        participant = booking.participants.get(id=participant_id)
        
        # Check if already checked in
        if CheckIn.objects.filter(booking=booking, participant=participant).exists():
            messages.warning(request, f'{participant.full_name} sudah check-in.')
            return redirect('checkins:form', booking_id=booking.id)
        
        # Create check-in
        checkin = CheckIn(
            booking=booking,
            participant=participant,
            id_card_photo=request.FILES.get('id_card_photo'),
            selfie_photo=request.FILES.get('selfie_photo')
        )
        checkin.save()
        
        # Generate QR code
        generate_qr_code(checkin)
        
        messages.success(request, f'Check-in {participant.full_name} berhasil! QR code telah digenerate.')
        return redirect('checkins:form', booking_id=booking.id)
    
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
        'participants_status': participants_status
    }
    return render(request, 'checkins/form.html', context)


@login_required
def checkin_success(request, checkin_id):
    """Halaman sukses check-in dengan QR code"""
    checkin = get_object_or_404(CheckIn, id=checkin_id, booking__user=request.user)
    return render(request, 'checkins/success.html', {'checkin': checkin})