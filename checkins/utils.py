import qrcode
from io import BytesIO
from django.core.files import File
import uuid

def generate_qr_code(checkin):
    """
    Generate QR code untuk check-in
    Format: CHECKIN-{booking_code}-{nik}-{unique_id}
    """
    # Generate unique QR data
    unique_id = uuid.uuid4().hex[:8].upper()
    qr_data = f"CHECKIN-{checkin.booking.booking_code}-{checkin.participant.id_number}-{unique_id}"
    
    # Create QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)
    
    # Create image
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Save to BytesIO
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    
    # Save to model
    filename = f'qr_{checkin.booking.booking_code}_{checkin.participant.id}.png'
    checkin.qr_code.save(filename, File(buffer), save=False)
    checkin.qr_data = qr_data
    checkin.save()
    
    return qr_data


def verify_qr_code(qr_data):
    """
    Verify QR code dan return CheckIn object
    """
    from .models import CheckIn
    
    try:
        checkin = CheckIn.objects.get(qr_data=qr_data)
        return {
            'valid': True,
            'checkin': checkin,
            'participant': checkin.participant,
            'booking': checkin.booking
        }
    except CheckIn.DoesNotExist:
        return {
            'valid': False,
            'error': 'QR Code tidak valid atau tidak ditemukan'
        }