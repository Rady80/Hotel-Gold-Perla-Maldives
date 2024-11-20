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
        ('King', 'Královský'),
        ('Luxury', 'Luxusní'),
        ('Normal', 'Standardní'),
        ('Economic', 'Ekonomický'),
    )
    ROOM_STATUS = (
        ('Available', 'Dostupné'),
        ('Occupied', 'Obsazené'),
        ('Maintenance', 'Údržba'),
    )

    number = models.IntegerField(primary_key=True, verbose_name="Číslo pokoje")
    capacity = models.PositiveSmallIntegerField(verbose_name="Kapacita pokoje")
    numberOfBeds = models.PositiveSmallIntegerField(verbose_name="Počet postelí")
    roomType = models.CharField(max_length=20, choices=ROOM_TYPES, verbose_name="Typ pokoje")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Cena za noc")
    statusStartDate = models.DateField(null=True, blank=True, verbose_name="Začátek stavu pokoje")
    statusEndDate = models.DateField(null=True, blank=True, verbose_name="Konec stavu pokoje")
    name = models.CharField(max_length=100, verbose_name="Název pokoje")
    description = models.TextField(null=True, blank=True, verbose_name="Popis pokoje")
    status = models.CharField(
        max_length=20,
        choices=ROOM_STATUS,
        verbose_name="Stav pokoje",
        default='Available'
    )

    def __str__(self):
        return f"{self.name} (Číslo: {self.number})"


# ------------------------------
# Model pro obrázky pokojů
# ------------------------------
class RoomImage(models.Model):
    """
    Model pro správu obrázků přidružených k pokojům.
    """
    room = models.ForeignKey(Room, related_name='images', on_delete=models.CASCADE, verbose_name="Pokoj")
    image = models.ImageField(upload_to='room_images/', verbose_name="Obrázek pokoje")
    caption = models.CharField(max_length=255, blank=True, null=True, verbose_name="Popisek obrázku")

    def __str__(self):
        return f"Obrázek pokoje: {self.room.name}"


# ------------------------------
# Model pro rezervace
# ------------------------------
class Booking(models.Model):
    """
    Model pro správu rezervací pokojů.
    """
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name="Pokoj")
    guest = models.ForeignKey(Guest, null=True, on_delete=models.CASCADE, verbose_name="Host")
    dateOfReservation = models.DateField(default=timezone.now, verbose_name="Datum vytvoření rezervace")
    startDate = models.DateField(verbose_name="Začátek pobytu")
    endDate = models.DateField(verbose_name="Konec pobytu")
    STATUS_CHOICES = [
        ('Active', 'Aktivní'),
        ('Cancelled', 'Zrušeno'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active', verbose_name="Stav rezervace")

    def numOfDep(self):
        """
        Vrací počet závislých osob u této rezervace.
        """
        return Dependees.objects.filter(booking=self).count()

    def __str__(self):
        return f"Rezervace: Pokoj {self.room} pro hosta {self.guest}"


# ------------------------------
# Model pro závislé osoby
# ------------------------------
class Dependees(models.Model):
    """
    Model pro správu závislých osob přidružených k rezervacím.
    """
    booking = models.ForeignKey(Booking, null=True, on_delete=models.CASCADE, verbose_name="Rezervace")
    name = models.CharField(max_length=100, verbose_name="Jméno osoby")
    relation = models.CharField(max_length=50, null=True, blank=True, verbose_name="Vztah k hostovi")

    def __str__(self):
        return f"{self.name} (Rezervace: {self.booking})"


# ------------------------------
# Model pro refundace
# ------------------------------
class Refund(models.Model):
    """
    Model pro správu refundací spojených s rezervacemi.
    """
    guest = models.ForeignKey(Guest, null=True, on_delete=models.CASCADE, verbose_name="Host")
    reservation = models.ForeignKey(Booking, on_delete=models.CASCADE, verbose_name="Rezervace")
    reason = models.TextField(verbose_name="Důvod refundace")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Částka refundace")
    STATUS_CHOICES = [
        ('Pending', 'Nevyřízeno'),
        ('Processed', 'Zpracováno'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending', verbose_name="Stav refundace")

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
    curBooking = models.ForeignKey(Booking, null=True, on_delete=models.CASCADE, verbose_name="Rezervace")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name="Pokoj")
    createdDate = models.DateField(default=timezone.now, verbose_name="Datum vytvoření služby")
    servicesType = models.CharField(max_length=20, choices=SERVICES_TYPES, verbose_name="Typ služby")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Cena služby")
    description = models.TextField(null=True, blank=True, verbose_name="Popis služby")

    def __str__(self):
        return f"Služba: {self.servicesType} pro pokoj {self.room}"


# ------------------------------
# Model pro produkty
# ------------------------------
class Product(models.Model):
    """
    Model pro správu produktů.
    """
    name = models.CharField(max_length=100, verbose_name="Název produktu")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Cena produktu")

    def __str__(self):
        return self.name