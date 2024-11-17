from django.db import models
from django.utils import timezone
from accounts.models import Guest

# Model pro pokoje
class Room(models.Model):
    ROOM_TYPES = (
        ('King', 'King'),
        ('Luxury', 'Luxury'),
        ('Normal', 'Normal'),
        ('Economic', 'Economic'),
    )
    number = models.IntegerField(primary_key=True, verbose_name="Číslo pokoje")
    capacity = models.SmallIntegerField(verbose_name="Kapacita")
    numberOfBeds = models.SmallIntegerField(verbose_name="Počet postelí")
    roomType = models.CharField(max_length=20, choices=ROOM_TYPES, verbose_name="Typ pokoje")
    price = models.FloatField(verbose_name="Cena za noc")
    statusStartDate = models.DateField(null=True, blank=True, verbose_name="Začátek rezervace")
    statusEndDate = models.DateField(null=True, blank=True, verbose_name="Konec rezervace")
    name = models.CharField(max_length=100, verbose_name="Název pokoje")
    description = models.TextField(verbose_name="Popis pokoje")
    
    def __str__(self):
        return f"{self.name} ({self.number})"

# Model pro obrázky pokojů
class RoomImage(models.Model):
    room = models.ForeignKey(Room, related_name='images', on_delete=models.CASCADE, verbose_name="Pokoj")
    image = models.ImageField(upload_to='room_images/', verbose_name="Obrázek pokoje")
    caption = models.CharField(max_length=255, blank=True, null=True, verbose_name="Popisek obrázku")

    def __str__(self):
        return f"Obrázek: {self.room.name}"

# Model pro rezervace
class Booking(models.Model):
    roomNumber = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name="Pokoj")
    guest = models.ForeignKey(Guest, null=True, on_delete=models.CASCADE, verbose_name="Host")
    dateOfReservation = models.DateField(default=timezone.now, verbose_name="Datum rezervace")
    startDate = models.DateField(verbose_name="Začátek pobytu")
    endDate = models.DateField(verbose_name="Konec pobytu")

    def numOfDep(self):
        return Dependees.objects.filter(booking=self).count()

    def __str__(self):
        return f"Rezervace: {self.roomNumber} pro {self.guest}"

# Model pro závislé osoby
class Dependees(models.Model):
    booking = models.ForeignKey(Booking, null=True, on_delete=models.CASCADE, verbose_name="Rezervace")
    name = models.CharField(max_length=100, verbose_name="Jméno osoby")

    def __str__(self):
        return f"{self.name} (Rezervace: {self.booking})"

# Model pro refundace
class Refund(models.Model):
    guest = models.ForeignKey(Guest, null=True, on_delete=models.CASCADE, verbose_name="Host")
    reservation = models.ForeignKey(Booking, on_delete=models.CASCADE, verbose_name="Rezervace")
    reason = models.TextField(verbose_name="Důvod refundace")

    def __str__(self):
        return f"Refundace pro {self.guest}"

# Model pro služby pokojů
class RoomServices(models.Model):
    SERVICES_TYPES = (
        ('Food', 'Food'),
        ('Cleaning', 'Cleaning'),
        ('Technical', 'Technical'),
    )
    curBooking = models.ForeignKey(Booking, null=True, on_delete=models.CASCADE, verbose_name="Rezervace")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name="Pokoj")
    createdDate = models.DateField(default=timezone.now, verbose_name="Datum vytvoření")
    servicesType = models.CharField(max_length=20, choices=SERVICES_TYPES, verbose_name="Typ služby")
    price = models.FloatField(verbose_name="Cena služby")

    def __str__(self):
        return f"Služba: {self.servicesType} (Pokoj: {self.room})"