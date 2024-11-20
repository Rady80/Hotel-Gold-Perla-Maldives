from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField

# ------------------------------
# Model pro hosty (Guest)
# ------------------------------
class Guest(models.Model):
    """
    Model pro hosty.
    Obsahuje informace o uživateli a telefonním čísle.
    """
    user = models.OneToOneField(
        'auth.User', null=True, on_delete=models.CASCADE, verbose_name="Uživatel"
    )
    phone_number = PhoneNumberField(unique=True, verbose_name="Telefonní číslo")

    def __str__(self):
        return f"{self.user.username} (Host)" if self.user else "Neznámý host"

    class Meta:
        verbose_name = "Host"
        verbose_name_plural = "Hosté"

# ------------------------------
# Model pro zaměstnance (Employee)
# ------------------------------
class Employee(models.Model):
    """
    Model pro zaměstnance.
    Obsahuje informace o uživateli, telefonním čísle a platu.
    """
    user = models.OneToOneField(
        'auth.User', on_delete=models.CASCADE, verbose_name="Uživatel"
    )
    phone_number = PhoneNumberField(unique=True, verbose_name="Telefonní číslo")
    salary = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Plat")

    def __str__(self):
        return f"{self.user.username} (Zaměstnanec)"

    class Meta:
        verbose_name = "Zaměstnanec"
        verbose_name_plural = "Zaměstnanci"

# ------------------------------
# Model pro pokoje (Room)
# ------------------------------
class Room(models.Model):
    """
    Model pro pokoje.
    """
    room_number = models.IntegerField(verbose_name="Číslo pokoje")
    room_type = models.CharField(max_length=50, verbose_name="Typ pokoje")
    capacity = models.IntegerField(verbose_name="Kapacita")
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Cena za noc")
    is_available = models.BooleanField(default=True, verbose_name="Dostupnost")

    def __str__(self):
        return f"Pokoj {self.room_number}"

    class Meta:
        verbose_name = "Pokoj"
        verbose_name_plural = "Pokoje"

# ------------------------------
# Model pro rezervace (Booking)
# ------------------------------
class Booking(models.Model):
    """
    Model pro rezervace.
    Obsahuje informace o hostovi, pokoji, datu začátku a konce rezervace.
    """
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE, verbose_name="Host")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name="Pokoj")
    start_date = models.DateField(verbose_name="Začátek pobytu")
    end_date = models.DateField(verbose_name="Konec pobytu")

    def __str__(self):
        return f"Rezervace: {self.guest} - Pokoj {self.room.room_number}"

    class Meta:
        verbose_name = "Rezervace"
        verbose_name_plural = "Rezervace"

# ------------------------------
# Model pro události (Event)
# ------------------------------
class Event(models.Model):
    """
    Model pro události v hotelu.
    """
    EVENT_TYPES = (
        ('Movie', 'Film'),
        ('Theater', 'Divadlo'),
        ('Conference', 'Konference'),
        ('Concert', 'Koncert'),
        ('Entertainment', 'Zábava'),
        ('Live Music', 'Živá hudba'),
    )

    title = models.CharField(max_length=200, verbose_name="Název události")
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES, verbose_name="Typ události")
    location = models.CharField(max_length=100, verbose_name="Místo konání")
    start_date = models.DateTimeField(verbose_name="Datum začátku")
    end_date = models.DateTimeField(verbose_name="Datum konce")
    description = models.TextField(null=True, blank=True, verbose_name="Popis události")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Událost"
        verbose_name_plural = "Události"

# ------------------------------
# Model pro účastníky událostí (EventAttendees)
# ------------------------------
class EventAttendees(models.Model):
    """
    Model pro účastníky událostí.
    """
    event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name="Událost")
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE, verbose_name="Host")
    number_of_dependents = models.IntegerField(default=0, verbose_name="Počet doprovodů")

    def __str__(self):
        return f"{self.guest} na {self.event}"

    class Meta:
        verbose_name = "Účastník události"
        verbose_name_plural = "Účastníci událostí"

# ------------------------------
# Model pro faktury (Bill)
# ------------------------------
class Bill(models.Model):
    """
    Model pro faktury hostů.
    """
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE, verbose_name="Host")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Celková částka")
    date_created = models.DateTimeField(default=timezone.now, verbose_name="Datum vystavení")

    def __str__(self):
        return f"Faktura: {self.guest} ({self.total_amount} Kč)"

    class Meta:
        verbose_name = "Faktura"
        verbose_name_plural = "Faktury"

# ------------------------------
# Model pro oznámení (Announcement)
# ------------------------------
class Announcement(models.Model):
    """
    Model pro oznámení.
    """
    title = models.CharField(max_length=200, verbose_name="Název oznámení")
    content = models.TextField(verbose_name="Obsah oznámení")
    sender = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name="Odesílatel")
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Datum vytvoření")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Oznámení"
        verbose_name_plural = "Oznámení"

# ------------------------------
# Model pro jídelní menu (FoodMenu)
# ------------------------------
class FoodMenu(models.Model):
    """
    Model pro jídelní menu.
    """
    name = models.CharField(max_length=255, verbose_name="Název jídla")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Cena")
    category = models.CharField(max_length=100, verbose_name="Kategorie")
    description = models.TextField(verbose_name="Popis", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Datum vytvoření")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Položka jídelního menu"
        verbose_name_plural = "Jídelní menu"

# ------------------------------
# Model pro reporty (Report)
# ------------------------------
class Report(models.Model):
    """
    Model pro správu reportů.
    """
    content = models.TextField(verbose_name="Obsah reportu")
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Datum vytvoření")

    def __str__(self):
        return f"Report {self.id} - {self.date_created}"

    class Meta:
        verbose_name = "Report"
        verbose_name_plural = "Reporty"
        ordering = ['-date_created']

# ------------------------------
# Model pro refundace (Refund)
# ------------------------------
class Refund(models.Model):
    """
    Model pro refundace hostů.
    """
    guest = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name="Host")
    reservation = models.CharField(max_length=255, verbose_name="Rezervace")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Částka")
    status = models.CharField(max_length=50, verbose_name="Stav refundace")
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Datum vytvoření")

    def __str__(self):
        return f"Refundace {self.id} - Host: {self.guest.username}"

    class Meta:
        verbose_name = "Refundace"
        verbose_name_plural = "Refundace"
        ordering = ['-date_created']

# ------------------------------
# Model pro skladové zásoby (Storage)
# ------------------------------
class Storage(models.Model):
    """
    Model pro skladové zásoby.
    """
    item_name = models.CharField(max_length=200, verbose_name="Název položky")
    quantity = models.IntegerField(verbose_name="Počet kusů skladem")
    last_updated = models.DateTimeField(auto_now=True, verbose_name="Datum poslední aktualizace")

    def __str__(self):
        return f"{self.item_name} ({self.quantity} ks)"

    class Meta:
        verbose_name = "Sklad"
        verbose_name_plural = "Sklady"