import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw
import uuid

def generate_qr_code(checkin):
    """Generate QR code untuk check-in"""
    # Generate unique QR data
    qr_data = f"CHECKIN-{checkin.booking.booking_code}-{checkin.participant.id_number}-{uuid.uuid4().hex[:8]}"
    
    # Create QR code
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(qr_data)
    qr.make(fit=True)
    
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