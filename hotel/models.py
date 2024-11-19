from django.db import models
from django.utils import timezone
from accounts.models import Guest, Employee


# ------------------------------
# Model pro oznámení
# ------------------------------
class Announcement(models.Model):
    """
    Model pro oznámení, která jsou posílána uživatelům.
    """
    content = models.TextField(verbose_name="Obsah oznámení")  # Obsah oznámení
    sender = models.ForeignKey(Employee, null=True, on_delete=models.CASCADE, verbose_name="Odesílatel")  # Odesílatel
    date = models.DateField(default=timezone.now, verbose_name="Datum vytvoření")  # Datum vytvoření

    def __str__(self):
        return f"Oznámení od {self.sender.user.username if self.sender else 'Neznámý'} ({self.date})"

    class Meta:
        verbose_name = "Oznámení"
        verbose_name_plural = "Oznámení"


# ------------------------------
# Model pro události
# ------------------------------
class Event(models.Model):
    """
    Model pro správu různých událostí, jako jsou koncerty, konference apod.
    """
    EVENT_TYPES = (
        ('Movie', 'Film'),
        ('Theater', 'Divadlo'),
        ('Conference', 'Konference'),
        ('Concert', 'Koncert'),
        ('Entertainment', 'Zábava'),
        ('Live Music', 'Živá hudba'),
    )

    eventType = models.CharField(max_length=20, choices=EVENT_TYPES, verbose_name="Typ události")  # Typ události
    location = models.CharField(max_length=100, verbose_name="Místo konání")  # Místo konání
    startDate = models.DateField(verbose_name="Datum začátku")  # Datum začátku
    endDate = models.DateField(verbose_name="Datum konce")  # Datum konce
    explanation = models.TextField(verbose_name="Popis události")  # Popis události

    def __str__(self):
        return f"{self.eventType} v {self.location} od {self.startDate} do {self.endDate}"

    class Meta:
        verbose_name = "Událost"
        verbose_name_plural = "Události"


# ------------------------------
# Model pro účastníky událostí
# ------------------------------
class EventAttendees(models.Model):
    """
    Model pro účastníky událostí. Každý účastník je spojen s konkrétní událostí.
    """
    event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name="Událost")  # Událost
    guest = models.ForeignKey(Guest, null=True, on_delete=models.CASCADE, verbose_name="Host")  # Host
    numberOfDependees = models.IntegerField(default=0, verbose_name="Počet doprovodů")  # Počet doprovodů

    def __str__(self):
        return f"{self.guest.user.username if self.guest else 'Neznámý'} na {self.event.eventType}"

    class Meta:
        verbose_name = "Účastník události"
        verbose_name_plural = "Účastníci událostí"


# ------------------------------
# Model pro faktury
# ------------------------------
class Bills(models.Model):
    """
    Model pro faktury vydané hostům.
    """
    guest = models.ForeignKey(Guest, null=True, on_delete=models.CASCADE, verbose_name="Host")  # Host
    totalAmount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Celková částka")  # Celková částka
    summary = models.TextField(verbose_name="Souhrn")  # Souhrn položek
    date = models.DateTimeField(default=timezone.now, verbose_name="Datum vystavení")  # Datum vystavení faktury

    def __str__(self):
        return f"Faktura pro {self.guest.user.username if self.guest else 'Neznámý'} ({self.totalAmount} Kč)"

    class Meta:
        verbose_name = "Faktura"
        verbose_name_plural = "Faktury"


# ------------------------------
# Model pro jídelní menu
# ------------------------------
class FoodMenu(models.Model):
    """
    Model pro jídelní menu s položkami, které jsou k dispozici v určitém časovém období.
    """
    startDate = models.DateField(verbose_name="Datum začátku")  # Datum začátku platnosti menu
    endDate = models.DateField(verbose_name="Datum konce")  # Datum konce platnosti menu
    menuItems = models.TextField(verbose_name="Položky menu")  # Jídelní položky

    def __str__(self):
        return f"Menu od {self.startDate} do {self.endDate}"

    class Meta:
        verbose_name = "Jídelní menu"
        verbose_name_plural = "Jídelní menu"


# ------------------------------
# Model pro reporty
# ------------------------------
class Report(models.Model):
    """
    Model pro reporty související s provozem hotelu.
    """
    date = models.DateField(default=timezone.now, verbose_name="Datum")  # Datum reportu
    content = models.TextField(verbose_name="Obsah reportu")  # Obsah reportu

    def __str__(self):
        return f"Report z {self.date}"

    class Meta:
        verbose_name = "Report"
        verbose_name_plural = "Reporty"


# ------------------------------
# Model pro skladové položky
# ------------------------------
class Storage(models.Model):
    """
    Model pro skladové položky v hotelu (např. kuchyňské potřeby, čisticí prostředky).
    """
    ITEM_TYPES = (
        ('Kitchen', 'Kuchyňské potřeby'),
        ('Cleaning', 'Čisticí prostředky'),
        ('Electronic', 'Elektronika'),
        ('Textile', 'Textilie'),
        ('Other', 'Ostatní'),
    )
    itemName = models.CharField(max_length=100, verbose_name="Název položky")  # Název položky
    itemType = models.CharField(max_length=20, choices=ITEM_TYPES, verbose_name="Typ položky")  # Typ položky
    quantity = models.IntegerField(verbose_name="Množství")  # Množství na skladě

    def __str__(self):
        return f"{self.itemName} ({self.quantity} ks)"

    class Meta:
        verbose_name = "Skladová položka"
        verbose_name_plural = "Skladové položky"


# ------------------------------
# Model pro refundace
# ------------------------------
class Refund(models.Model):
    """
    Model pro správu refundací spojených s rezervacemi.
    """
    guest = models.ForeignKey(Guest, null=True, on_delete=models.CASCADE, verbose_name="Host")  # Odkaz na hosta
    reservation = models.ForeignKey('hotel.Booking', on_delete=models.CASCADE, verbose_name="Rezervace")  # Odkaz na rezervaci
    reason = models.TextField(verbose_name="Důvod refundace")  # Důvod refundace
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Částka refundace")  # Částka refundace

    def __str__(self):
        return f"Refundace pro {self.guest}"

    class Meta:
        verbose_name = "Refundace"
        verbose_name_plural = "Refundace"