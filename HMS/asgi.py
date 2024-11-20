"""
ASGI konfigurace pro projekt HMS.

Tento soubor konfiguruje ASGI aplikaci pro Django.
Poskytuje modulovou proměnnou `application`, která slouží jako vstupní bod pro ASGI servery,
například při použití uvicorn nebo Daphne.

Více informací naleznete na:
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application

# ------------------------------
# Nastavení prostředí
# ------------------------------
# Nastavuje výchozí konfiguraci nastavení Django.
# Určuje, který soubor nastavení (`settings.py`) se má použít.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HMS.settings')

# ------------------------------
# Inicializace ASGI aplikace
# ------------------------------
# Získá a inicializuje ASGI aplikaci, která slouží jako spojení mezi
# ASGI serverem a Django aplikací.
application = get_asgi_application()

# ------------------------------
# Popis
# ------------------------------
# ASGI (Asynchronous Server Gateway Interface) je standardní rozhraní pro
# provozování asynchronních aplikací. Tento soubor zajišťuje, že vaše Django aplikace
# může být nasazena na ASGI serveru, například uvicorn nebo Daphne.

# Tato konfigurace umožňuje spuštění aplikace jak v synchronním, tak v asynchronním režimu.



