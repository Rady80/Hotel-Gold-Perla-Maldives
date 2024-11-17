"""
ASGI config for HMS project.

This file configures the ASGI application for Django. It exposes the ASGI callable 
as a module-level variable named `application`.

For more information on this file, see:
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application

# Nastavení výchozího prostředí pro Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HMS.settings')

# Získání ASGI aplikace
application = get_asgi_application()