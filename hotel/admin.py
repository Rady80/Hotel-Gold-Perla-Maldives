from django.contrib import admin
from .models import (
    Announcement, Event, EventAttendees, Bills, FoodMenu, Report, Storage
)


# Registrace modelu Announcement
@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_created')  # Zobrazené sloupce
    search_fields = ('title', 'description')  # Vyhledávací pole
    list_filter = ('date_created',)  # Filtry na postranním panelu
    ordering = ('-date_created',)  # Výchozí řazení


# Registrace modelu Event
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'location')
    search_fields = ('name', 'location')
    list_filter = ('date',)
    ordering = ('-date',)


# Registrace modelu EventAttendees
@admin.register(EventAttendees)
class EventAttendeesAdmin(admin.ModelAdmin):
    list_display = ('event', 'guest')
    search_fields = ('event__name', 'guest__user__username')
    list_filter = ('event',)


# Registrace modelu Bills
@admin.register(Bills)
class BillsAdmin(admin.ModelAdmin):
    list_display = ('guest', 'amount', 'date_created')
    search_fields = ('guest__user__username', 'amount')
    list_filter = ('date_created',)
    ordering = ('-date_created',)


# Registrace modelu FoodMenu
@admin.register(FoodMenu)
class FoodMenuAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'availability')
    search_fields = ('name',)
    list_filter = ('availability',)
    ordering = ('name',)


# Registrace modelu Report
@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_created')
    search_fields = ('title', 'description')
    list_filter = ('date_created',)
    ordering = ('-date_created',)


# Registrace modelu Storage
@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin):
    list_display = ('item_name', 'quantity', 'date_added')
    search_fields = ('item_name',)
    list_filter = ('date_added',)
    ordering = ('-date_added',)