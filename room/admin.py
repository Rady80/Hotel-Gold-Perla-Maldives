from django.contrib import admin
from .models import Room, RoomImage, Booking, Dependees, RoomServices, Refund

# Inline model for RoomImage to enable adding images directly within the Room admin page
class RoomImageInline(admin.TabularInline):
    model = RoomImage
    extra = 1  # Number of additional empty forms for RoomImage
    verbose_name = "Room Image"
    verbose_name_plural = "Room Images"

# Admin configuration for Room model
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    inlines = [RoomImageInline]  # Adding RoomImage inline to Room admin
    list_display = ('name', 'description')  # Columns displayed in the admin list view
    search_fields = ('name', 'description')  # Search functionality for Room name and description
    list_filter = ('name',)  # Filter functionality in the sidebar
    ordering = ('name',)  # Default ordering of the Room list by name

# Register other models
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'guest', 'room', 'startDate', 'endDate')  # Display columns
    search_fields = ('guest__user__username', 'room__name')  # Enable search
    list_filter = ('startDate', 'endDate')  # Filter options for bookings
    ordering = ('-startDate',)  # Default ordering by most recent bookings

@admin.register(Dependees)
class DependeesAdmin(admin.ModelAdmin):
    list_display = ('guest', 'number')  # Display columns for Dependees
    search_fields = ('guest__user__username',)  # Enable search
    ordering = ('guest',)  # Default ordering by guest

@admin.register(RoomServices)
class RoomServicesAdmin(admin.ModelAdmin):
    list_display = ('room', 'serviceType', 'date')  # Display columns
    search_fields = ('room__name', 'serviceType')  # Enable search for room name and service type
    list_filter = ('date', 'serviceType')  # Filter options
    ordering = ('-date',)  # Default ordering by the latest service

@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
    list_display = ('booking', 'reason', 'amount', 'date')  # Display columns for Refund
    search_fields = ('booking__guest__user__username', 'reason')  # Enable search
    list_filter = ('date',)  # Filter options
    ordering = ('-date',)  # Default ordering by the latest refund