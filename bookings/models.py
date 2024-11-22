from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField  # Pro telefonní číslo

# ------------------------------
# Model pro hosty (Guest)
# ------------------------------
class Guest(models.Model):
    """
    Model reprezentující hosta, který je propojen s uživatelem Django.
    Obsahuje informace o celém jménu a telefonním čísle.
    """
    user = models.OneToOneField(
        User,  # Tento model je propojen s uživatelem Django
        on_delete=models.CASCADE,  # Pokud uživatel bude smazán, smaže se i host
        related_name='hotel_guest',  # Možnost přístupu na hosta přes uživatele
        verbose_name="Uživatel"
    )
    full_name = models.CharField(max_length=255, verbose_name="Celé jméno")
    phone_number = PhoneNumberField(unique=True, verbose_name="Telefonní číslo")  # Telefonní číslo hosta

    def __str__(self):
        return self.full_name  # Vypíše celé jméno hosta

    class Meta:
        verbose_name = "Host"
        verbose_name_plural = "Hosté"
        
# ------------------------------
# Model pro pokoje (Room)
# ------------------------------
class Room(models.Model):
    """
    Model reprezentující pokoje v hotelu.
    Obsahuje informace o čísle pokoje, typu, kapacitě, ceně za noc a dostupnosti.
    """
    room_number = models.IntegerField(verbose_name="Číslo pokoje")
    room_type = models.CharField(max_length=50, verbose_name="Typ pokoje")
    capacity = models.IntegerField(verbose_name="Kapacita")  # Počet hostů, které pokoj pojme
    price_per_night = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Cena za noc"
    )
    is_available = models.BooleanField(default=True, verbose_name="Dostupnost")  # Je pokoj dostupný?

    def __str__(self):
        return f"Pokoj {self.room_number} - {self.room_type}"

    class Meta:
        verbose_name = "Pokoj"
        verbose_name_plural = "Pokoje"
        ordering = ['room_number']  # Seřazení pokojů podle čísla pokoje

# ------------------------------
# Model pro rezervace (Booking)
# ------------------------------
class Booking(models.Model):
    """
    Model pro rezervace pokojů.
    Uchovává informace o hostovi, pokoji, datu začátku a konce pobytu a stavu rezervace.
    """
    guest = models.ForeignKey(
        Guest,  # Host, který vytvořil rezervaci
        on_delete=models.CASCADE,
        verbose_name="Host"
    )
    room = models.ForeignKey(
        Room,  # Pokoj, který je rezervován
        on_delete=models.CASCADE,
        verbose_name="Pokoj"
    )
    start_date = models.DateField(verbose_name="Začátek pobytu")
    end_date = models.DateField(verbose_name="Konec pobytu")
    status = models.CharField(
        max_length=50,
        choices=[  # Možnosti stavu rezervace
            ('Čeká na potvrzení', 'Čeká na potvrzení'),
            ('Potvrzeno', 'Potvrzeno'),
            ('Zrušeno', 'Zrušeno'),
        ],
        default='Čeká na potvrzení',
        verbose_name="Stav rezervace"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Vytvořeno")  # Datum vytvoření rezervace
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Aktualizováno")  # Datum poslední aktualizace rezervace

    def __str__(self):
        return f"Rezervace {self.guest.full_name} - Pokoj {self.room.room_number}"

    class Meta:
        verbose_name = "Rezervace"
        verbose_name_plural = "Rezervace"
        ordering = ['-start_date']  # Seřazení rezervací podle data začátku pobytu, od nejnovějších
        
# ------------------------------
# Model pro detaily rezervací (ReservationDetails)
# ------------------------------
class ReservationDetails(models.Model):
    """
    Model pro detailní informace o rezervacích.
    Umožňuje zaznamenat hosta, typ pokoje, stav rezervace a další podrobnosti.
    """
    guest_name = models.CharField(max_length=100)
    room_number = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=50, default='Pending')  # Stav rezervace

    def __str__(self):
        return f'Rezervace {self.guest_name} - Pokoj {self.room_number}'

    class Meta:
        verbose_name = "Detail rezervace"
        verbose_name_plural = "Detaily rezervací"
        ordering = ['start_date']  # Seřazení podle data příjezdu
        
        