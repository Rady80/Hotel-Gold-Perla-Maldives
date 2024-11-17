from django.contrib import admin
from .models import Guest, Employee, Task


# Vlastní nastavení administrace pro model Guest
@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    # Sloupce zobrazené v seznamu
    list_display = ('id', 'user', 'phoneNumber', 'numOfBooking', 'numOfDays', 'user_date_joined')
    
    # Vyhledávací pole
    search_fields = ('user__username', 'user__email', 'phoneNumber')
    
    # Filtry v postranním panelu
    list_filter = ('user__date_joined',)
    
    # Výchozí řazení
    ordering = ('user__username',)
    
    # Pole, která jsou pouze ke čtení
    readonly_fields = ('numOfBooking', 'numOfDays', 'user_date_joined')
    
    # Vlastní metoda pro datum registrace uživatele
    def user_date_joined(self, obj):
        return obj.user.date_joined
    user_date_joined.short_description = "Datum registrace"

    # Přizpůsobení akce "Chybí telefonní číslo"
    actions = ['mark_missing_phone_number']
    
    # Akce v admin panelu
    def mark_missing_phone_number(self, request, queryset):
        queryset.update(phoneNumber='Neznámé')
        self.message_user(request, "Telefonní číslo bylo nastaveno na 'Neznámé' u vybraných hostů.")
    mark_missing_phone_number.short_description = "Označit chybějící telefonní číslo"