from django.shortcuts import render
from .models import Booking  # Změňte na správný model 'Booking'

def reservations(request):
    reservations = Booking.objects.all()  # Načtěte všechny rezervace
    return render(request, 'reservations.html', {'reservations': reservations})

# Funkce pro zobrazení seznamu rezervací
def bookings_list(request):
    bookings = Booking.objects.all()  # Načteme všechny rezervace
    return render(request, 'bookings/bookings_list.html', {'bookings': bookings})  # Předáme je šabloně