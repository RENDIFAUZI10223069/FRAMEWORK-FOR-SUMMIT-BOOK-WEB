from django import forms
from .models import CheckIn

class CheckInForm(forms.ModelForm):
    """Form untuk check-in peserta"""
    
    class Meta:
        model = CheckIn
        fields = ['id_card_photo', 'selfie_photo', 'notes']
        widgets = {
            'id_card_photo': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
                'required': True
            }),
            'selfie_photo': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Catatan tambahan (opsional)'
            }),
        }
    
    def clean_id_card_photo(self):
        photo = self.cleaned_data.get('id_card_photo')
        if photo:
            # Check file size (max 2MB)
            if photo.size > 2 * 1024 * 1024:
                raise forms.ValidationError('Ukuran file maksimal 2MB')
        return photo
    
    def clean_selfie_photo(self):
        photo = self.cleaned_data.get('selfie_photo')
        if photo:
            # Check file size (max 2MB)
            if photo.size > 2 * 1024 * 1024:
                raise forms.ValidationError('Ukuran file maksimal 2MB')
        return photo