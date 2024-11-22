from django.core.management.base import BaseCommand
from bookings.models import Booking

class Command(BaseCommand):
    help = 'Naplní model Booking ukázkovými daty'

    def handle(self, *args, **kwargs):
        Booking.objects.create(description="Rezervace pokoje Standard", date="2024-12-01")
        Booking.objects.create(description="Rezervace pokoje Deluxe", date="2024-12-02")
        Booking.objects.create(description="Rezervace apartmánu", date="2024-12-03")
        
        self.stdout.write("Data byla úspěšně přidána!")