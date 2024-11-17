from django.contrib import admin
from .models import Booking, Dependees, Refund, RoomServices


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    """
    Konfigurace zobrazení rezervací v admin rozhraní.
    """
    list_display = ('roomNumber', 'guest', 'startDate', 'endDate')  # Správná pole z modelu Booking
    search_fields = ('roomNumber__number', 'guest__user__username')  # Hledání podle čísla pokoje a jména hosta
    list_filter = ('startDate', 'endDate')  # Filtrování podle data
    ordering = ('-startDate',)  # Řazení podle začátku rezervace


@admin.register(Dependees)
class DependeesAdmin(admin.ModelAdmin):
    """
    Konfigurace zobrazení závislých osob v admin rozhraní.
    """
    list_display = ('booking', 'name')  # Správná pole z modelu Dependees
    search_fields = ('booking__roomNumber__number', 'name')  # Hledání podle rezervace a jména
    ordering = ('booking',)  # Řazení podle rezervace


@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
    """
    Konfigurace zobrazení refundací v admin rozhraní.
    """
    list_display = ('guest', 'reservation', 'reason')  # Správná pole z modelu Refund
    search_fields = ('guest__user__username', 'reservation__roomNumber__number')  # Hledání podle hosta a rezervace
    list_filter = ('guest',)  # Filtrování podle hosta
    ordering = ('-reservation__startDate',)  # Řazení podle začátku rezervace


@admin.register(RoomServices)
class RoomServicesAdmin(admin.ModelAdmin):
    """
    Konfigurace zobrazení služeb pokojů v admin rozhraní.
    """
    list_display = ('room', 'curBooking', 'servicesType', 'createdDate', 'price')  # Správná pole z modelu RoomServices
    search_fields = ('room__number', 'curBooking__guest__user__username', 'servicesType')  # Hledání podle pokoje a služby
    list_filter = ('servicesType', 'createdDate')  # Filtrování podle typu služby a data
    ordering = ('-createdDate',)  # Řazení podle data vytvoření