from django.test import TestCase
from django.contrib.auth.models import User
from hotel.models import Guest, Employee, Event, Bills, Storage


class GuestModelTest(TestCase):
    """
    Testy pro model Guest.
    """
    def setUp(self):
        """
        Příprava testovacích dat: vytvoření uživatele a hosta.
        """
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="password123")
        self.guest = Guest.objects.create(user=self.user, phoneNumber="+123456789")

    def test_guest_creation(self):
        """
        Ověření správného vytvoření hosta.
        """
        self.assertEqual(self.guest.user.username, "testuser")
        self.assertEqual(self.guest.phoneNumber, "+123456789")

    def test_guest_str_method(self):
        """
        Ověření správného fungování metody __str__ u modelu Guest.
        """
        self.assertEqual(str(self.guest), "testuser (Guest)")


class EmployeeModelTest(TestCase):
    """
    Testy pro model Employee.
    """
    def setUp(self):
        """
        Příprava testovacích dat: vytvoření uživatele a zaměstnance.
        """
        self.user = User.objects.create_user(username="employee1", email="employee@example.com", password="password123")
        self.employee = Employee.objects.create(user=self.user, phoneNumber="+987654321", salary=5000.0)

    def test_employee_creation(self):
        """
        Ověření správného vytvoření zaměstnance.
        """
        self.assertEqual(self.employee.user.username, "employee1")
        self.assertEqual(self.employee.phoneNumber, "+987654321")
        self.assertEqual(self.employee.salary, 5000.0)

    def test_employee_str_method(self):
        """
        Ověření správného fungování metody __str__ u modelu Employee.
        """
        self.assertEqual(str(self.employee), "employee1 (Employee)")


class EventModelTest(TestCase):
    """
    Testy pro model Event.
    """
    def setUp(self):
        """
        Příprava testovacích dat: vytvoření události.
        """
        self.event = Event.objects.create(
            eventType="Conference",
            location="Main Hall",
            startDate="2024-01-01",
            endDate="2024-01-03",
            explanation="Annual business conference"
        )

    def test_event_creation(self):
        """
        Ověření správného vytvoření události.
        """
        self.assertEqual(self.event.eventType, "Conference")
        self.assertEqual(self.event.location, "Main Hall")
        self.assertEqual(str(self.event.startDate), "2024-01-01")
        self.assertEqual(self.event.explanation, "Annual business conference")

    def test_event_str_method(self):
        """
        Ověření správného fungování metody __str__ u modelu Event.
        """
        self.assertEqual(
            str(self.event),
            "Conference v Main Hall od 2024-01-01 do 2024-01-03"
        )


class BillsModelTest(TestCase):
    """
    Testy pro model Bills.
    """
    def setUp(self):
        """
        Příprava testovacích dat: vytvoření hosta a faktury.
        """
        self.user = User.objects.create_user(username="guest1", email="guest@example.com", password="password123")
        self.guest = Guest.objects.create(user=self.user, phoneNumber="+123456789")
        self.bill = Bills.objects.create(
            guest=self.guest,
            totalAmount=1200.50,
            summary="Room and meal charges",
            date="2024-01-01"
        )

    def test_bill_creation(self):
        """
        Ověření správného vytvoření faktury.
        """
        self.assertEqual(self.bill.guest.user.username, "guest1")
        self.assertEqual(self.bill.totalAmount, 1200.50)
        self.assertEqual(self.bill.summary, "Room and meal charges")

    def test_bill_str_method(self):
        """
        Ověření správného fungování metody __str__ u modelu Bills.
        """
        self.assertEqual(str(self.bill), "Faktura pro guest1 (1200.5 Kč)")


class StorageModelTest(TestCase):
    """
    Testy pro model Storage.
    """
    def setUp(self):
        """
        Příprava testovacích dat: vytvoření skladové položky.
        """
        self.item = Storage.objects.create(itemName="Toilet Paper", itemType="Cleaning", quantity=50)

    def test_storage_creation(self):
        """
        Ověření správného vytvoření skladové položky.
        """
        self.assertEqual(self.item.itemName, "Toilet Paper")
        self.assertEqual(self.item.itemType, "Cleaning")
        self.assertEqual(self.item.quantity, 50)

    def test_storage_str_method(self):
        """
        Ověření správného fungování metody __str__ u modelu Storage.
        """
        self.assertEqual(str(self.item), "Toilet Paper (50 ks)")