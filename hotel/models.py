from django.db import models
from django.utils import timezone
from accounts.models import Guest, Employee


class Announcement(models.Model):
    """
    Model pro oznámení.
    """
    content = models.TextField(verbose_name="Obsah oznámení")
    sender = models.ForeignKey(Employee, null=True, on_delete=models.CASCADE, verbose_name="Odesílatel")
    date = models.DateField(default=timezone.now, verbose_name="Datum vytvoření")

    def __str__(self):
        return f"Oznámení od {self.sender.user.username} ({self.date})"

    class Meta:
        verbose_name = "Oznámení"
        verbose_name_plural = "Oznámení"


class Event(models.Model):
    """
    Model pro události.
    """
    EVENT_TYPES = (
        ('Movie', 'Film'),
        ('Theater', 'Divadlo'),
        ('Conference', 'Konference'),
        ('Concert', 'Koncert'),
        ('Entertainment', 'Zábava'),
        ('Live Music', 'Živá hudba'),
    )

    eventType = models.CharField(max_length=20, choices=EVENT_TYPES, verbose_name="Typ události")
    location = models.CharField(max_length=100, verbose_name="Místo konání")
    startDate = models.DateField(verbose_name="Datum začátku")
    endDate = models.DateField(verbose_name="Datum konce")
    explanation = models.TextField(verbose_name="Popis události")

    def __str__(self):
        return f"{self.eventType} v {self.location} od {self.startDate} do {self.endDate}"

    class Meta:
        verbose_name = "Událost"
        verbose_name_plural = "Události"


class EventAttendees(models.Model):
    """
    Model pro účastníky událostí.
    """
    event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name="Událost")
    guest = models.ForeignKey(Guest, null=True, on_delete=models.CASCADE, verbose_name="Host")
    numberOfDependees = models.IntegerField(default=0, verbose_name="Počet doprovodů")

    def __str__(self):
        return f"{self.guest.user.username} na {self.event.eventType}"

    class Meta:
        verbose_name = "Účastník události"
        verbose_name_plural = "Účastníci událostí"


class Bills(models.Model):
    """
    Model pro faktury.
    """
    guest = models.ForeignKey(Guest, null=True, on_delete=models.CASCADE, verbose_name="Host")
    totalAmount = models.FloatField(verbose_name="Celková částka")
    summary = models.TextField(verbose_name="Souhrn")
    date = models.DateTimeField(default=timezone.now, verbose_name="Datum vystavení")

    def __str__(self):
        return f"Faktura pro {self.guest.user.username} ({self.totalAmount} Kč)"

    class Meta:
        verbose_name = "Faktura"
        verbose_name_plural = "Faktury"


class FoodMenu(models.Model):
    """
    Model pro jídelní menu.
    """
    startDate = models.DateField(verbose_name="Datum začátku")
    endDate = models.DateField(verbose_name="Datum konce")
    menuItems = models.TextField(verbose_name="Položky menu")

    def __str__(self):
        return f"Menu od {self.startDate} do {self.endDate}"

    class Meta:
        verbose_name = "Jídelní menu"
        verbose_name_plural = "Jídelní menu"


class Report(models.Model):
    """
    Model pro reporty.
    """
    date = models.DateField(default=timezone.now, verbose_name="Datum")
    content = models.TextField(verbose_name="Obsah reportu")

    def __str__(self):
        return f"Report z {self.date}"

    class Meta:
        verbose_name = "Report"
        verbose_name_plural = "Reporty"


class Storage(models.Model):
    """
    Model pro skladové položky.
    """
    ITEM_TYPES = (
        ('Kitchen', 'Kuchyňské potřeby'),
        ('Cleaning', 'Čisticí prostředky'),
        ('Electronic', 'Elektronika'),
        ('Textile', 'Textilie'),
        ('Other', 'Ostatní'),
    )
    itemName = models.CharField(max_length=100, verbose_name="Název položky")
    itemType = models.CharField(max_length=20, choices=ITEM_TYPES, verbose_name="Typ položky")
    quantity = models.IntegerField(verbose_name="Množství")  # Opraven překlep

    def __str__(self):
        return f"{self.itemName} ({self.quantity} ks)"

    class Meta:
        verbose_name = "Skladová položka"
        verbose_name_plural = "Skladové položky"