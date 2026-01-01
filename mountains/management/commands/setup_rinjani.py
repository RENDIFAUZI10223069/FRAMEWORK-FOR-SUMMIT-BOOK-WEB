from django.core.management.base import BaseCommand
from mountains.models import Mountain, Route

class Command(BaseCommand):
    help = 'Setup initial Rinjani data'
    
    def handle(self, *args, **kwargs):
        self.stdout.write('Setting up Rinjani data...')
        
        # Create Mountain
        mountain, created = Mountain.objects.get_or_create(
            slug='gunung-rinjani',
            defaults={
                'name': 'Gunung Rinjani',
                'description': 'Gunung Rinjani adalah gunung berapi tertinggi kedua di Indonesia dengan ketinggian 3.726 mdpl. Terletak di Pulau Lombok, Nusa Tenggara Barat.',
                'height': 3726,
                'location': 'Lombok Utara',
                'province': 'Nusa Tenggara Barat',
                'difficulty_level': 'hard',
                'is_active': True
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'✓ Mountain created: {mountain.name}'))
        else:
            self.stdout.write(self.style.WARNING(f'○ Mountain already exists: {mountain.name}'))
        
        # Create Senaru Route
        route, created = Route.objects.get_or_create(
            mountain=mountain,
            slug='jalur-senaru',
            defaults={
                'name': 'Jalur Senaru',
                'description': 'Jalur Senaru adalah rute paling populer untuk mendaki Gunung Rinjani dengan pemandangan Danau Segara Anak yang memukau. Jalur ini dimulai dari Desa Senaru, Lombok Utara.',
                'starting_point': 'Desa Senaru, Lombok Utara',
                'duration_days': 3,
                'duration_nights': 2,
                'distance_km': 22.5,
                'difficulty_level': 'medium',
                'price_per_person': 1800000,
                'max_participants': 10,
                'facilities': '''Pemandu lokal bersertifikat TNGL
Porter untuk membawa logistik grup
Tenda camping 4 season
Sleeping bag & matras
Makanan 3x sehari (sarapan, makan siang, makan malam)
Snack & air mineral
Perlengkapan masak lengkap
Izin masuk TNGL (Taman Nasional Gunung Rinjani)
P3K & oksigen portable
Sertifikat pendakian
Dokumentasi foto''',
                'requirements': '''Minimal umur 17 tahun
Kondisi fisik sehat dan bugar
Surat keterangan sehat dari dokter (untuk umur 50+)
KTP/Paspor asli dan fotokopi
Asuransi perjalanan (sangat disarankan)
Perlengkapan pribadi:
- Carrier/tas gunung 40-60L
- Jaket tebal/windproof
- Sepatu tracking/hiking
- Sleeping bag (jika punya)
- Headlamp/senter
- Pakaian ganti 2-3 set
- Kaus kaki tebal
- Sarung tangan
- Peralatan mandi secukupnya''',
                'is_active': True
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'✓ Route created: {route.name}'))
        else:
            self.stdout.write(self.style.WARNING(f'○ Route already exists: {route.name}'))
        
        self.stdout.write(self.style.SUCCESS('\n✓ Setup completed successfully!'))
        self.stdout.write(f'\nYou can now access:')
        self.stdout.write(f'- Admin: http://127.0.0.1:8000/admin/mountains/')
        self.stdout.write(f'- Detail: http://127.0.0.1:8000/mountains/rinjani-senaru/')