from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator

class Mountain(models.Model):
    """Model untuk Gunung"""
    name = models.CharField(max_length=200, verbose_name='Nama Gunung')
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField(verbose_name='Deskripsi')
    height = models.IntegerField(
        verbose_name='Ketinggian (mdpl)',
        validators=[MinValueValidator(0)]
    )
    location = models.CharField(max_length=200, verbose_name='Lokasi')
    province = models.CharField(max_length=100, verbose_name='Provinsi')
    difficulty_level = models.CharField(
        max_length=20,
        choices=[
            ('easy', 'Mudah'),
            ('medium', 'Menengah'),
            ('hard', 'Sulit'),
            ('extreme', 'Ekstrim'),
        ],
        default='medium',
        verbose_name='Tingkat Kesulitan'
    )
    image = models.ImageField(
        upload_to='mountains/',
        blank=True,
        null=True,
        verbose_name='Gambar Utama'
    )
    is_active = models.BooleanField(default=True, verbose_name='Aktif')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Mountain'
        verbose_name_plural = 'Mountains'
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.height} mdpl)"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('mountains:detail', kwargs={'slug': self.slug})


class Route(models.Model):
    """Model untuk Jalur Pendakian"""
    mountain = models.ForeignKey(
        Mountain,
        on_delete=models.CASCADE,
        related_name='routes',
        verbose_name='Gunung'
    )
    name = models.CharField(max_length=200, verbose_name='Nama Jalur')
    slug = models.SlugField(max_length=200, blank=True)
    description = models.TextField(verbose_name='Deskripsi Jalur')
    starting_point = models.CharField(max_length=200, verbose_name='Titik Awal')
    duration_days = models.IntegerField(
        verbose_name='Durasi (Hari)',
        validators=[MinValueValidator(1)]
    )
    duration_nights = models.IntegerField(
        verbose_name='Durasi (Malam)',
        validators=[MinValueValidator(0)]
    )
    distance_km = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name='Jarak (KM)',
        validators=[MinValueValidator(0)]
    )
    difficulty_level = models.CharField(
        max_length=20,
        choices=[
            ('easy', 'Mudah'),
            ('medium', 'Menengah'),
            ('hard', 'Sulit'),
            ('extreme', 'Ekstrim'),
        ],
        default='medium',
        verbose_name='Tingkat Kesulitan'
    )
    price_per_person = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Harga per Orang (Rp)'
    )
    max_participants = models.IntegerField(
        default=10,
        verbose_name='Maksimal Peserta',
        validators=[MinValueValidator(1)]
    )
    facilities = models.TextField(
        verbose_name='Fasilitas yang Disediakan',
        help_text='Pisahkan dengan enter untuk setiap item'
    )
    requirements = models.TextField(
        verbose_name='Persyaratan',
        help_text='Pisahkan dengan enter untuk setiap item'
    )
    gpx_file = models.FileField(
        upload_to='routes/gpx/',
        blank=True,
        null=True,
        verbose_name='File GPX'
    )
    is_active = models.BooleanField(default=True, verbose_name='Aktif')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Route'
        verbose_name_plural = 'Routes'
        ordering = ['mountain', 'name']
        unique_together = ['mountain', 'slug']
    
    def __str__(self):
        return f"{self.mountain.name} - {self.name}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_facilities_list(self):
        return [f.strip() for f in self.facilities.split('\n') if f.strip()]
    
    def get_requirements_list(self):
        return [r.strip() for r in self.requirements.split('\n') if r.strip()]
    
    def get_duration_text(self):
        return f"{self.duration_days} Hari {self.duration_nights} Malam"


class MountainGallery(models.Model):
    """Model untuk Galeri Foto Gunung"""
    mountain = models.ForeignKey(
        Mountain,
        on_delete=models.CASCADE,
        related_name='gallery',
        verbose_name='Gunung'
    )
    route = models.ForeignKey(
        Route,
        on_delete=models.CASCADE,
        related_name='gallery',
        blank=True,
        null=True,
        verbose_name='Jalur (Opsional)'
    )
    title = models.CharField(max_length=200, verbose_name='Judul Foto')
    image = models.ImageField(upload_to='mountains/gallery/', verbose_name='Foto')
    description = models.TextField(blank=True, verbose_name='Deskripsi')
    photographer = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Fotografer'
    )
    taken_date = models.DateField(blank=True, null=True, verbose_name='Tanggal Diambil')
    is_featured = models.BooleanField(default=False, verbose_name='Foto Unggulan')
    order = models.IntegerField(default=0, verbose_name='Urutan')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Mountain Gallery'
        verbose_name_plural = 'Mountain Galleries'
        ordering = ['mountain', 'order', '-created_at']
    
    def __str__(self):
        return f"{self.mountain.name} - {self.title}"