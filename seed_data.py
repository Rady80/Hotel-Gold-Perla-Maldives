import os
import django

# Nastavení Django prostředí
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HMS.settings')
django.setup()

from bookings.models import Booking

Booking.objects.create(description="Rezervace pokoje Standard", date="2024-12-01")
Booking.objects.create(description="Rezervace pokoje Deluxe", date="2024-12-02")
Booking.objects.create(description="Rezervace apartmánu", date="2024-12-03")

print("Data byla přidána!")