from django.contrib import admin
from .models import Booking, BookingParticipant

class BookingParticipantInline(admin.TabularInline):
    model = BookingParticipant
    extra = 0
    fields = ['full_name', 'id_number', 'phone_number', 'blood_type']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['booking_code', 'user', 'route', 'start_date', 'num_participants', 'total_price', 'status', 'created_at']
    list_filter = ['status', 'start_date', 'route', 'created_at']
    search_fields = ['booking_code', 'user__email', 'user__first_name', 'user__last_name']
    readonly_fields = ['booking_code', 'total_price', 'created_at', 'updated_at']
    inlines = [BookingParticipantInline]
    date_hierarchy = 'start_date'
    
    fieldsets = (
        ('Booking Info', {
            'fields': ('booking_code', 'user', 'route', 'status')
        }),
        ('Schedule', {
            'fields': ('start_date', 'end_date')
        }),
        ('Participants & Pricing', {
            'fields': ('num_participants', 'price_per_person', 'total_price')
        }),
        ('Payment', {
            'fields': ('payment_method', 'payment_proof', 'paid_at')
        }),
        ('Notes', {
            'fields': ('notes', 'admin_notes')
        }),
        ('Status Tracking', {
            'fields': ('confirmed_at', 'cancelled_at', 'cancellation_reason', 'created_at', 'updated_at')
        }),
    )

@admin.register(BookingParticipant)
class BookingParticipantAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'booking', 'id_number', 'phone_number', 'blood_type']
    list_filter = ['blood_type', 'gender']
    search_fields = ['full_name', 'id_number', 'booking__booking_code']
    raw_id_fields = ['booking']