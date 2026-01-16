from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from mountains.models import Route
import uuid

class Booking(models.Model):
    """Model untuk Booking Pendakian"""
    
    STATUS_CHOICES = [
        ('pending', 'Menunggu Pembayaran'),
        ('paid', 'Sudah Dibayar'),
        ('confirmed', 'Dikonfirmasi'),
        ('cancelled', 'Dibatalkan'),
        ('completed', 'Selesai'),
    ]
    
    # Booking Info
    booking_code = models.CharField(max_length=20, unique=True, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    route = models.ForeignKey(Route, on_delete=models.PROTECT, related_name='bookings')
    
    # Schedule
    start_date = models.DateField(verbose_name='Tanggal Mulai Pendakian')
    end_date = models.DateField(verbose_name='Tanggal Selesai Pendakian')
    
    # Participants
    num_participants = models.IntegerField(
        verbose_name='Jumlah Peserta',
        validators=[MinValueValidator(1)]
    )
    
    # Pricing
    price_per_person = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Harga per Orang'
    )
    total_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name='Total Harga'
    )
    
    # Payment
    payment_method = models.CharField(
        max_length=50,
        choices=[
            ('transfer', 'Transfer Bank'),
            ('ewallet', 'E-Wallet'),
            ('credit_card', 'Kartu Kredit'),
        ],
        blank=True,
        null=True
    )
    payment_proof = models.ImageField(
        upload_to='bookings/payments/',
        blank=True,
        null=True,
        verbose_name='Bukti Pembayaran'
    )
    paid_at = models.DateTimeField(blank=True, null=True)
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    
    # Notes
    notes = models.TextField(blank=True, verbose_name='Catatan Tambahan')
    admin_notes = models.TextField(blank=True, verbose_name='Catatan Admin')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    confirmed_at = models.DateTimeField(blank=True, null=True)
    cancelled_at = models.DateTimeField(blank=True, null=True)
    cancellation_reason = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.booking_code} - {self.user.email}"
    
    def save(self, *args, **kwargs):
        if not self.booking_code:
            # Generate booking code: RNJ-YYYYMMDD-XXXX
            from datetime import date
            today = date.today().strftime('%Y%m%d')
            random_code = str(uuid.uuid4())[:4].upper()
            self.booking_code = f"RNJ-{today}-{random_code}"
        
        # Calculate total price
        self.total_price = self.price_per_person * self.num_participants
        
        super().save(*args, **kwargs)
    
    def get_status_badge_class(self):
        badge_classes = {
            'pending': 'warning',
            'paid': 'info',
            'confirmed': 'success',
            'cancelled': 'danger',
            'completed': 'secondary',
        }
        return badge_classes.get(self.status, 'secondary')


class BookingParticipant(models.Model):
    """Model untuk peserta pendakian"""
    
    GENDER_CHOICES = [
        ('male', 'Laki-laki'),
        ('female', 'Perempuan'),
    ]
    
    BLOOD_TYPE_CHOICES = [
        ('A', 'A'),
        ('B', 'B'),
        ('AB', 'AB'),
        ('O', 'O'),
    ]
    
    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        related_name='participants',
        verbose_name='Booking'
    )
    
    # Data Pribadi
    full_name = models.CharField(max_length=200, verbose_name='Nama Lengkap')
    id_number = models.CharField(max_length=50, verbose_name='NIK/No. Identitas')
    date_of_birth = models.DateField(verbose_name='Tanggal Lahir')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, verbose_name='Jenis Kelamin')
    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPE_CHOICES, verbose_name='Golongan Darah')
    phone_number = models.CharField(max_length=20, verbose_name='Nomor Telepon')
    email = models.EmailField(verbose_name='Email')
    
    # NEW: Alamat
    address = models.TextField(verbose_name='Alamat Lengkap', blank=True)
    city = models.CharField(max_length=100, verbose_name='Kota/Kabupaten', blank=True)
    province = models.CharField(max_length=100, verbose_name='Provinsi', blank=True)
    postal_code = models.CharField(max_length=10, verbose_name='Kode Pos', blank=True)
    
    # Kontak Darurat
    emergency_contact_name = models.CharField(max_length=200, verbose_name='Nama Kontak Darurat')
    emergency_contact_phone = models.CharField(max_length=20, verbose_name='Telepon Kontak Darurat')
    emergency_contact_relation = models.CharField(max_length=50, verbose_name='Hubungan')
    
    # Kesehatan
    health_notes = models.TextField(blank=True, verbose_name='Catatan Kesehatan')
    
    # NEW: Surat Keterangan Sehat
    health_certificate = models.FileField(
        upload_to='participants/health_certificates/',
        blank=True,
        null=True,
        verbose_name='Surat Keterangan Sehat'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Peserta Booking'
        verbose_name_plural = 'Peserta Booking'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.full_name} - {self.booking.booking_code}"
    
    @property
    def age(self):
        from datetime import date
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )