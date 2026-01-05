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
    
    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        related_name='checkins',
        verbose_name='Booking'
    )
    participant = models.ForeignKey(
        BookingParticipant,
        on_delete=models.CASCADE,
        related_name='checkins',
        verbose_name='Peserta'
    )
    
    # Documents
    id_card_photo = models.ImageField(
        upload_to='checkins/id_cards/',
        verbose_name='Foto KTP/Identitas'
    )
    selfie_photo = models.ImageField(
        upload_to='checkins/selfies/',
        blank=True,
        null=True,
        verbose_name='Foto Selfie dengan KTP'
    )
    
    # QR Code
    qr_code = models.ImageField(
        upload_to='checkins/qr_codes/',
        blank=True,
        null=True,
        verbose_name='QR Code'
    )
    qr_data = models.CharField(
        max_length=200,
        blank=True,
        unique=True,
        verbose_name='Data QR Code'
    )
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Status'
    )
    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='verified_checkins',
        verbose_name='Diverifikasi Oleh'
    )
    verified_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Waktu Verifikasi'
    )
    rejection_reason = models.TextField(
        blank=True,
        verbose_name='Alasan Penolakan'
    )
    
    # Notes
    notes = models.TextField(
        blank=True,
        verbose_name='Catatan'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Check-in'
        verbose_name_plural = 'Check-ins'
        unique_together = ['booking', 'participant']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Check-in: {self.participant.full_name} - {self.booking.booking_code}"
    
    def get_status_badge_class(self):
        badge_classes = {
            'pending': 'warning',
            'verified': 'success',
            'rejected': 'danger',
        }
        return badge_classes.get(self.status, 'secondary')