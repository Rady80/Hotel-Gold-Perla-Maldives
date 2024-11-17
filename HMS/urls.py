"""
HMS URL Configuration

Tento soubor definuje směrování URL pro projekt. Každá URL směřuje na konkrétní view (pohled).
Více informací: https://docs.djangoproject.com/en/3.1/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from hotel.views import edit_food_menu, pearl_view  # Opravený import
from accounts.views import *
from room.views import *
from hotel.views import *

urlpatterns = [
    # Admin panel
    path('admin/', admin.site.urls, name="admin"),

    # Domovská stránka
    path('', home, name="home"),

    # Ostatní URL...

    # Obrázek Zlaté Perly
    path('pearl/', pearl_view, name='pearl'),  # Odkaz na Zlatou perlu
]

# Statické a mediální soubory během vývoje
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)