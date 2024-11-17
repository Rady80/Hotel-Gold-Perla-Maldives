"""
WSGI config for HMS project.

This file configures the WSGI application for Django. It exposes the WSGI callable
as a module-level variable named `application`.

For more information on this file, see:
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

# Nastavení výchozího prostředí pro Django aplikaci
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HMS.settings')

# Získání WSGI aplikace
application = get_wsgi_application()