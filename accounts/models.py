from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
from django.apps import apps  # Lazy loading modelů


# ------------------------------
# Model pro hosty (Guest)
# ------------------------------
class Guest(models.Model):
    """
    Model pro hosty.
    Host je propojen s uživatelem (User) a obsahuje informace o telefonním čísle,
    jméně, datu příjezdu a odjezdu. Obsahuje také metody pro výpočet statistik hosta.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='accounts_guest',  # Unikátní název relace
        verbose_name="Uživatel"
    )
    phoneNumber = PhoneNumberField(unique=True, verbose_name="Telefonní číslo")
    name = models.CharField(max_length=255, verbose_name="Jméno")
    check_in_date = models.DateField(verbose_name="Datum příjezdu")
    check_out_date = models.DateField(verbose_name="Datum odjezdu")

    @property
    def num_of_days(self):
        """
        Vrací počet dní pobytu hosta.
        """
        return (self.check_out_date - self.check_in_date).days

    def __str__(self):
        return f"{self.user.username} (Host)"

    def num_of_bookings(self):
        """
        Vrací počet rezervací spojených s hostem.
        """
        Booking = apps.get_model('hotel', 'Booking')  # Lazy loading modelu Booking
        return Booking.objects.filter(guest=self).count()

    def total_booking_days(self):
        """
        Vrací celkový počet dní ze všech rezervací hosta.
        """
        Booking = apps.get_model('hotel', 'Booking')  # Lazy loading modelu Booking
        bookings = Booking.objects.filter(guest=self)
        return sum((booking.endDate - booking.startDate).days for booking in bookings)

    def last_booking_days(self):
        """
        Vrací počet dní poslední rezervace hosta.
        Pokud není žádná rezervace, vrací 0.
        """
        Booking = apps.get_model('hotel', 'Booking')  # Lazy loading modelu Booking
        last_booking = Booking.objects.filter(guest=self).last()
        return (
            (last_booking.endDate - last_booking.startDate).days
            if last_booking
            else 0
        )

    def current_room(self):
        """
        Vrací číslo pokoje poslední rezervace hosta.
        Pokud není žádná rezervace, vrací None.
        """
        Booking = apps.get_model('hotel', 'Booking')  # Lazy loading modelu Booking
        last_booking = Booking.objects.filter(guest=self).last()
        return last_booking.roomNumber if last_booking else None

    class Meta:
        verbose_name = "Host"
        verbose_name_plural = "Hosté"


# ------------------------------
# Model pro zaměstnance (Employee)
# ------------------------------
class Employee(models.Model):
    """
    Model pro zaměstnance.
    Zaměstnanec je propojen s uživatelem (User) a obsahuje informace o telefonním čísle a platu.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='accounts_employee',  # Unikátní název relace
        verbose_name="Uživatel"
    )
    phoneNumber = PhoneNumberField(unique=True, verbose_name="Telefonní číslo")
    salary = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Plat"
    )

    def __str__(self):
        return f"{self.user.username} (Zaměstnanec)"

    class Meta:
        verbose_name = "Zaměstnanec"
        verbose_name_plural = "Zaměstnanci"


# ------------------------------
# Model pro úkoly (Task)
# ------------------------------
class Task(models.Model):
    """
    Model pro úkoly.
    Každý úkol je propojen se zaměstnancem (Employee) a obsahuje informace o začátku a konci úkolu,
    a také jeho popis.
    """
    employee = models.ForeignKey(
        Employee,
        null=True,
        on_delete=models.CASCADE,
        verbose_name="Zaměstnanec"
    )
    startTime = models.DateTimeField(verbose_name="Začátek úkolu")
    endTime = models.DateTimeField(verbose_name="Konec úkolu")
    description = models.TextField(verbose_name="Popis úkolu")

    def __str__(self):
        return (
            f"Úkol pro {self.employee.user.username} "
            f"({self.startTime.strftime('%d.%m.%Y %H:%M')} - {self.endTime.strftime('%d.%m.%Y %H:%M')})"
        )

    class Meta:
        verbose_name = "Úkol"
        verbose_name_plural = "Úkoly"
        
class Event(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField()

    def __str__(self):
        return self.name
