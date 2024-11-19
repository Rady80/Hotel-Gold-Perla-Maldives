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

# Tajný klíč (musí být v produkci bezpečně uložen)
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'nahraďte_vlastním_tajným_klíčem')

# Ladící režim (v produkci by měl být nastaven na False)
DEBUG = os.getenv('DJANGO_DEBUG', 'True') == 'True'

# Povolené hosty (v produkci nastavte konkrétní domény/IP adresy)
ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# ------------------------------
# Aplikace a middleware
# ------------------------------

# Instalované aplikace
INSTALLED_APPS = [
    # Django vestavěné aplikace
    'django.contrib.admin',  # Admin rozhraní pro správu
    'django.contrib.auth',  # Autentizace uživatelů
    'django.contrib.contenttypes',  # Základní typy pro modely
    'django.contrib.sessions',  # Správa relací
    'django.contrib.messages',  # Správa zpráv pro uživatele
    'django.contrib.staticfiles',  # Statické soubory (CSS, JavaScript, obrázky)

    # Aplikace třetích stran
    'phonenumber_field',  # Zpracování telefonních čísel

    # Lokální aplikace
    'hotel',  # Aplikace pro správu hotelu
    'accounts',  # Aplikace pro správu uživatelských účtů
    'room.apps.RoomConfig',  # Použití konfigurace aplikace místo přímého názvu 'room'
]

# Middleware pro různé operace, včetně zabezpečení
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',  # Zabezpečení aplikace
    'django.contrib.sessions.middleware.SessionMiddleware',  # Správa session (relace)
    'django.middleware.common.CommonMiddleware',  # Různé běžné operace
    'django.middleware.csrf.CsrfViewMiddleware',  # Ochrana proti CSRF útokům
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Autentizace uživatelů
    'django.contrib.messages.middleware.MessageMiddleware',  # Správa zpráv
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # Ochrana proti Clickjacking útokům
]

# ------------------------------
# URL a WSGI konfigurace
# ------------------------------

ROOT_URLCONF = 'HMS.urls'  # Nastavení URL konfiguračního souboru
WSGI_APPLICATION = 'HMS.wsgi.application'  # WSGI aplikace pro nasazení

# ------------------------------
# Nastavení databáze
# ------------------------------

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Výchozí databáze SQLite
        'NAME': BASE_DIR / 'db.sqlite3',  # Umístění databázového souboru
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

LOGIN_REDIRECT_URL = '/accounts/dashboard/'  # Kam přesměrovat po přihlášení
LOGIN_URL = '/login/'  # URL přihlašovací stránky
LOGOUT_REDIRECT_URL = '/'  # Kam přesměrovat po odhlášení

AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend']

# ------------------------------
# Lokalizace a časová zóna
# ------------------------------

LANGUAGE_CODE = 'cs'  # Jazyk aplikace (čeština)
TIME_ZONE = 'Europe/Prague'  # Časová zóna
USE_I18N = True  # Internacionalizace (překlady)
USE_L10N = True  # Lokalizace formátů dat a čísel
USE_TZ = True  # Povolit podporu časových zón

# ------------------------------
# Statické a mediální soubory
# ------------------------------

# Statické soubory (CSS, JavaScript, obrázky)
STATIC_URL = '/static/'  # URL pro statické soubory
STATICFILES_DIRS = [BASE_DIR / 'static']  # Cesty ke statickým souborům
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Pro produkční nasazení

# Mediální soubory (nahrávané uživatelem)
MEDIA_URL = '/media/'  # URL pro mediální soubory
MEDIA_ROOT = BASE_DIR / 'media'  # Cesta pro ukládání mediálních souborů

# ------------------------------
# Nastavení šablon
# ------------------------------

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Hlavní složka šablon
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
# Nastavení e-mailu
# ------------------------------

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # SMTP server pro e-maily
EMAIL_PORT = 587  # Port pro SMTP
EMAIL_USE_TLS = True  # Použití šifrování
EMAIL_HOST_USER = os.getenv('DJANGO_EMAIL_HOST_USER', 'your_email@gmail.com')  # Nastavit vlastní e-mail
EMAIL_HOST_PASSWORD = os.getenv('DJANGO_EMAIL_HOST_PASSWORD', 'your_password')  # Nastavit heslo k e-mailu

# ------------------------------
# Protokolování
# ------------------------------

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',  # Zobrazování logů v konzoli
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG' if DEBUG else 'ERROR',
    },
}

# ------------------------------
# Další nastavení
# ------------------------------

# Ochrana proti XSS útokům
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# Maximální velikost nahrávaného souboru (v bajtech)
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5 MB

