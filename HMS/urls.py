"""
Konfigurace URL pro projekt HMS.

Tento soubor definuje směrování URL projektu. Každá URL je svázána s konkrétním pohledem (view).
Více informací: https://docs.djangoproject.com/en/4.2/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from hotel import views as hotel_views  # Import pohledů z aplikace hotel
from accounts import views as accounts_views  # Import pohledů z aplikace accounts
from django.contrib.auth import views as auth_views

# ------------------------------
# Definice směrování URL
# ------------------------------
urlpatterns = [
    # Administrace
    path('admin/', admin.site.urls),  # Admin rozhraní

    # Hlavní stránka projektu
    path('', include('home.urls')),  # Směrování root URL na aplikaci "home"

    # Směrování aplikace 'hotel'
    path('hotel/', include('hotel.urls')),  # Hlavní URL aplikace hotel (směřuje na hotel.urls)

    # Směrování aplikace 'bookings'
    path('bookings/', include('bookings.urls')),  # Směrování aplikace bookings (rezervace)

    # Směrování aplikace 'rooms'
    path('rooms/', include('rooms.urls')),  # Směrování aplikace rooms (pokoje)

    # Směrování aplikace 'accounts'
    path('accounts/', include('accounts.urls')),  # Směrování aplikace accounts (uživatelé, registrace, přihlášení)

    # Přihlašovací a odhlašovací stránky
    path(
        'login/',
        auth_views.LoginView.as_view(template_name='registration/login.html'),  # Vlastní šablona pro přihlášení
        name='login'
    ),
    path(
        'logout/',
        auth_views.LogoutView.as_view(next_page='/'),  # Přesměrování na hlavní stránku po odhlášení
        name='logout'
    ),

    # Registrace nového uživatele
    path('register/', accounts_views.register_page, name='register'),  # Stránka pro registraci nových uživatelů

    # Statická stránka "Zlatá Perla"
    path('pearl/', hotel_views.pearl_view, name='pearl'),  # Zobrazení statické stránky Zlatá Perla

    # Profil události
    path('event/<int:event_id>/', hotel_views.event_profile, name='event-profile'),  # Detail konkrétní události

    # Zobrazení refundací
    path('refunds/', hotel_views.refunds_view, name='refunds'),  # Zobrazení seznamu refundací
]

# ------------------------------
# Podpora statických a mediálních souborů během vývoje
# ------------------------------
if settings.DEBUG:
    # Směrování pro statické soubory (CSS, JavaScript, obrázky)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    # Směrování pro mediální soubory (nahrané obrázky, dokumenty)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)