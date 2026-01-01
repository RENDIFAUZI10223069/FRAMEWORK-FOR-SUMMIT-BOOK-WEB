from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from datetime import date, timedelta

User = get_user_model()

# Kode admin rahasia (ganti dengan yang Anda inginkan)
ADMIN_SECRET_CODE = "RINJANI2025"


class PendakiRegisterForm(UserCreationForm):
    """Form registrasi untuk Pendaki"""
    
    first_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nama depan'
        }),
        label='Nama Depan'
    )
    
    last_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nama belakang'
        }),
        label='Nama Belakang'
    )
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'nama@email.com'
        }),
        label='Email'
    )
    
    phone_number = forms.CharField(
        max_length=17,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '08123456789'
        }),
        label='Nomor Telepon'
    )
    
    date_of_birth = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'max': date.today().isoformat()
        }),
        label='Tanggal Lahir'
    )
    
    blood_type = forms.ChoiceField(
        required=True,
        choices=[('', 'Pilih Golongan Darah')] + [
            ('A', 'A'), ('B', 'B'), ('AB', 'AB'), ('O', 'O')
        ],
        widget=forms.Select(attrs={
            'class': 'form-select'
        }),
        label='Golongan Darah'
    )
    
    emergency_contact_name = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nama keluarga/kerabat'
        }),
        label='Kontak Darurat (Nama)'
    )
    
    emergency_contact_phone = forms.CharField(
        max_length=17,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '08123456789'
        }),
        label='Kontak Darurat (Telepon)'
    )
    
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Minimal 8 karakter'
        }),
        help_text='Password minimal 8 karakter, kombinasi huruf dan angka'
    )
    
    password2 = forms.CharField(
        label='Konfirmasi Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ketik ulang password'
        }),
        help_text='Masukkan password yang sama untuk verifikasi'
    )
    
    agree_terms = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        label='Saya setuju dengan syarat dan ketentuan'
    )
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 
                  'date_of_birth', 'blood_type', 'emergency_contact_name', 
                  'emergency_contact_phone', 'password1', 'password2']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Email sudah terdaftar. Silakan gunakan email lain atau login.')
        return email.lower()
    
    def clean_date_of_birth(self):
        dob = self.cleaned_data.get('date_of_birth')
        if dob:
            min_age = date.today() - timedelta(days=17*365)
            if dob > min_age:
                raise ValidationError('Anda harus berusia minimal 17 tahun untuk mendaftar.')
            
            max_age = date.today() - timedelta(days=100*365)
            if dob < max_age:
                raise ValidationError('Tanggal lahir tidak valid.')
        return dob
    
    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if len(password) < 8:
            raise ValidationError('Password minimal 8 karakter.')
        if password.isdigit():
            raise ValidationError('Password tidak boleh hanya angka.')
        if password.isalpha():
            raise ValidationError('Password harus mengandung kombinasi huruf dan angka.')
        return password
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['email'].split('@')[0]
        user.role = 'pendaki'
        user.phone_number = self.cleaned_data['phone_number']
        user.date_of_birth = self.cleaned_data['date_of_birth']
        user.blood_type = self.cleaned_data['blood_type']
        user.emergency_contact_name = self.cleaned_data['emergency_contact_name']
        user.emergency_contact_phone = self.cleaned_data['emergency_contact_phone']
        
        if commit:
            user.save()
        return user


class AdminRegisterForm(UserCreationForm):
    """Form registrasi untuk Admin"""
    
    first_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nama depan'
        }),
        label='Nama Depan'
    )
    
    last_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nama belakang'
        }),
        label='Nama Belakang'
    )
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'admin@summitbook.com'
        }),
        label='Email'
    )
    
    phone_number = forms.CharField(
        max_length=17,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '08123456789'
        }),
        label='Nomor Telepon'
    )
    
    position = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Misal: Manager Booking, Staff Operasional'
        }),
        label='Jabatan'
    )
    
    admin_secret_code = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Kode rahasia admin'
        }),
        label='Kode Rahasia Admin',
        help_text='Hubungi supervisor untuk mendapatkan kode ini'
    )
    
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Minimal 8 karakter'
        }),
        help_text='Password minimal 8 karakter, kombinasi huruf dan angka'
    )
    
    password2 = forms.CharField(
        label='Konfirmasi Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ketik ulang password'
        })
    )
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 
                  'position', 'admin_secret_code', 'password1', 'password2']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Email sudah terdaftar.')
        return email.lower()
    
    def clean_admin_secret_code(self):
        code = self.cleaned_data.get('admin_secret_code')
        if code != ADMIN_SECRET_CODE:
            raise ValidationError('Kode admin tidak valid. Hubungi supervisor untuk mendapatkan kode yang benar.')
        return code
    
    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if len(password) < 8:
            raise ValidationError('Password minimal 8 karakter.')
        if password.isdigit():
            raise ValidationError('Password tidak boleh hanya angka.')
        return password
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['email'].split('@')[0]
        user.role = 'admin'
        user.phone_number = self.cleaned_data['phone_number']
        user.position = self.cleaned_data['position']
        user.admin_code = self.cleaned_data['admin_secret_code']
        user.is_staff = True  # Admin bisa akses Django Admin
        
        if commit:
            user.save()
        return user


class UserLoginForm(AuthenticationForm):
    """Form untuk login (semua role)"""
    
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'nama@email.com',
            'autofocus': True
        }),
        label='Email'
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Password'
        }),
        label='Password'
    )
    
    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        label='Ingat Saya'
    )