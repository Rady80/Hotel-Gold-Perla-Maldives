from django.contrib import admin
from .models import Guest, Room, Booking # Načítáme modely Guest, Room, Booking

class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'guest', 'room', 'start_date', 'end_date')  # Změň na správná pole z modelu Booking
    list_filter = ('start_date', 'end_date')
    search_fields = ('guest__full_name', 'room__room_number')



# Registrujeme modely pro správu přes Django Admin
admin.site.register(Guest)  # Hosty spravujeme v admin rozhraní
admin.site.register(Room)   # Pokoje spravujeme v admin rozhraní
admin.site.register(Booking)  # Rezervace spravujeme v admin rozhraní
