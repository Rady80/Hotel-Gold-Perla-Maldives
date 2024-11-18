"""
WSGI konfigurace pro projekt HMS.

Tento soubor konfiguruje WSGI aplikaci pro Django. Poskytuje modulovou proměnnou
`application`, která slouží jako vstupní bod pro WSGI servery.

Více informací:
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

# Nastavení výchozího prostředí pro konfiguraci Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HMS.settings')

# Inicializace a získání WSGI aplikace
application = get_wsgi_application()