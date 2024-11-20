from django.contrib import admin
from .models import Booking, Dependees, Refund, RoomServices, Room


# ------------------------------
# Administrace pokojů (Room)
# ------------------------------
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    """
    Konfigurace zobrazení pokojů v administraci.
    """
    list_display = ('name', 'price', 'roomType', 'status')  # Pole, která se zobrazí v seznamu
    search_fields = ('name', 'roomType')  # Vyhledávání podle názvu a typu pokoje
    list_filter = ('status', 'roomType')  # Filtry podle stavu a typu pokoje
    ordering = ('-price',)  # Výchozí řazení podle ceny sestupně


# ------------------------------
# Administrace rezervací (Booking)
# ------------------------------
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    """
    Konfigurace zobrazení rezervací v administraci.
    """
    list_display = ('room', 'guest', 'startDate', 'endDate', 'status')  # Pole, která se zobrazí v přehledu
    search_fields = ('room__name', 'guest__user__username')  # Možnost hledání podle pokoje a uživatele
    list_filter = ('startDate', 'endDate', 'status')  # Filtry podle dat a stavu rezervace
    ordering = ('-startDate',)  # Výchozí řazení podle začátku pobytu sestupně
    date_hierarchy = 'startDate'  # Navigace podle hierarchie dat

    fieldsets = (
        ("Základní informace", {
            'fields': ('room', 'guest', 'startDate', 'endDate', 'status')  # Sekce s hlavními poli
        }),
        ("Detaily rezervace", {
            'fields': ('notes',)  # Sekce s dodatečnými informacemi
        }),
    )


# ------------------------------
# Administrace závislých osob (Dependees)
# ------------------------------
@admin.register(Dependees)
class DependeesAdmin(admin.ModelAdmin):
    """
    Konfigurace zobrazení závislých osob v administraci.
    """
    list_display = ('booking', 'name', 'relation')  # Pole, která se zobrazí v přehledu
    search_fields = ('booking__room__name', 'name')  # Možnost hledání podle pokoje a jména závislé osoby
    list_filter = ('relation',)  # Filtry podle vztahu
    ordering = ('booking',)  # Výchozí řazení podle rezervace


# ------------------------------
# Administrace refundací (Refund)
# ------------------------------
@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
    """
    Konfigurace zobrazení refundací v administraci.
    """
    list_display = ('guest', 'reservation', 'reason', 'amount', 'status')  # Pole, která se zobrazí v přehledu
    search_fields = ('guest__user__username', 'reservation__room__name', 'reason')  # Možnost hledání podle uživatele, pokoje a důvodu
    list_filter = ('status',)  # Filtry podle stavu refundace
    ordering = ('-reservation__startDate',)  # Výchozí řazení podle začátku rezervace sestupně
    readonly_fields = ('status',)  # Pole, která jsou pouze pro čtení


# ------------------------------
# Administrace služeb pokojů (RoomServices)
# ------------------------------
@admin.register(RoomServices)
class RoomServicesAdmin(admin.ModelAdmin):
    """
    Konfigurace zobrazení služeb pokojů v administraci.
    """
    list_display = ('room', 'curBooking', 'servicesType', 'createdDate', 'price')  # Pole, která se zobrazí v přehledu
    search_fields = ('room__name', 'curBooking__guest__user__username', 'servicesType')  # Možnost hledání podle pokoje, uživatele a typu služby
    list_filter = ('servicesType', 'createdDate')  # Filtry podle typu služby a data vytvoření
    ordering = ('-createdDate',)  # Výchozí řazení podle data vytvoření sestupně

    fieldsets = (
        ("Základní informace", {
            'fields': ('room', 'curBooking', 'servicesType', 'price')  # Sekce s hlavními poli
        }),
        ("Detaily služby", {
            'fields': ('description', 'createdDate')  # Sekce s dodatečnými informacemi
        }),
    )