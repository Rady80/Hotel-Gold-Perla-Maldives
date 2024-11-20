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
    'phonenumber_field',
    'hotel',  # Aplikace pro správu hotelu
    'accounts',  # Aplikace pro správu uživatelských účtů
    'room.apps.RoomConfig',  # Aplikace pro správu pokojů
    'myapp',
]

# Middleware
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

LOGIN_REDIRECT_URL = '/accounts/dashboard/'  # Přesměrování po přihlášení
LOGIN_URL = '/login/'  # URL pro přihlášení
LOGOUT_REDIRECT_URL = '/'  # Přesměrování po odhlášení
AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend']

# ------------------------------
# Lokalizace a časová zóna
# ------------------------------

LANGUAGE_CODE = 'cs'  # Jazyk aplikace (čeština)
TIME_ZONE = 'Europe/Prague'  # Časová zóna
USE_I18N = True  # Internacionalizace (překlady)
USE_L10N = True  # Lokalizace formátů dat a čísel
USE_TZ = True  # Povolení časových zón

# ------------------------------
# Statické a mediální soubory
# ------------------------------

STATIC_URL = '/static/'  # URL pro statické soubory
STATICFILES_DIRS = [BASE_DIR / 'static']  # Cesty ke statickým souborům
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Kořenový adresář pro produkční nasazení

MEDIA_URL = '/media/'  # URL pro mediální soubory
MEDIA_ROOT = BASE_DIR / 'media'  # Kořenový adresář mediálních souborů

# ------------------------------
# Nastavení šablon
# ------------------------------

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Složky s šablonami
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
EMAIL_HOST = 'smtp.gmail.com'  # SMTP server
EMAIL_PORT = 587  # SMTP port
EMAIL_USE_TLS = True  # Šifrování
EMAIL_HOST_USER = os.getenv('DJANGO_EMAIL_HOST_USER', 'your_email@gmail.com')  # Uživatelské jméno
EMAIL_HOST_PASSWORD = os.getenv('DJANGO_EMAIL_HOST_PASSWORD', 'your_password')  # Heslo

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

SECURE_BROWSER_XSS_FILTER = True  # Ochrana proti XSS útokům
SECURE_CONTENT_TYPE_NOSNIFF = True  # Ochrana proti nosní sniffing útokům

# Maximální velikost nahrávaných souborů (v bajtech)
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5 MB