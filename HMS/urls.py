"""
Konfigurace URL pro projekt HMS

Tento soubor definuje směrování URL projektu. Každá URL je svázána s konkrétním pohledem (view).
Více informací: https://docs.djangoproject.com/en/3.1/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views  # Vestavěné pohledy pro přihlášení a odhlášení
from django.conf import settings
from django.conf.urls.static import static
from hotel.views import home, pearl_view  # Import pohledů z aplikace hotel
from accounts.views import register_page  # Import pohledu pro registraci uživatele
from django.contrib.auth import views as auth_views

# Definice směrování URL
urlpatterns = [
    # Administrace
    path('admin/', admin.site.urls, name='admin'),  # URL pro přístup do administrace

    # Domovská stránka
    path('', home, name='home'),  # Domovská stránka projektu
    
    # Přihlašovací stránka
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),

    # Statická stránka Zlatá Perla
    path('pearl/', pearl_view, name='pearl'),  # Zobrazení stránky Zlatá Perla

    # Uživatelské operace (přihlášení, odhlášení, registrace)
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),  # Přihlášení
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),  # Odhlášení uživatele
    path('register/', register_page, name='register'),  # Registrace nového uživatele

    # Zahrnutí dalších URL z aplikace accounts
    path('accounts/', include('accounts.urls')),  # URL aplikace accounts (další pohledy)
]

# Podpora statických a mediálních souborů během vývoje (pouze pokud DEBUG=True)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)