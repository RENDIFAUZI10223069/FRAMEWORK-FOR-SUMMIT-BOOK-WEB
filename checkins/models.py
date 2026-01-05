from django.db import models
from django.conf import settings
from bookings.models import Booking, BookingParticipant

class CheckIn(models.Model):
    """Model untuk Check-in Pendaki"""
    
    STATUS_CHOICES = [
        ('pending', 'Menunggu Verifikasi'),
        ('verified', 'Terverifikasi'),
        ('rejected', 'Ditolak'),
    ]
    
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='checkins')
    participant = models.ForeignKey(BookingParticipant, on_delete=models.CASCADE, related_name='checkins')
    
    # Documents
    id_card_photo = models.ImageField(upload_to='checkins/id_cards/', verbose_name='Foto KTP')
    selfie_photo = models.ImageField(upload_to='checkins/selfies/', verbose_name='Foto Selfie', blank=True, null=True)
    
    # QR Code
    qr_code = models.ImageField(upload_to='checkins/qr_codes/', blank=True, null=True, verbose_name='QR Code')
    qr_data = models.CharField(max_length=200, blank=True, unique=True)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    verified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='verified_checkins')
    verified_at = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Check-in'
        verbose_name_plural = 'Check-ins'
        unique_together = ['booking', 'participant']
    
    def __str__(self):
        return f"Check-in: {self.participant.full_name} - {self.booking.booking_code}" 