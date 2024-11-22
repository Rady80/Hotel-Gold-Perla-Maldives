from django.contrib import admin
from .models import Reservation

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('guest_name', 'room', 'check_in', 'check_out', 'status')
    list_filter = ('status', 'check_in', 'check_out')
    search_fields = ('guest_name', 'room')