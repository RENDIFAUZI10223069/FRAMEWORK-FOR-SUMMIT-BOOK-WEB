from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('accounts/', include('accounts.urls')),
    path('mountains/', include('mountains.urls')),      # Person 1
    path('bookings/', include('bookings.urls')),        # Person 2
    path('checkins/', include('checkins.urls')),        # Person 3
    path('dashboard/', include('dashboard.urls')),      # Person 4 & 5
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)