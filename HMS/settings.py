"""
Django nastavení pro projekt HMS.

Tento soubor obsahuje základní konfiguraci projektu, včetně cest, aplikací,
databáze, autentizace a dalších funkcí.

Více informací:
https://docs.djangoproject.com/en/4.2/topics/settings/
"""

from pathlib import Path
import os

# ------------------------------
# Základní nastavení projektu
# ------------------------------

# Absolutní cesta k základnímu adresáři projektu
BASE_DIR = Path(__file__).resolve().parent.parent

# Tajný klíč (v produkci musí být bezpečně uložen a nikdy nesdílen)
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'nahraďte_vlastním_tajným_klíčem')

# Ladící režim (v produkci nastavte na False)
DEBUG = os.getenv('DJANGO_DEBUG', 'True') == 'True'

# Povolené hosty (v produkci specifikujte konkrétní domény/IP adresy)
ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# ------------------------------
# Aplikace a middleware
# ------------------------------

# Instalované aplikace
INSTALLED_APPS = [
    # Vestavěné aplikace Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'phonenumber_field',  # Podpora telefonních čísel

    # Vlastní aplikace
    'hotel',
    'accounts',
    'room.apps.RoomConfig',
    'myapp',
    'bookings',
    'rooms',
    'home',
]

# Middleware - řetězec middlewarů, které budou zpracovávat požadavky
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ------------------------------
# URL a WSGI konfigurace
# ------------------------------

ROOT_URLCONF = 'HMS.urls'
WSGI_APPLICATION = 'HMS.wsgi.application'

# ------------------------------
# Databázová konfigurace
# ------------------------------

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ------------------------------
# Validace hesel
# ------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 8}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ------------------------------
# Autentizace a přihlášení
# ------------------------------

LOGIN_REDIRECT_URL = '/accounts/dashboard/'
LOGIN_URL = '/login/'
LOGOUT_REDIRECT_URL = '/'
AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend']

# ------------------------------
# Lokalizace a časová zóna
# ------------------------------

LANGUAGE_CODE = 'cs'
TIME_ZONE = 'Europe/Prague'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# ------------------------------
# Statické a mediální soubory
# ------------------------------

# Statické soubory (CSS, JavaScript, obrázky)
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'hotel' / 'static']  # Statické soubory aplikace hotel
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Složka pro shromažďování statických souborů (pro produkci)

# Mediální soubory (nahrané uživatelské soubory)
MEDIA_URL = '/media/'  # URL prefix pro mediální soubory
MEDIA_ROOT = BASE_DIR / 'media'  # Cesta k adresáři mediálních souborů

# ------------------------------
# Nastavení šablon
# ------------------------------

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Hlavní adresář pro šablony
        'APP_DIRS': True,  # Automatické načítání šablon z aplikací
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ------------------------------
# E-mailová konfigurace
# ------------------------------

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('DJANGO_EMAIL_HOST_USER', 'your_email@gmail.com')
EMAIL_HOST_PASSWORD = os.getenv('DJANGO_EMAIL_HOST_PASSWORD', 'your_password')

# ------------------------------
# Protokolování
# ------------------------------

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG' if DEBUG else 'ERROR',
    },
}

# ------------------------------
# Další zabezpečení
# ------------------------------

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# Maximální velikost nahrávaných souborů (v bajtech)
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5 MB