from django.contrib import admin
from .models import Announcement, Event, EventAttendees, Bill, FoodMenu, Report, Refund, Room, Storage

# ------------------------------
# Administrace oznámení (Announcement)
# ------------------------------
@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    """
    Konfigurace zobrazení oznámení v administraci.
    """
    list_display = ('title', 'content', 'date_created')  # Zobrazené sloupce
    search_fields = ('title', 'content')  # Vyhledávání podle nadpisu a obsahu
    list_filter = ('date_created',)  # Filtrování podle data vytvoření
    ordering = ('-date_created',)  # Seřazení od nejnovějších


# ------------------------------
# Administrace událostí (Event)
# ------------------------------
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """
    Konfigurace zobrazení událostí v administraci.
    """
    list_display = ('title', 'event_type', 'location', 'start_date', 'end_date')  # Zobrazené sloupce
    search_fields = ('title', 'event_type', 'location')  # Vyhledávání podle názvu, typu a místa
    list_filter = ('event_type', 'start_date', 'end_date')  # Filtrování podle typu a dat
    ordering = ('-start_date',)  # Seřazení od nejnovějších událostí


# ------------------------------
# Administrace účastníků událostí (EventAttendees)
# ------------------------------
@admin.register(EventAttendees)
class EventAttendeesAdmin(admin.ModelAdmin):
    """
    Konfigurace zobrazení účastníků událostí v administraci.
    """
    list_display = ('event', 'guest', 'number_of_dependents')  # Zobrazené sloupce
    search_fields = ('event__title', 'guest__user__username')  # Vyhledávání podle názvu události a jména hosta
    list_filter = ('event',)  # Filtrování podle události


# ------------------------------
# Administrace faktur (Bill)
# ------------------------------
@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    """
    Konfigurace zobrazení faktur v administraci.
    """
    list_display = ('guest', 'total_amount', 'date_created')  # Zobrazené sloupce
    search_fields = ('guest__user__username', 'summary')  # Vyhledávání podle hosta a souhrnu
    list_filter = ('date_created', 'guest')  # Filtrování podle data a hosta
    ordering = ('-date_created',)  # Seřazení od nejnovějších faktur


# ------------------------------
# Administrace jídelního menu (FoodMenu)
# ------------------------------
@admin.register(FoodMenu)
class FoodMenuAdmin(admin.ModelAdmin):
    """
    Konfigurace zobrazení jídelního menu v administraci.
    """
    list_display = ('name', 'price', 'category', 'created_at')  # Zobrazené sloupce
    search_fields = ('name', 'description')  # Vyhledávání podle názvu a popisu
    list_filter = ('category', 'created_at')  # Filtrování podle kategorie a data vytvoření
    ordering = ('-created_at',)  # Seřazení od nejnovějších položek


# ------------------------------
# Administrace reportů (Report)
# ------------------------------
@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    """
    Konfigurace zobrazení reportů v administraci.
    """
    list_display = ('date_created', 'content')  # Zobrazené sloupce
    search_fields = ('content',)  # Vyhledávání podle obsahu
    list_filter = ('date_created',)  # Filtrování podle data vytvoření
    ordering = ('-date_created',)  # Seřazení od nejnovějších reportů


# ------------------------------
# Administrace refundací (Refund)
# ------------------------------
@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
    """
    Konfigurace zobrazení refundací v administraci.
    """
    list_display = ('guest', 'reservation', 'amount', 'status')  # Zobrazené sloupce
    search_fields = ('guest__user__username', 'reservation__id', 'amount')  # Vyhledávání podle hosta a rezervace
    list_filter = ('status', 'date_created')  # Filtrování podle stavu a data
    ordering = ('-date_created',)  # Seřazení od nejnovějších refundací


# ------------------------------
# Administrace pokojů (Room)
# ------------------------------
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    """
    Konfigurace zobrazení pokojů v administraci.
    """
    list_display = ('room_number', 'room_type', 'capacity', 'price_per_night', 'is_available')  # Zobrazené sloupce
    search_fields = ('room_number', 'room_type')  # Vyhledávání podle čísla a typu pokoje
    list_filter = ('room_type', 'is_available')  # Filtrování podle typu a dostupnosti
    ordering = ('room_number',)  # Seřazení podle čísla pokoje


# ------------------------------
# Administrace skladu (Storage)
# ------------------------------
@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin):
    """
    Konfigurace zobrazení skladu v administraci.
    """
    list_display = ('item_name', 'quantity', 'last_updated')  # Zobrazené sloupce
    search_fields = ('item_name',)  # Vyhledávání podle názvu položky
    list_filter = ('last_updated',)  # Filtrování podle data poslední aktualizace
    ordering = ('item_name',)  # Seřazení podle názvu položky