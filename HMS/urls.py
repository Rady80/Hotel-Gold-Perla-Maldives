"""
Konfigurace URL pro projekt HMS.

Tento soubor definuje směrování URL projektu. Každá URL je svázána s konkrétním pohledem (view).
Více informací: https://docs.djangoproject.com/en/4.2/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views  # Vestavěné pohledy pro přihlášení a odhlášení
from django.conf import settings
from django.conf.urls.static import static
from hotel.views import home, pearl_view, event_profile, refunds_view  # Import pohledů z aplikace hotel
from accounts.views import register_page  # Import pohledu pro registraci uživatele

# Definice směrování URL
urlpatterns = [
    # Administrace
    path('admin/', admin.site.urls, name='admin'),  # URL pro přístup do administrace

    # URL aplikace hotel
    path('hotel/', include('hotel.urls')),  # Zahrnutí směrování aplikace hotel

    # URL aplikace accounts
    path('accounts/', include('accounts.urls')),  # Směrování pro aplikaci accounts

    # Domovská stránka projektu
    path('', home, name='home'),  # Hlavní URL směřující na domovskou stránku

    # Přihlašovací a odhlašovací stránky
    path(
        'login/',
        auth_views.LoginView.as_view(template_name='registration/login.html'),
        name='login'
    ),  # Stránka pro přihlášení uživatele
    path(
        'logout/',
        auth_views.LogoutView.as_view(next_page='/'),
        name='logout'
    ),  # Stránka pro odhlášení uživatele s přesměrováním na hlavní stránku

    # Registrace nového uživatele
    path('register/', register_page, name='register'),  # Stránka pro registraci nových uživatelů

    # Statická stránka "Zlatá Perla"
    path('pearl/', pearl_view, name='pearl'),  # Zobrazení statické stránky Zlatá Perla

    # URL pro profil události
    path('event/<int:event_id>/', event_profile, name='event-profile'),  # Detail konkrétní události

    # URL pro zobrazení refundací
    path('refunds/', refunds_view, name='refunds'),  # Zobrazení seznamu refundací
]

# Podpora statických a mediálních souborů během vývoje
if settings.DEBUG:
    # Směrování pro statické soubory (CSS, JavaScript, obrázky)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    # Směrování pro mediální soubory (nahrané obrázky, dokumenty)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)