from django.contrib import admin
from .models import Booking, Dependees, Refund, RoomServices


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    """
    Konfigurace zobrazení rezervací v administraci.
    """
    list_display = ('roomNumber', 'guest', 'startDate', 'endDate', 'status')  # Pole zobrazená v přehledu rezervací
    search_fields = ('roomNumber__number', 'guest__user__username', 'guest__name')  # Možnosti vyhledávání
    list_filter = ('startDate', 'endDate', 'status')  # Možnosti filtrování
    ordering = ('-startDate',)  # Výchozí řazení (od nejnovější rezervace)
    date_hierarchy = 'startDate'  # Hierarchie zobrazení podle dat

    fieldsets = (
        ("Základní informace", {
            'fields': ('roomNumber', 'guest', 'startDate', 'endDate', 'status')  # Hlavní pole
        }),
        ("Detaily rezervace", {
            'fields': ('paymentMethod', 'totalPrice', 'notes'),  # Další informace
        }),
    )


@admin.register(Dependees)
class DependeesAdmin(admin.ModelAdmin):
    """
    Konfigurace zobrazení závislých osob (doprovod) v administraci.
    """
    list_display = ('booking', 'name', 'age', 'relation')  # Pole zobrazená v přehledu
    search_fields = ('booking__roomNumber__number', 'name')  # Možnosti vyhledávání
    list_filter = ('relation',)  # Možnosti filtrování podle vztahu
    ordering = ('booking',)  # Řazení podle rezervace


@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
    """
    Konfigurace zobrazení refundací v administraci.
    """
    list_display = ('guest', 'reservation', 'reason', 'amount', 'status')  # Pole zobrazená v přehledu
    search_fields = ('guest__user__username', 'reservation__roomNumber__number', 'reason')  # Možnosti vyhledávání
    list_filter = ('guest', 'status', 'reason')  # Možnosti filtrování
    ordering = ('-reservation__startDate',)  # Řazení podle začátku rezervace
    readonly_fields = ('processedDate',)  # Pole, která nelze měnit (pouze pro čtení)


@admin.register(RoomServices)
class RoomServicesAdmin(admin.ModelAdmin):
    """
    Konfigurace zobrazení služeb pokojů v administraci.
    """
    list_display = ('room', 'curBooking', 'servicesType', 'createdDate', 'price')  # Pole zobrazená v přehledu
    search_fields = ('room__number', 'curBooking__guest__user__username', 'servicesType')  # Možnosti vyhledávání
    list_filter = ('servicesType', 'createdDate')  # Možnosti filtrování
    ordering = ('-createdDate',)  # Řazení podle data vytvoření služby

    fieldsets = (
        ("Základní informace", {
            'fields': ('room', 'curBooking', 'servicesType', 'price')  # Hlavní pole
        }),
        ("Detaily služby", {
            'fields': ('description', 'createdDate'),  # Další informace
        }),
    )