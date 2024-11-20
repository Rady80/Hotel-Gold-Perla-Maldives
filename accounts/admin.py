from django.contrib import admin
from .models import Guest, Employee, Task

# ------------------------------
# Administrace modelu Guest (Host)
# ------------------------------
@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    """
    Administrace modelu Guest (Host).
    Poskytuje přehled a správu hostů s přizpůsobenými zobrazeními a akcemi.
    """
    # Sloupce zobrazené v seznamu hostů
    list_display = ('id', 'user', 'phoneNumber', 'num_of_bookings', 'num_of_days', 'user_date_joined')
    # Pole pro vyhledávání
    search_fields = ('user__username', 'user__email', 'phoneNumber')
    # Filtry v postranním panelu
    list_filter = ('user__date_joined',)
    # Výchozí řazení seznamu
    ordering = ('user__username',)
    # Pole pouze ke čtení
    readonly_fields = ('num_of_bookings', 'num_of_days', 'user_date_joined')

    def user_date_joined(self, obj):
        """
        Vrátí datum, kdy byl uživatel registrován.
        """
        return obj.user.date_joined
    user_date_joined.short_description = "Datum registrace"

    actions = ['mark_missing_phone_number']

    def mark_missing_phone_number(self, request, queryset):
        """
        Akce: Nastavit telefonní číslo na 'Neznámé', pokud chybí.
        """
        queryset.update(phoneNumber='Neznámé')
        self.message_user(request, "Telefonní číslo bylo nastaveno na 'Neznámé' u vybraných hostů.")
    mark_missing_phone_number.short_description = "Označit chybějící telefonní číslo"


# ------------------------------
# Administrace modelu Employee (Zaměstnanec)
# ------------------------------
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    """
    Administrace modelu Employee (Zaměstnanec).
    Poskytuje správu zaměstnanců s možností hledání a filtrování podle platu.
    """
    # Sloupce zobrazené v seznamu zaměstnanců
    list_display = ('id', 'user', 'phoneNumber', 'salary')
    # Pole pro vyhledávání
    search_fields = ('user__username', 'user__email', 'phoneNumber')
    # Filtry v postranním panelu
    list_filter = ('salary',)
    # Řazení podle jména uživatele
    ordering = ('user__username',)


# ------------------------------
# Administrace modelu Task (Úkol)
# ------------------------------
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """
    Administrace modelu Task (Úkol).
    Umožňuje správu úkolů přiřazených zaměstnancům s přizpůsobenými sloupci a filtry.
    """
    # Sloupce zobrazené v seznamu úkolů
    list_display = ('id', 'description', 'employee', 'startTime', 'endTime')
    # Pole pro vyhledávání
    search_fields = ('description', 'employee__user__username', 'employee__phoneNumber')
    # Filtry v postranním panelu
    list_filter = ('startTime', 'endTime')
    # Výchozí řazení
    ordering = ('-startTime',)