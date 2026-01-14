# checkins/admin.py
from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import CheckIn

@admin.register(CheckIn)
class CheckInAdmin(admin.ModelAdmin):
    list_display = [
        'booking_code',
        'participant_name',
        'status_badge',
        'created_at',
        'verified_by',
        'verified_at'
    ]
    list_filter = [
        'status',
        'created_at',
        'verified_at',
        # 'booking__mountain'  # ← HAPUS INI jika field tidak ada
    ]
    search_fields = [
        'booking__booking_code',
        'participant__full_name',
        'participant__id_number',
        'qr_data'
    ]
    readonly_fields = [
        'created_at',
        'updated_at',
        'qr_code_preview',
        'id_card_preview',
        'selfie_preview'
    ]
    
    fieldsets = (
        ('Informasi Booking', {
            'fields': ('booking', 'participant')
        }),
        ('Dokumen', {
            'fields': (
                'id_card_photo',
                'id_card_preview',
                'selfie_photo',
                'selfie_preview'
            )
        }),
        ('QR Code', {
            'fields': ('qr_code', 'qr_code_preview', 'qr_data')
        }),
        ('Status Verifikasi', {
            'fields': (
                'status',
                'verified_by',
                'verified_at',
                'rejection_reason',
                'notes'
            )
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['verify_checkins', 'reject_checkins']
    
    def booking_code(self, obj):
        return obj.booking.booking_code
    booking_code.short_description = 'Kode Booking'
    
    def participant_name(self, obj):
        return obj.participant.full_name
    participant_name.short_description = 'Nama Peserta'
    
    def status_badge(self, obj):
        colors = {
            'pending': '#ffc107',
            'verified': '#28a745',
            'rejected': '#dc3545',
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; '
            'border-radius: 3px; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def qr_code_preview(self, obj):
        if obj.qr_code:
            return format_html(
                '<img src="{}" style="max-width: 200px; max-height: 200px;" />',
                obj.qr_code.url
            )
        return "Belum ada QR Code"
    qr_code_preview.short_description = 'Preview QR Code'
    
    def id_card_preview(self, obj):
        if obj.id_card_photo:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 300px;" />',
                obj.id_card_photo.url
            )
        return "Belum ada foto KTP"
    id_card_preview.short_description = 'Preview KTP'
    
    def selfie_preview(self, obj):
        if obj.selfie_photo:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 300px;" />',
                obj.selfie_photo.url
            )
        return "Belum ada foto selfie"
    selfie_preview.short_description = 'Preview Selfie'
    
    def verify_checkins(self, request, queryset):
        updated = queryset.filter(status='pending').update(
            status='verified',
            verified_by=request.user,
            verified_at=timezone.now()
        )
        self.message_user(
            request,
            f'{updated} check-in berhasil diverifikasi.'
        )
    verify_checkins.short_description = 'Verifikasi check-in terpilih'
    
    def reject_checkins(self, request, queryset):
        updated = queryset.filter(status='pending').update(
            status='rejected',
            verified_by=request.user,
            verified_at=timezone.now()
        )
        self.message_user(
            request,
            f'{updated} check-in berhasil ditolak.'
        )
    reject_checkins.short_description = 'Tolak check-in terpilih'
    
    def save_model(self, request, obj, form, change):
        if change and 'status' in form.changed_data:
            if obj.status in ['verified', 'rejected']:
                if not obj.verified_by:
                    obj.verified_by = request.user
                if not obj.verified_at:
                    obj.verified_at = timezone.now()
        super().save_model(request, obj, form, change)