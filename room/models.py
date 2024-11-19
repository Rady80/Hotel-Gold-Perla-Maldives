from django.db import models
from django.utils import timezone
from accounts.models import Guest


# ------------------------------
# Model pro pokoje
# ------------------------------
class Room(models.Model):
    """
    Model pro správu pokojů v hotelu.
    """
    ROOM_TYPES = (
        ('King', 'King'),
        ('Luxury', 'Luxury'),
        ('Normal', 'Normal'),
        ('Economic', 'Economic'),
    )
    ROOM_STATUS = (
        ('Available', 'Dostupné'),
        ('Occupied', 'Obsazené'),
        ('Maintenance', 'Údržba'),
    )

    number = models.IntegerField(primary_key=True, verbose_name="Číslo pokoje")  # Unikátní číslo pokoje
    capacity = models.PositiveSmallIntegerField(verbose_name="Kapacita")  # Maximální kapacita pokoje
    numberOfBeds = models.PositiveSmallIntegerField(verbose_name="Počet postelí")  # Počet postelí v pokoji
    roomType = models.CharField(max_length=20, choices=ROOM_TYPES, verbose_name="Typ pokoje")  # Typ pokoje
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Cena za noc")  # Cena za noc
    statusStartDate = models.DateField(null=True, blank=True, verbose_name="Začátek rezervace")  # Datum od, kdy je pokoj rezervován
    statusEndDate = models.DateField(null=True, blank=True, verbose_name="Konec rezervace")  # Datum do, kdy je pokoj rezervován
    name = models.CharField(max_length=100, verbose_name="Název pokoje")  # Název pokoje
    description = models.TextField(null=True, blank=True, verbose_name="Popis pokoje")  # Popis pokoje
    status = models.CharField(
        max_length=20,
        choices=ROOM_STATUS,
        verbose_name="Stav pokoje",
        default='Available'
    )  # Stav pokoje

    def __str__(self):
        return f"{self.name} ({self.number})"


# ------------------------------
# Model pro obrázky pokojů
# ------------------------------
class RoomImage(models.Model):
    """
    Model pro správu obrázků přidružených k pokojům.
    """
    room = models.ForeignKey(Room, related_name='images', on_delete=models.CASCADE, verbose_name="Pokoj")  # Odkaz na pokoj
    image = models.ImageField(upload_to='room_images/', verbose_name="Obrázek pokoje")  # Obrázek pokoje
    caption = models.CharField(max_length=255, blank=True, null=True, verbose_name="Popisek obrázku")  # Popisek obrázku

    def __str__(self):
        return f"Obrázek: {self.room.name}"


# ------------------------------
# Model pro rezervace
# ------------------------------
class Booking(models.Model):
    """
    Model pro správu rezervací pokojů.
    """
    roomNumber = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name="Pokoj")  # Odkaz na pokoj
    guest = models.ForeignKey(Guest, null=True, on_delete=models.CASCADE, verbose_name="Host")  # Odkaz na hosta
    dateOfReservation = models.DateField(default=timezone.now, verbose_name="Datum rezervace")  # Datum vytvoření rezervace
    startDate = models.DateField(verbose_name="Začátek pobytu")  # Datum začátku pobytu
    endDate = models.DateField(verbose_name="Konec pobytu")  # Datum konce pobytu

    def numOfDep(self):
        """
        Vrací počet závislých osob u této rezervace.
        """
        return Dependees.objects.filter(booking=self).count()

    def __str__(self):
        return f"Rezervace: {self.roomNumber} pro {self.guest}"


# ------------------------------
# Model pro závislé osoby
# ------------------------------
class Dependees(models.Model):
    """
    Model pro správu závislých osob přidružených k rezervacím.
    """
    booking = models.ForeignKey(Booking, null=True, on_delete=models.CASCADE, verbose_name="Rezervace")  # Odkaz na rezervaci
    name = models.CharField(max_length=100, verbose_name="Jméno osoby")  # Jméno závislé osoby
    relation = models.CharField(max_length=50, null=True, blank=True, verbose_name="Vztah k hostovi")  # Vztah k hostovi

    def __str__(self):
        return f"{self.name} (Rezervace: {self.booking})"


# ------------------------------
# Model pro refundace
# ------------------------------
class Refund(models.Model):
    """
    Model pro správu refundací spojených s rezervacemi.
    """
    guest = models.ForeignKey(Guest, null=True, on_delete=models.CASCADE, verbose_name="Host")  # Odkaz na hosta
    reservation = models.ForeignKey(Booking, on_delete=models.CASCADE, verbose_name="Rezervace")  # Odkaz na rezervaci
    reason = models.TextField(verbose_name="Důvod refundace")  # Důvod refundace
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Částka refundace")  # Částka refundace

    def __str__(self):
        return f"Refundace pro {self.guest}"


# ------------------------------
# Model pro služby pokojů
# ------------------------------
class RoomServices(models.Model):
    """
    Model pro správu dodatečných služeb spojených s pokoji.
    """
    SERVICES_TYPES = (
        ('Food', 'Jídlo'),
        ('Cleaning', 'Úklid'),
        ('Technical', 'Technická podpora'),
    )
    curBooking = models.ForeignKey(Booking, null=True, on_delete=models.CASCADE, verbose_name="Rezervace")  # Odkaz na rezervaci
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name="Pokoj")  # Odkaz na pokoj
    createdDate = models.DateField(default=timezone.now, verbose_name="Datum vytvoření")  # Datum vytvoření služby
    servicesType = models.CharField(max_length=20, choices=SERVICES_TYPES, verbose_name="Typ služby")  # Typ služby
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Cena služby")  # Cena služby
    description = models.TextField(null=True, blank=True, verbose_name="Popis služby")  # Popis služby

    def __str__(self):
        return f"Služba: {self.servicesType} (Pokoj: {self.room})"