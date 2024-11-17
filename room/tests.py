from django.test import TestCase
from .models import Room, Booking, Guest
from datetime import date

class RoomModelTest(TestCase):
    def setUp(self):
        """
        Vytvoření testovacích dat pro model Room.
        """
        self.room = Room.objects.create(
            number=101,
            capacity=2,
            numberOfBeds=2,
            roomType='Luxury',
            price=1500.0,
            name='Luxury Suite',
            description='Luxusní pokoj s výhledem na moře.'
        )

    def test_room_creation(self):
        """
        Testuje, zda je pokoj správně vytvořen.
        """
        self.assertEqual(self.room.name, 'Luxury Suite')
        self.assertEqual(self.room.capacity, 2)
        self.assertEqual(self.room.roomType, 'Luxury')

class BookingModelTest(TestCase):
    def setUp(self):
        """
        Vytvoření testovacích dat pro model Booking.
        """
        self.guest = Guest.objects.create(
            user=None, phoneNumber='+123456789'
        )
        self.room = Room.objects.create(
            number=101,
            capacity=2,
            numberOfBeds=2,
            roomType='Luxury',
            price=1500.0,
            name='Luxury Suite',
            description='Luxusní pokoj s výhledem na moře.'
        )
        self.booking = Booking.objects.create(
            roomNumber=self.room,
            guest=self.guest,
            startDate=date(2024, 11, 20),
            endDate=date(2024, 11, 25)
        )

    def test_booking_duration(self):
        """
        Testuje, zda je délka rezervace správně vypočítána.
        """
        duration = (self.booking.endDate - self.booking.startDate).days
        self.assertEqual(duration, 5)

class GuestModelTest(TestCase):
    def setUp(self):
        """
        Vytvoření testovacích dat pro model Guest.
        """
        self.guest = Guest.objects.create(
            user=None, phoneNumber='+123456789'
        )

    def test_guest_creation(self):
        """
        Testuje, zda je host správně vytvořen.
        """
        self.assertEqual(self.guest.phoneNumber, '+123456789')