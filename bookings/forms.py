from django import forms
from django.core.exceptions import ValidationError
from datetime import date, timedelta
from .models import Booking, BookingParticipant

class BookingForm(forms.ModelForm):
    """Form untuk membuat booking"""
    
    class Meta:
        model = Booking
        fields = ['route', 'start_date', 'num_participants', 'notes']
        widgets = {
            'route': forms.Select(attrs={'class': 'form-select'}),
            'start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'min': (date.today() + timedelta(days=7)).isoformat()
            }),
            'num_participants': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 10
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Catatan tambahan (opsional)'
            }),
        }
    
    def clean_start_date(self):
        start_date = self.cleaned_data.get('start_date')
        min_date = date.today() + timedelta(days=7)
        
        if start_date < min_date:
            raise ValidationError('Booking minimal H-7 dari tanggal keberangkatan')
        
        return start_date
    
    def clean_num_participants(self):
        num = self.cleaned_data.get('num_participants')
        if num < 1:
            raise ValidationError('Minimal 1 peserta')
        if num > 10:
            raise ValidationError('Maksimal 10 peserta per booking')
        return num


class BookingParticipantForm(forms.ModelForm):
    class Meta:
        model = BookingParticipant
        fields = [
            'full_name', 'id_number', 'date_of_birth', 'gender', 'blood_type',
            'phone_number', 'email',
            'address', 'city', 'province', 'postal_code',  # NEW
            'emergency_contact_name', 'emergency_contact_phone', 'emergency_contact_relation',
            'health_notes',
            'health_certificate'  # NEW
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nama lengkap sesuai KTP'
            }),
            'id_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Contoh: 3201234567890123'
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'gender': forms.Select(attrs={
                'class': 'form-select'
            }),
            'blood_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '08123456789'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email@example.com'
            }),
            # NEW: Address fields
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Jalan, RT/RW, Kelurahan, Kecamatan'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Contoh: Bandung'
            }),
            'province': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Contoh: Jawa Barat'
            }),
            'postal_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Contoh: 40123'
            }),
            'emergency_contact_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nama keluarga/kerabat terdekat'
            }),
            'emergency_contact_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '08123456789'
            }),
            'emergency_contact_relation': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Contoh: Ayah, Ibu, Saudara, Teman'
            }),
            'health_notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Contoh: Alergi obat, Asma, Diabetes, dll'
            }),
            # NEW: Health certificate upload
            'health_certificate': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.jpg,.jpeg,.png'
            }),
        }
    
    def clean_id_number(self):
        id_number = self.cleaned_data.get('id_number')
        if len(id_number) < 10:
            raise forms.ValidationError('Nomor identitas minimal 10 karakter')
        return id_number
    
    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if not phone.startswith('0'):
            raise forms.ValidationError('Nomor telepon harus diawali dengan 0')
        return phone
    
    def clean_emergency_contact_phone(self):
        phone = self.cleaned_data.get('emergency_contact_phone')
        if not phone.startswith('0'):
            raise forms.ValidationError('Nomor telepon harus diawali dengan 0')
        return phone
    
    def clean_health_certificate(self):
        file = self.cleaned_data.get('health_certificate')
        if file:
            # Check file size (max 2MB)
            if file.size > 2 * 1024 * 1024:
                raise forms.ValidationError('Ukuran file maksimal 2MB')
            
            # Check file extension
            ext = file.name.split('.')[-1].lower()
            if ext not in ['pdf', 'jpg', 'jpeg', 'png']:
                raise forms.ValidationError('Format file harus PDF, JPG, JPEG, atau PNG')
        
        return file

class PaymentForm(forms.ModelForm):
    """Form untuk upload bukti pembayaran"""
    
    class Meta:
        model = Booking
        fields = ['payment_method', 'payment_proof']
        widgets = {
            'payment_method': forms.Select(attrs={'class': 'form-select'}),
            'payment_proof': forms.FileInput(attrs={'class': 'form-control'}),
        }