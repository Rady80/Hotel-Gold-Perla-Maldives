from django.contrib import admin
from .models import (
    Announcement, Event, EventAttendees, Bills, FoodMenu, Report, Storage
)


# ------------------------------
# Administrace oznámení (Announcement)
# ------------------------------
@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    """
    Konfigurace zobrazení oznámení v administraci.
    """
    list_display = ('content', 'sender', 'date')  # Zobrazené sloupce v přehledu
    search_fields = ('content', 'sender__username')  # Vyhledávací pole
    list_filter = ('date', 'sender')  # Filtry na bočním panelu
    ordering = ('-date',)  # Výchozí řazení (od nejnovějších oznámení)


# ------------------------------
# Administrace událostí (Event)
# ------------------------------
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """
    Konfigurace zobrazení událostí v administraci.
    """
    list_display = ('eventType', 'location', 'startDate', 'endDate')  # Zobrazené sloupce
    search_fields = ('eventType', 'location')  # Pole pro vyhledávání
    list_filter = ('startDate', 'endDate')  # Filtry na bočním panelu
    ordering = ('-startDate',)  # Výchozí řazení podle začátku události


# ------------------------------
# Administrace účastníků událostí (EventAttendees)
# ------------------------------
@admin.register(EventAttendees)
class EventAttendeesAdmin(admin.ModelAdmin):
    """
    Konfigurace zobrazení účastníků událostí v administraci.
    """
    list_display = ('event', 'guest', 'numberOfDependees')  # Zobrazené sloupce
    search_fields = ('event__eventType', 'guest__user__username')  # Vyhledávací pole
    list_filter = ('event',)  # Filtry na bočním panelu


# ------------------------------
# Administrace faktur (Bills)
# ------------------------------
@admin.register(Bills)
class BillsAdmin(admin.ModelAdmin):
    """
    Konfigurace zobrazení faktur v administraci.
    """
    list_display = ('guest', 'totalAmount', 'date')  # Zobrazené sloupce
    search_fields = ('guest__user__username', 'totalAmount')  # Vyhledávací pole
    list_filter = ('date',)  # Filtry na bočním panelu
    ordering = ('-date',)  # Výchozí řazení podle data (od nejnovějších)


# ------------------------------
# Administrace jídelního menu (FoodMenu)
# ------------------------------
@admin.register(FoodMenu)
class FoodMenuAdmin(admin.ModelAdmin):
    """
    Konfigurace zobrazení jídelního menu v administraci.
    """
    list_display = ('startDate', 'endDate', 'menuItems')  # Zobrazené sloupce
    search_fields = ('menuItems',)  # Vyhledávací pole
    ordering = ('-startDate',)  # Výchozí řazení podle začátku platnosti menu


# ------------------------------
# Administrace reportů (Report)
# ------------------------------
@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    """
    Konfigurace zobrazení reportů v administraci.
    """
    list_display = ('date', 'content')  # Zobrazené sloupce
    search_fields = ('content',)  # Vyhledávací pole
    list_filter = ('date',)  # Filtry na bočním panelu
    ordering = ('-date',)  # Výchozí řazení (od nejnovějších reportů)


# ------------------------------
# Administrace skladu (Storage)
# ------------------------------
@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin):
    """
    Konfigurace zobrazení skladu v administraci.
    """
    list_display = ('itemName', 'itemType', 'quantity')  # Zobrazené sloupce
    search_fields = ('itemName',)  # Vyhledávací pole
    list_filter = ('itemType',)  # Filtry na bočním panelu
    ordering = ('itemName',)  # Výchozí řazení podle názvu položky