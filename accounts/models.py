from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User


class Guest(models.Model):
    """
    Model pro hosty.
    Každý host je propojen s uživatelem a obsahuje informace o telefonním čísle.
    """
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE, verbose_name="Uživatel")
    phoneNumber = PhoneNumberField(unique=True, verbose_name="Telefonní číslo")

    def __str__(self):
        return f"{self.user.username} (Host)"

    def numOfBooking(self):
        """
        Vrací počet rezervací hosta.
        """
        return Booking.objects.filter(guest=self).count()

    def numOfDays(self):
        """
        Vrací celkový počet dní všech rezervací hosta.
        """
        total_days = 0
        bookings = Booking.objects.filter(guest=self)
        for booking in bookings:
            day_count = booking.endDate - booking.startDate
            total_days += day_count.days
        return total_days

    def numOfLastBookingDays(self):
        """
        Vrací počet dní poslední rezervace hosta.
        Pokud není žádná rezervace, vrátí 0.
        """
        last_booking = Booking.objects.filter(guest=self).last()
        if last_booking:
            return (last_booking.endDate - last_booking.startDate).days
        return 0

    def currentRoom(self):
        """
        Vrací číslo pokoje z poslední rezervace hosta.
        Pokud není žádná rezervace, vrátí None.
        """
        last_booking = Booking.objects.filter(guest=self).last()
        return last_booking.roomNumber if last_booking else None

    class Meta:
        verbose_name = "Host"
        verbose_name_plural = "Hosté"


class Employee(models.Model):
    """
    Model pro zaměstnance.
    Každý zaměstnanec je propojen s uživatelem a obsahuje informace o telefonním čísle a platu.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phoneNumber = PhoneNumberField(unique=True, verbose_name="Telefonní číslo")
    salary = models.FloatField(verbose_name="Plat")
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Povolení prázdných hodnot

    def __str__(self):
        return f"{self.user.username} (Zaměstnanec)"

    class Meta:
        verbose_name = "Zaměstnanec"
        verbose_name_plural = "Zaměstnanci"


class Task(models.Model):
    """
    Model pro úkoly.
    Každý úkol je propojen se zaměstnancem a obsahuje informace o čase začátku a konce, 
    a také popis úkolu.
    """
    employee = models.ForeignKey(
        Employee, null=True, on_delete=models.CASCADE, verbose_name="Zaměstnanec"
    )
    startTime = models.DateTimeField(verbose_name="Začátek úkolu")
    endTime = models.DateTimeField(verbose_name="Konec úkolu")
    description = models.TextField(verbose_name="Popis úkolu")

    def __str__(self):
        return f"Úkol pro {self.employee.user.username} ({self.startTime.strftime('%d.%m.%Y %H:%M')} - {self.endTime.strftime('%d.%m.%Y %H:%M')})"

    class Meta:
        verbose_name = "Úkol"
        verbose_name_plural = "Úkoly"