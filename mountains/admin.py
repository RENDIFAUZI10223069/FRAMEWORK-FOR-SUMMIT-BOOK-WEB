from django.contrib import admin
from .models import Mountain, Route, MountainGallery

@admin.register(Mountain)
class MountainAdmin(admin.ModelAdmin):
    list_display = ['name', 'height', 'location', 'difficulty_level', 'is_active', 'created_at']
    list_filter = ['difficulty_level', 'is_active', 'province']
    search_fields = ['name', 'location', 'province']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_active']
    date_hierarchy = 'created_at'

@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ['name', 'mountain', 'duration_days', 'difficulty_level', 'price_per_person', 'is_active']
    list_filter = ['mountain', 'difficulty_level', 'is_active']
    search_fields = ['name', 'mountain__name', 'starting_point']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_active']
    raw_id_fields = ['mountain']

@admin.register(MountainGallery)
class MountainGalleryAdmin(admin.ModelAdmin):
    list_display = ['title', 'mountain', 'route', 'is_featured', 'order', 'created_at']
    list_filter = ['mountain', 'is_featured']
    search_fields = ['title', 'mountain__name']
    list_editable = ['is_featured', 'order']
    raw_id_fields = ['mountain', 'route']