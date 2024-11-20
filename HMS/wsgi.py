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

# ------------------------------
# Nastavení prostředí pro Django
# ------------------------------
# Určuje, který soubor nastavení se má použít pro tento projekt.
# Pokud používáte více prostředí (např. vývoj, testování, produkce),
# můžete zde dynamicky nastavovat různé konfigurační soubory.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HMS.settings')

# ------------------------------
# Inicializace WSGI aplikace
# ------------------------------
# Tato proměnná `application` slouží jako vstupní bod pro WSGI servery,
# které komunikují s vaší Django aplikací. Webový server (např. Apache)
# deleguje požadavky na tuto aplikaci.
application = get_wsgi_application()