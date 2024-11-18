"""
ASGI konfigurace pro projekt HMS.

Tento soubor konfiguruje ASGI aplikaci pro Django. Poskytuje modulovou proměnnou 
`application`, která slouží jako vstupní bod pro ASGI servery.

Více informací naleznete na:
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application

# Nastavení výchozího prostředí pro konfiguraci Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HMS.settings')

# Inicializace a získání ASGI aplikace
application = get_asgi_application()



