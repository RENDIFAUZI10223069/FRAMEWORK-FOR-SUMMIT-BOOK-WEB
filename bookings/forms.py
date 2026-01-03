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
    """Form untuk data peserta"""
    
    class Meta:
        model = BookingParticipant
        fields = [
            'full_name', 'id_number', 'date_of_birth', 'gender',
            'phone_number', 'email', 'blood_type',
            'emergency_contact_name', 'emergency_contact_phone',
            'emergency_contact_relation', 'health_notes'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sesuai KTP'}),
            'id_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'NIK 16 digit'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '08xxxxxxxxxx'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'blood_type': forms.Select(attrs={'class': 'form-select'}),
            'emergency_contact_name': forms.TextInput(attrs={'class': 'form-control'}),
            'emergency_contact_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'emergency_contact_relation': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contoh: Orang Tua'}),
            'health_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Riwayat penyakit, alergi, dll (opsional)'}),
        }
    
    def clean_date_of_birth(self):
        dob = self.cleaned_data.get('date_of_birth')
        min_age = date.today() - timedelta(days=17*365)
        if dob > min_age:
            raise ValidationError('Peserta harus berusia minimal 17 tahun')
        return dob


class PaymentForm(forms.ModelForm):
    """Form untuk upload bukti pembayaran"""
    
    class Meta:
        model = Booking
        fields = ['payment_method', 'payment_proof']
        widgets = {
            'payment_method': forms.Select(attrs={'class': 'form-select'}),
            'payment_proof': forms.FileInput(attrs={'class': 'form-control'}),
        }