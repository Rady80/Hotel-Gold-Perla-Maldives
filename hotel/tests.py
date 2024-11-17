from django.test import TestCase
from django.contrib.auth.models import User
from hotel.models import Guest, Employee, Event, Bills, Storage


class GuestModelTest(TestCase):
    def setUp(self):
        """
        Nastavení testovacích dat pro model Guest.
        """
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="password123")
        self.guest = Guest.objects.create(user=self.user, phoneNumber="+123456789")

    def test_guest_creation(self):
        """
        Test, zda byl host správně vytvořen.
        """
        self.assertEqual(self.guest.user.username, "testuser")
        self.assertEqual(self.guest.phoneNumber, "+123456789")

    def test_guest_str_method(self):
        """
        Test, zda metoda __str__ vrací očekávaný výsledek.
        """
        self.assertEqual(str(self.guest), "testuser (Guest)")


class EmployeeModelTest(TestCase):
    def setUp(self):
        """
        Nastavení testovacích dat pro model Employee.
        """
        self.user = User.objects.create_user(username="employee1", email="employee@example.com", password="password123")
        self.employee = Employee.objects.create(user=self.user, phoneNumber="+987654321", salary=5000.0)

    def test_employee_creation(self):
        """
        Test, zda byl zaměstnanec správně vytvořen.
        """
        self.assertEqual(self.employee.user.username, "employee1")
        self.assertEqual(self.employee.phoneNumber, "+987654321")
        self.assertEqual(self.employee.salary, 5000.0)

    def test_employee_str_method(self):
        """
        Test, zda metoda __str__ vrací očekávaný výsledek.
        """
        self.assertEqual(str(self.employee), "employee1 (Employee)")


class EventModelTest(TestCase):
    def setUp(self):
        """
        Nastavení testovacích dat pro model Event.
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
        Test, zda byla událost správně vytvořena.
        """
        self.assertEqual(self.event.eventType, "Conference")
        self.assertEqual(self.event.location, "Main Hall")
        self.assertEqual(str(self.event.startDate), "2024-01-01")
        self.assertEqual(self.event.explanation, "Annual business conference")

    def test_event_str_method(self):
        """
        Test, zda metoda __str__ vrací očekávaný výsledek.
        """
        self.assertEqual(
            str(self.event),
            "Conference v Main Hall od 2024-01-01 do 2024-01-03"
        )


class BillsModelTest(TestCase):
    def setUp(self):
        """
        Nastavení testovacích dat pro model Bills.
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
        Test, zda byla faktura správně vytvořena.
        """
        self.assertEqual(self.bill.guest.user.username, "guest1")
        self.assertEqual(self.bill.totalAmount, 1200.50)
        self.assertEqual(self.bill.summary, "Room and meal charges")

    def test_bill_str_method(self):
        """
        Test, zda metoda __str__ vrací očekávaný výsledek.
        """
        self.assertEqual(str(self.bill), "guest1 Room and meal charges 1200.5")


class StorageModelTest(TestCase):
    def setUp(self):
        """
        Nastavení testovacích dat pro model Storage.
        """
        self.item = Storage.objects.create(itemName="Toilet Paper", itemType="Cleaning", quantitiy=50)

    def test_storage_creation(self):
        """
        Test, zda byla položka ve skladu správně vytvořena.
        """
        self.assertEqual(self.item.itemName, "Toilet Paper")
        self.assertEqual(self.item.itemType, "Cleaning")
        self.assertEqual(self.item.quantitiy, 50)

    def test_storage_str_method(self):
        """
        Test, zda metoda __str__ vrací očekávaný výsledek.
        """
        self.assertEqual(str(self.item), "Toilet Paper (50 ks)")