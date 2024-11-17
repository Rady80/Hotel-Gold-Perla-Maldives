from django.db import models
from django.utils import timezone
from accounts.models import Guest

# Model pro pokoje
class Room(models.Model):
    """
    Model pro správu pokojů.
    """
    ROOM_TYPES = (
        ('King', 'King'),
        ('Luxury', 'Luxury'),
        ('Normal', 'Normal'),
        ('Economic', 'Economic'),
    )
    number = models.IntegerField(primary_key=True, verbose_name="Číslo pokoje")  # Unikátní číslo pokoje
    capacity = models.SmallIntegerField(verbose_name="Kapacita")  # Kapacita pokoje
    numberOfBeds = models.SmallIntegerField(verbose_name="Počet postelí")  # Počet postelí
    roomType = models.CharField(max_length=20, choices=ROOM_TYPES, verbose_name="Typ pokoje")  # Typ pokoje
    price = models.FloatField(verbose_name="Cena za noc")  # Cena za noc
    statusStartDate = models.DateField(null=True, blank=True, verbose_name="Začátek rezervace")  # Začátek rezervace
    statusEndDate = models.DateField(null=True, blank=True, verbose_name="Konec rezervace")  # Konec rezervace
    name = models.CharField(max_length=100, verbose_name="Název pokoje")  # Název pokoje
    description = models.TextField(verbose_name="Popis pokoje")  # Popis pokoje
    room_number = models.CharField(max_length=10, verbose_name="Číslo pokoje", unique=True, null=True, blank=True)  # Číslo pokoje
    description = models.TextField(null=True, blank=True)  # Povolení prázdných hodnot
    status = models.CharField(
        max_length=20,
        choices=[('Available', 'Dostupné'), ('Occupied', 'Obsazené'), ('Maintenance', 'Údržba')],
        verbose_name="Stav pokoje",
        default='Available'
    )  # Stav pokoje

    def __str__(self):
        return f"{self.name} ({self.number})"


# Model pro obrázky pokojů
class RoomImage(models.Model):
    """
    Model pro správu obrázků pokojů.
    """
    room = models.ForeignKey(Room, related_name='images', on_delete=models.CASCADE, verbose_name="Pokoj")  # Odkaz na pokoj
    image = models.ImageField(upload_to='room_images/', verbose_name="Obrázek pokoje")  # Obrázek pokoje
    caption = models.CharField(max_length=255, blank=True, null=True, verbose_name="Popisek obrázku")  # Popisek obrázku

    def __str__(self):
        return f"Obrázek: {self.room.name}"


# Model pro rezervace
class Booking(models.Model):
    """
    Model pro správu rezervací.
    """
    roomNumber = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name="Pokoj")  # Odkaz na pokoj
    guest = models.ForeignKey(Guest, null=True, on_delete=models.CASCADE, verbose_name="Host")  # Odkaz na hosta
    dateOfReservation = models.DateField(default=timezone.now, verbose_name="Datum rezervace")  # Datum vytvoření rezervace
    startDate = models.DateField(verbose_name="Začátek pobytu")  # Začátek pobytu
    endDate = models.DateField(verbose_name="Konec pobytu")  # Konec pobytu

    def numOfDep(self):
        """
        Počet závislých osob u této rezervace.
        """
        return Dependees.objects.filter(booking=self).count()

    def __str__(self):
        return f"Rezervace: {self.roomNumber} pro {self.guest}"


# Model pro závislé osoby
class Dependees(models.Model):
    """
    Model pro správu závislých osob u rezervací.
    """
    booking = models.ForeignKey(Booking, null=True, on_delete=models.CASCADE, verbose_name="Rezervace")  # Odkaz na rezervaci
    name = models.CharField(max_length=100, verbose_name="Jméno osoby")  # Jméno závislé osoby

    def __str__(self):
        return f"{self.name} (Rezervace: {self.booking})"


# Model pro refundace
class Refund(models.Model):
    """
    Model pro správu refundací.
    """
    guest = models.ForeignKey(Guest, null=True, on_delete=models.CASCADE, verbose_name="Host")  # Odkaz na hosta
    reservation = models.ForeignKey(Booking, on_delete=models.CASCADE, verbose_name="Rezervace")  # Odkaz na rezervaci
    reason = models.TextField(verbose_name="Důvod refundace")  # Důvod refundace

    def __str__(self):
        return f"Refundace pro {self.guest}"


# Model pro služby pokojů
class RoomServices(models.Model):
    """
    Model pro správu služeb pokojů.
    """
    SERVICES_TYPES = (
        ('Food', 'Food'),
        ('Cleaning', 'Cleaning'),
        ('Technical', 'Technical'),
    )
    curBooking = models.ForeignKey(Booking, null=True, on_delete=models.CASCADE, verbose_name="Rezervace")  # Odkaz na rezervaci
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name="Pokoj")  # Odkaz na pokoj
    createdDate = models.DateField(default=timezone.now, verbose_name="Datum vytvoření")  # Datum vytvoření služby
    servicesType = models.CharField(max_length=20, choices=SERVICES_TYPES, verbose_name="Typ služby")  # Typ služby
    price = models.FloatField(verbose_name="Cena služby")  # Cena služby

    def __str__(self):
        return f"Služba: {self.servicesType} (Pokoj: {self.room})"
