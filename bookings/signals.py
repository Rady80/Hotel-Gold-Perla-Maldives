from django.db import connection
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Booking  # Importujeme model Booking

@receiver(post_migrate)
def create_default_bookings(sender, **kwargs):
    """
    Funkce, která se spustí po každé migraci a vytváří výchozí rezervace,
    pokud v databázi žádné rezervace neexistují.
    """
    # Zkontroluj, zda tabulka existuje
    if 'bookings_booking' in connection.introspection.table_names():
        # Kontrola, zda tabulka 'Booking' není prázdná
        if not Booking.objects.exists():
            # Vytvoření výchozích rezervací
            Booking.objects.create(guest_name="Default Guest", room_number=101, start_date="2024-12-01", end_date="2024-12-02", status="Confirmed")
            Booking.objects.create(guest_name="Default Guest", room_number=102, start_date="2024-12-02", end_date="2024-12-03", status="Confirmed")
            Booking.objects.create(guest_name="Default Guest", room_number=103, start_date="2024-12-03", end_date="2024-12-04", status="Confirmed")
            print("Výchozí rezervace byly vytvořeny.")  # Výpis do konzole pro ověření

