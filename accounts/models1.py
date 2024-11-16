from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Guest(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    phoneNumber = PhoneNumberField(unique=True)

    def __str__(self):
        return str(self.user) if self.user else "Anonymous Guest"

    def numOfDays(self):
        bookings = Booking.objects.filter(guest=self)
        return sum((b.endDate - b.startDate).days for b in bookings)

    def numOfLastBookingDays(self):
        try:
            last_booking = Booking.objects.filter(guest=self).last()
            return (last_booking.endDate - last_booking.startDate).days if last_booking else 0
        except:
            return 0

    def currentRoom(self):
        booking = Booking.objects.filter(guest=self).last()
        return booking.roomNumber if booking else None


class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    phoneNumber = PhoneNumberField(unique=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    employee = models.ForeignKey(Employee, null=True, on_delete=models.CASCADE)
    startTime = models.DateTimeField()
    endTime = models.DateTimeField()
    description = models.TextField()

    def clean(self):
        if self.startTime >= self.endTime:
            raise ValidationError("Start time must be before end time.")

    def __str__(self):
        return f"Task for {self.employee.name if self.employee else 'No Employee'}"