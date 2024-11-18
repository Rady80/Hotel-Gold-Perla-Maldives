"""
Django nastavení pro projekt HMS.

Tento soubor obsahuje nastavení projektu včetně cest, aplikací, databáze, autentizace a dalších.
Pro více informací o tomto souboru:
https://docs.djangoproject.com/en/4.2/topics/settings/
"""

from pathlib import Path
import os

# ------------------------------
# Základní nastavení projektu
# ------------------------------

# Cesta k základnímu adresáři projektu
BASE_DIR = Path(__file__).resolve().parent.parent

# Tajný klíč (v produkci by měl být uložen v proměnných prostředí)
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'replace_with_your_secret_key_for_deployment')

# Ladicí režim (v produkci musí být nastaven na False)
DEBUG = os.getenv('DJANGO_DEBUG', 'True') == 'True'

# Povolené hosty (v produkci nastavte na domény nebo IP adresy serveru)
ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# ------------------------------
# Aplikace a middleware
# ------------------------------

# Instalované aplikace
INSTALLED_APPS = [
    # Vestavěné Django aplikace
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Aplikace třetích stran
    'phonenumber_field',  # Pro zpracování telefonních čísel

    # Lokální aplikace
    'hotel',
    'accounts',
    'room',
]

# Middleware (pro bezpečnost, autentizaci a další funkce)
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
# Hlavní konfigurace URL a WSGI
# ------------------------------

# Hlavní konfigurace URL
ROOT_URLCONF = 'HMS.urls'

# WSGI aplikace (používá se při nasazení na server)
WSGI_APPLICATION = 'HMS.wsgi.application'

# ------------------------------
# Nastavení databáze
# ------------------------------

# SQLite databáze (výchozí pro vývoj)
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
# Nastavení autentizace
# ------------------------------

# Přesměrování po přihlášení a odhlášení
LOGIN_REDIRECT_URL = '/accounts/dashboard/'  # Kam přesměrovat uživatele po přihlášení
LOGIN_URL = '/login/'  # URL přihlašovací stránky
LOGOUT_REDIRECT_URL = '/'  # Kam přesměrovat uživatele po odhlášení

# Backend pro autentizaci
AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend']

# ------------------------------
# Lokalizace a časová zóna
# ------------------------------

LANGUAGE_CODE = 'cs'  # Jazyk aplikace (čeština)
TIME_ZONE = 'Europe/Prague'  # Časové pásmo
USE_I18N = True  # Povolit internacionalizaci
USE_L10N = True  # Povolit lokalizaci (formáty dat a čísel)
USE_TZ = True  # Povolit časové zóny

# ------------------------------
# Statické a mediální soubory
# ------------------------------

# Statické soubory
STATIC_URL = '/static/'  # URL cesta pro statické soubory
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]  # Cesta pro vývojové statické soubory
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Cesta pro produkční statické soubory

# Média (nahrané soubory)
MEDIA_URL = '/media/'  # URL cesta pro média
MEDIA_ROOT = BASE_DIR / 'media'  # Složka pro ukládání mediálních souborů

# ------------------------------
# Nastavení šablon
# ------------------------------

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # Cesta k vlastním šablonám
        'APP_DIRS': True,  # Automatické vyhledání šablon v aplikacích
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
# Nastavení e-mailu
# ------------------------------

# E-mailové nastavení pro SMTP server
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('DJANGO_EMAIL_HOST_USER', 'your_email@gmail.com')  # E-mailový účet
EMAIL_HOST_PASSWORD = os.getenv('DJANGO_EMAIL_HOST_PASSWORD', 'your_password')  # Heslo k e-mailu

# ------------------------------
# Protokolování
# ------------------------------

# Základní logování (loguje do konzole během vývoje)
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