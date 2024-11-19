"""
WSGI konfigurace pro projekt HMS.

Tento soubor slouží jako rozhraní mezi webovým serverem (např. Apache, Nginx)
a Django aplikací. Poskytuje modulovou proměnnou `application`, která je
vstupním bodem pro WSGI servery.

Více informací:
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

# Nastavení výchozího prostředí pro konfiguraci Django
# Určuje, který soubor nastavení se má použít pro tento projekt
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HMS.settings')

# Inicializace a získání WSGI aplikace
# Tato proměnná `application` slouží jako vstupní bod pro WSGI servery
application = get_wsgi_application()