from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

class User(AbstractUser):
    """Custom User Model dengan Role"""
    
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('pendaki', 'Pendaki'),
    ]
    
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='pendaki',
        verbose_name='Role'
    )
    
    email = models.EmailField(unique=True, verbose_name='Email')
    
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Format: '+999999999'. Maksimal 15 digit."
    )
    phone_number = models.CharField(
        validators=[phone_regex], 
        max_length=17, 
        blank=True,
        verbose_name='Nomor Telepon'
    )
    
    date_of_birth = models.DateField(
        null=True, 
        blank=True,
        verbose_name='Tanggal Lahir'
    )
    
    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        null=True,
        blank=True,
        verbose_name='Foto Profil'
    )
    
    # Khusus untuk Admin
    admin_code = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Kode Admin'
    )
    
    position = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Jabatan'
    )
    
    # Khusus untuk Pendaki
    emergency_contact_name = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='Nama Kontak Darurat'
    )
    
    emergency_contact_phone = models.CharField(
        max_length=17,
        blank=True,
        null=True,
        verbose_name='Telepon Kontak Darurat'
    )
    
    blood_type = models.CharField(
        max_length=5,
        blank=True,
        null=True,
        choices=[
            ('A', 'A'),
            ('B', 'B'),
            ('AB', 'AB'),
            ('O', 'O'),
        ],
        verbose_name='Golongan Darah'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.username
    
    @property
    def is_admin_role(self):
        return self.role == 'admin'
    
    @property
    def is_pendaki_role(self):
        return self.role == 'pendaki'
    
    @property
    def age(self):
        if self.date_of_birth:
            from datetime import date
            today = date.today()
            return today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
        return None