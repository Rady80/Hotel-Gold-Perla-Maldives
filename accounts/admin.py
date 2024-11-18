from django.contrib import admin
from .models import Guest, Employee, Task


# Vlastní nastavení administrace pro model Guest
@admin.register(Guest)  # Registrace modelu Guest v administraci
class GuestAdmin(admin.ModelAdmin):
    # Sloupce zobrazené v seznamu hostů
    list_display = ('id', 'user', 'phoneNumber', 'numOfBooking', 'numOfDays', 'user_date_joined')
    # Pole pro vyhledávání (lze hledat podle jména, emailu nebo telefonu)
    search_fields = ('user__username', 'user__email', 'phoneNumber')
    # Filtry v postranním panelu (např. podle data registrace)
    list_filter = ('user__date_joined',)
    # Výchozí řazení seznamu (např. podle uživatelského jména)
    ordering = ('user__username',)
    # Pole, která jsou pouze ke čtení (nelze je editovat)
    readonly_fields = ('numOfBooking', 'numOfDays', 'user_date_joined')

    # Vlastní metoda pro zobrazení data registrace uživatele
    def user_date_joined(self, obj):
        return obj.user.date_joined  # Vrátí datum, kdy se uživatel zaregistroval
    user_date_joined.short_description = "Datum registrace"  # Popisek sloupce v administraci

    # Akce dostupné v administraci pro tento model
    actions = ['mark_missing_phone_number']

    # Akce: Nastavit telefonní číslo na "Neznámé", pokud chybí
    def mark_missing_phone_number(self, request, queryset):
        # Aktualizace vybraných záznamů
        queryset.update(phoneNumber='Neznámé')
        # Zobrazení zprávy pro administrátora
        self.message_user(request, "Telefonní číslo bylo nastaveno na 'Neznámé' u vybraných hostů.")
    mark_missing_phone_number.short_description = "Označit chybějící telefonní číslo"


# Registrace modelu Employee s výchozím nastavením
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'position', 'phone')  # Sloupce v seznamu zaměstnanců
    search_fields = ('name', 'position')  # Pole pro vyhledávání
    list_filter = ('position',)  # Filtr podle pozice zaměstnance


# Registrace modelu Task s výchozím nastavením
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'assigned_to', 'due_date', 'status')  # Sloupce v seznamu úkolů
    search_fields = ('title', 'assigned_to__name')  # Pole pro vyhledávání (podle názvu nebo zaměstnance)
    list_filter = ('status', 'due_date')  # Filtr podle stavu a termínu úkolu
    ordering = ('-due_date',)  # Řazení podle nejnovějšího termínu