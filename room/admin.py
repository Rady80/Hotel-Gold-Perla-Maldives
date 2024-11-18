from django.contrib import admin
from .models import Booking, Dependees, Refund, RoomServices


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    """
    Konfigurace zobrazení rezervací v admin rozhraní.
    """
    list_display = ('roomNumber', 'guest', 'startDate', 'endDate', 'status')  # Pole pro přehled v adminu
    search_fields = ('roomNumber__number', 'guest__user__username', 'guest__name')  # Hledání podle pokoje a hosta
    list_filter = ('startDate', 'endDate', 'status')  # Filtrování podle dat a stavu rezervace
    ordering = ('-startDate',)  # Řazení podle začátku rezervace
    date_hierarchy = 'startDate'  # Hierarchie podle data

    fieldsets = (
        ("Základní informace", {
            'fields': ('roomNumber', 'guest', 'startDate', 'endDate', 'status')
        }),
        ("Detaily rezervace", {
            'fields': ('paymentMethod', 'totalPrice', 'notes'),
        }),
    )


@admin.register(Dependees)
class DependeesAdmin(admin.ModelAdmin):
    """
    Konfigurace zobrazení závislých osob v admin rozhraní.
    """
    list_display = ('booking', 'name', 'age', 'relation')  # Pole pro přehled
    search_fields = ('booking__roomNumber__number', 'name')  # Hledání podle rezervace a jména
    list_filter = ('relation',)  # Filtrování podle vztahu
    ordering = ('booking',)  # Řazení podle rezervace


@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
    """
    Konfigurace zobrazení refundací v admin rozhraní.
    """
    list_display = ('guest', 'reservation', 'reason', 'amount', 'status')  # Pole pro přehled
    search_fields = ('guest__user__username', 'reservation__roomNumber__number', 'reason')  # Hledání podle hosta a rezervace
    list_filter = ('guest', 'status', 'reason')  # Filtrování podle hosta, stavu a důvodu refundace
    ordering = ('-reservation__startDate',)  # Řazení podle začátku rezervace
    readonly_fields = ('processedDate',)  # Pole pouze pro čtení


@admin.register(RoomServices)
class RoomServicesAdmin(admin.ModelAdmin):
    """
    Konfigurace zobrazení služeb pokojů v admin rozhraní.
    """
    list_display = ('room', 'curBooking', 'servicesType', 'createdDate', 'price')  # Pole pro přehled
    search_fields = ('room__number', 'curBooking__guest__user__username', 'servicesType')  # Hledání podle pokoje a služby
    list_filter = ('servicesType', 'createdDate')  # Filtrování podle typu služby a data
    ordering = ('-createdDate',)  # Řazení podle data vytvoření

    fieldsets = (
        ("Základní informace", {
            'fields': ('room', 'curBooking', 'servicesType', 'price')
        }),
        ("Detaily služby", {
            'fields': ('description', 'createdDate'),
        }),
    )