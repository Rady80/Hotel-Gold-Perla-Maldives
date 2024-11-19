from django.test import TestCase
from .models import Room, Booking, Guest
from datetime import date


class RoomModelTest(TestCase):
    """
    Testy pro model Room.
    """
    def setUp(self):
        """
        Příprava testovacích dat pro model Room.
        """
        self.room = Room.objects.create(
            number=101,  # Číslo pokoje
            capacity=2,  # Kapacita pokoje
            numberOfBeds=2,  # Počet postelí
            roomType='Luxury',  # Typ pokoje
            price=1500.0,  # Cena za noc
            name='Luxury Suite',  # Název pokoje
            description='Luxusní pokoj s výhledem na moře.'  # Popis pokoje
        )

    def test_room_creation(self):
        """
        Testuje, zda je pokoj správně vytvořen a má správné atributy.
        """
        self.assertEqual(self.room.name, 'Luxury Suite')
        self.assertEqual(self.room.capacity, 2)
        self.assertEqual(self.room.roomType, 'Luxury')

    def test_room_string_representation(self):
        """
        Testuje textovou reprezentaci pokoje (metoda __str__).
        """
        self.assertEqual(str(self.room), "Luxury Suite (101)")


class BookingModelTest(TestCase):
    """
    Testy pro model Booking.
    """
    def setUp(self):
        """
        Příprava testovacích dat pro model Booking.
        """
        self.guest = Guest.objects.create(
            user=None,  # Uživatel (nevyžadován v tomto testu)
            phoneNumber='+123456789'  # Telefonní číslo hosta
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
            roomNumber=self.room,  # Odkaz na pokoj
            guest=self.guest,  # Odkaz na hosta
            startDate=date(2024, 11, 20),  # Začátek rezervace
            endDate=date(2024, 11, 25)  # Konec rezervace
        )

    def test_booking_duration(self):
        """
        Testuje správný výpočet délky rezervace.
        """
        duration = (self.booking.endDate - self.booking.startDate).days
        self.assertEqual(duration, 5)

    def test_booking_string_representation(self):
        """
        Testuje textovou reprezentaci rezervace (metoda __str__).
        """
        expected_str = f"Rezervace: {self.room} pro {self.guest}"
        self.assertEqual(str(self.booking), expected_str)


class GuestModelTest(TestCase):
    """
    Testy pro model Guest.
    """
    def setUp(self):
        """
        Příprava testovacích dat pro model Guest.
        """
        self.guest = Guest.objects.create(
            user=None,  # Uživatel (nevyžadován v tomto testu)
            phoneNumber='+123456789'  # Telefonní číslo hosta
        )

    def test_guest_creation(self):
        """
        Testuje, zda je host správně vytvořen a má správné atributy.
        """
        self.assertEqual(self.guest.phoneNumber, '+123456789')

    def test_guest_string_representation(self):
        """
        Testuje textovou reprezentaci hosta (metoda __str__).
        """
        expected_str = f"Host: {self.guest.phoneNumber}"
        self.assertEqual(str(self.guest), expected_str)