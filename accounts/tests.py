from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from accounts.models import Guest, Employee
from django.urls import reverse


class AccountsTestCase(TestCase):
    """
    Testovací třída pro aplikaci Accounts.
    """

    def setUp(self):
        """
        Inicializace testovacích dat.
        """
        # Vytvoření skupin
        self.guest_group = Group.objects.create(name="guest")
        self.manager_group = Group.objects.create(name="manager")

        # Vytvoření uživatele a hosta
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.guest = Guest.objects.create(user=self.user, phoneNumber="+123456789")

        # Vytvoření klienta
        self.client = Client()

    def test_registration_view(self):
        """
        Testování registrace uživatele.
        """
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'password1': 'securePassword123',
            'password2': 'securePassword123',
            'phoneNumber': '+987654321'
        })
        self.assertEqual(response.status_code, 302)  # Přesměrování po registraci
        self.assertTrue(User.objects.filter(username="newuser").exists())
        self.assertTrue(Guest.objects.filter(phoneNumber="+987654321").exists())

    def test_login_view(self):
        """
        Testování přihlášení uživatele.
        """
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 302)  # Přesměrování po přihlášení
        self.assertEqual(int(self.client.session['_auth_user_id']), self.user.pk)

    def test_guest_creation(self):
        """
        Testování správného vytvoření hosta.
        """
        self.assertEqual(self.guest.phoneNumber, "+123456789")
        self.assertEqual(self.guest.user.username, "testuser")

    def test_guest_booking_count(self):
        """
        Testování počtu rezervací pro hosta.
        """
        # Simulace modelu Booking (pokud existuje).
        # Booking.objects.create(guest=self.guest, startDate="2023-01-01", endDate="2023-01-10")
        # self.assertEqual(self.guest.numOfBooking(), 1)  # Ověření počtu rezervací
        self.assertEqual(self.guest.numOfBooking(), 0)  # Výchozí hodnota

    def test_employee_creation(self):
        """
        Testování vytvoření zaměstnance.
        """
        manager_user = User.objects.create_user(username="manager", password="password123")
        employee = Employee.objects.create(user=manager_user, phoneNumber="+111111111", salary=5000.0)
        self.assertEqual(employee.phoneNumber, "+111111111")
        self.assertEqual(employee.salary, 5000.0)

    def test_unauthorized_access(self):
        """
        Testování, zda nepřihlášený uživatel nemá přístup na chráněné stránky.
        """
        response = self.client.get(reverse('guests'))
        self.assertEqual(response.status_code, 302)  # Přesměrování na přihlašovací stránku
        self.assertTrue(response.url.startswith(reverse('login')))

    def test_authorized_access(self):
        """
        Testování, zda přihlášený uživatel má přístup na chráněné stránky.
        """
        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse('guests'))
        self.assertEqual(response.status_code, 200)  # Ověření přístupu
