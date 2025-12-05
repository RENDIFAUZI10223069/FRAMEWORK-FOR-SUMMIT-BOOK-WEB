# 🏔️ Summit Book

**Sistem Booking Pendakian Gunung Berbasis Web**

Summit Book adalah aplikasi web modern untuk manajemen pemesanan pendakian gunung yang dibangun dengan Django, MySQL, dan Bootstrap 5. Dirancang khusus untuk mengelola pendakian seperti Gunung Rinjani dengan fitur booking online, check-in digital, dan dashboard monitoring.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-6.0-green.svg)](https://www.djangoproject.com/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple.svg)](https://getbootstrap.com/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0+-orange.svg)](https://www.mysql.com/)

---

## ✨ Fitur Utama

- 🎫 **Sistem Booking Online** - Pemesanan pendakian dengan validasi kuota
- 👥 **Manajemen User** - Multi-role (Admin, Operator, Pendaki)
- 📊 **Dashboard Analytics** - Statistik real-time pendakian
- ✅ **Check-in Digital** - QR Code scanning untuk verifikasi
- 🏔️ **Multi-Mountain** - Mendukung berbagai gunung dan jalur
- 💳 **Payment Tracking** - Monitor status pembayaran
- 📱 **Responsive Design** - Mobile-friendly interface

---

## 📋 Daftar Isi

- [Prasyarat](#-prasyarat)
- [Instalasi](#-instalasi)
- [Konfigurasi Database](#-konfigurasi-database)
- [Setup Environment](#-setup-environment)
- [Menjalankan Aplikasi](#-menjalankan-aplikasi)
- [Struktur Project](#-struktur-project)
- [Testing](#-testing)
- [Deployment](#-deployment)
- [Troubleshooting](#-troubleshooting)
- [Kontribusi](#-kontribusi)

---

## 🔧 Prasyarat

Pastikan sistem Anda telah memiliki:

| Requirement | Versi Minimum | Cek Versi |
|------------|---------------|-----------|
| Python | 3.8+ | `python --version` |
| pip | Latest | `pip --version` |
| MySQL | 8.0+ | `mysql --version` |
| Git | Latest | `git --version` |

---

## 🚀 Instalasi

### 1. Clone Repository

```bash
git clone https://github.com/username/summit-book.git
cd summit-book
```

### 2. Buat Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**Atau install manual:**

```bash
pip install django==4.2.7
pip install mysqlclient
pip install django-bootstrap5
pip install Pillow
pip install django-crispy-forms crispy-bootstrap5
pip install python-decouple
pip install qrcode[pil]
pip install django-widget-tweaks
```

---

## 🗄️ Konfigurasi Database

### 1. Buat Database MySQL

Login ke MySQL dan jalankan:

```sql
CREATE DATABASE summit_book CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE USER 'summitbook_user'@'localhost' IDENTIFIED BY 'your_secure_password';

GRANT ALL PRIVILEGES ON summit_book.* TO 'summitbook_user'@'localhost';

FLUSH PRIVILEGES;
```

### 2. Verifikasi Koneksi

```bash
mysql -u summitbook_user -p summit_book
```

---

## ⚙️ Setup Environment

### 1. Buat File `.env`

Copy template environment:

```bash
cp .env.example .env
```

### 2. Konfigurasi `.env`

Edit file `.env` dengan editor favorit:

```env
# Django Settings
SECRET_KEY=your-generated-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration
DB_NAME=summit_book
DB_USER=summitbook_user
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=3306

# Email Configuration (Optional)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### 3. Generate Secret Key

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy output ke `SECRET_KEY` di file `.env`.

---

## 🎯 Menjalankan Aplikasi

### 1. Migrasi Database

```bash
# Cek konfigurasi
python manage.py check

# Buat file migrasi
python manage.py makemigrations

# Terapkan migrasi
python manage.py migrate
```

### 2. Buat Superuser

```bash
python manage.py createsuperuser
```

Ikuti prompt untuk membuat admin account.

### 3. Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### 4. Jalankan Development Server

```bash
python manage.py runserver
```

### 5. Akses Aplikasi

- **Web App:** http://127.0.0.1:8000/
- **Admin Panel:** http://127.0.0.1:8000/admin/
- **API Docs:** http://127.0.0.1:8000/api/docs/

---

## 📁 Struktur Project

```
summit-book/
├── 📁 summit_book_project/    # Konfigurasi utama Django
│   ├── settings.py            # Settings & konfigurasi
│   ├── urls.py                # Routing utama
│   └── wsgi.py                # WSGI configuration
│
├── 📁 accounts/               # Manajemen user & autentikasi
│   ├── models.py              # User models
│   ├── views.py               # Login, register, profile
│   └── forms.py               # Form autentikasi
│
├── 📁 mountains/              # Data gunung & jalur
│   ├── models.py              # Mountain, Trail models
│   ├── views.py               # CRUD gunung
│   └── admin.py               # Admin interface
│
├── 📁 bookings/               # Sistem booking
│   ├── models.py              # Booking model
│   ├── views.py               # Create, update booking
│   ├── forms.py               # Booking form
│   └── utils.py               # Helper functions
│
├── 📁 checkins/               # Check-in digital
│   ├── models.py              # Check-in records
│   ├── views.py               # QR scanning
│   └── qr_generator.py        # QR code generation
│
├── 📁 dashboard/              # Analytics & monitoring
│   ├── views.py               # Dashboard views
│   └── charts.py              # Data visualization
│
├── 📁 core/                   # Shared utilities
│   ├── middleware.py          # Custom middleware
│   ├── decorators.py          # Custom decorators
│   └── validators.py          # Custom validators
│
├── 📁 static/                 # Static files (CSS, JS, Images)
│   ├── css/
│   ├── js/
│   └── images/
│
├── 📁 media/                  # User uploads
│   ├── profiles/
│   └── mountains/
│
├── 📁 templates/              # HTML templates
│   ├── base.html              # Base template
│   ├── accounts/
│   ├── mountains/
│   ├── bookings/
│   └── dashboard/
│
├── 📄 manage.py               # Django management script
├── 📄 requirements.txt        # Python dependencies
├── 📄 .env                    # Environment variables
├── 📄 .env.example            # Environment template
├── 📄 .gitignore              # Git ignore rules
└── 📄 README.md               # Dokumentasi ini
```

---

## 🧪 Testing

### Run All Tests

```bash
python manage.py test
```

### Test Specific App

```bash
python manage.py test accounts
python manage.py test bookings
```

### Coverage Report

```bash
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html  # Generate HTML report
```

---

## 🚢 Deployment

### Production Checklist

- [ ] Set `DEBUG=False` di `.env`
- [ ] Konfigurasi `ALLOWED_HOSTS`
- [ ] Setup database production
- [ ] Konfigurasi static files serving
- [ ] Setup SSL certificate
- [ ] Configure email backend
- [ ] Setup backup database
- [ ] Enable security headers
- [ ] Setup monitoring & logging

### Deploy ke Server

```bash
# Collect static files
python manage.py collectstatic --noinput

# Migrasi database
python manage.py migrate --no-input

# Gunakan Gunicorn
pip install gunicorn
gunicorn summit_book_project.wsgi:application --bind 0.0.0.0:8000
```

---

## 🔥 Troubleshooting

### Error: MySQL Build Failed (Windows)

**Solusi:**
1. Download MySQL Connector C dari [MySQL Downloads](https://dev.mysql.com/downloads/connector/c/)
2. Install dan tambahkan ke PATH
3. Restart terminal dan reinstall `mysqlclient`

### Error: Port 8000 Already in Use

**Windows:**
```bash
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

**Mac/Linux:**
```bash
lsof -ti:8000 | xargs kill -9
```

### Error: Static Files Not Loading

```bash
python manage.py collectstatic --clear
python manage.py collectstatic
```

### Error: Database Connection Failed

1. Cek MySQL service running
2. Verifikasi credentials di `.env`
3. Test koneksi manual: `mysql -u summitbook_user -p`

### Dependencies Conflict

```bash
pip install pipreqs
pipreqs . --force
pip install -r requirements.txt --upgrade
```

---

## 🤝 Kontribusi

Kami menerima kontribusi! Silakan ikuti langkah berikut:

1. Fork repository ini
2. Buat branch fitur (`git checkout -b feature/AmazingFeature`)
3. Commit perubahan (`git commit -m 'Add some AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Buat Pull Request

### Coding Standards

- Follow PEP 8 untuk Python code
- Gunakan meaningful variable names
- Tambahkan docstrings untuk functions
- Write tests untuk fitur baru

---

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.

---

## 👥 Tim Pengembang

- **Project Lead** - [Nama Anda](https://github.com/username)
- **Backend Developer** - [Nama](https://github.com/username)
- **Frontend Developer** - [Nama](https://github.com/username)

---

## 📞 Support & Kontak

- 📧 Email: support@summitbook.com
- 🐛 Issues: [GitHub Issues](https://github.com/username/summit-book/issues)
- 📖 Documentation: [Wiki](https://github.com/username/summit-book/wiki)
- 💬 Discord: [Join Community](https://discord.gg/summitbook)

---

## 🙏 Acknowledgments

- [Django Documentation](https://docs.djangoproject.com/)
- [Bootstrap](https://getbootstrap.com/)
- [MySQL](https://www.mysql.com/)
- Komunitas Open Source Indonesia

---

<div align="center">

**⭐ Jika project ini membantu, berikan star di GitHub! ⭐**

Made with ❤️ by Summit Book Team
