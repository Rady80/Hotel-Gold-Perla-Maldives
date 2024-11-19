# accounts/test.py
from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from accounts.models import Guest, Employee
from django.urls import reverse


class AccountsTestCase(TestCase):
    """
    Testovací třída pro aplikaci Accounts.
    Obsahuje testy pro registraci, přihlášení, vytváření hostů a zaměstnanců
    a také kontrolu přístupů k chráněným stránkám.
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
        Testování registrace nového uživatele.
        Ověřuje, že po registraci je uživatel i host úspěšně vytvořen.
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
        self.assertTrue(User.objects.filter(username="newuser").exists())  # Ověření existence uživatele
        self.assertTrue(Guest.objects.filter(phoneNumber="+987654321").exists())  # Ověření existence hosta

    def test_login_view(self):
        """
        Testování přihlášení existujícího uživatele.
        """
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 302)  # Přesměrování po přihlášení
        self.assertEqual(int(self.client.session['_auth_user_id']), self.user.pk)

    def test_guest_creation(self):
        """
        Testování vytvoření hosta.
        Ověřuje správnost přidělení údajů hostovi.
        """
        self.assertEqual(self.guest.phoneNumber, "+123456789")
        self.assertEqual(self.guest.user.username, "testuser")

    def test_guest_booking_count(self):
        """
        Testování počtu rezervací hosta.
        Výchozí hodnota by měla být 0.
        """
        self.assertEqual(self.guest.num_of_bookings(), 0)

    def test_employee_creation(self):
        """
        Testování vytvoření zaměstnance.
        Ověřuje, že zaměstnanec je správně propojen s uživatelem
        a obsahuje správné údaje.
        """
        manager_user = User.objects.create_user(username="manager", password="password123")
        employee = Employee.objects.create(user=manager_user, phoneNumber="+111111111", salary=5000.0)
        self.assertEqual(employee.phoneNumber, "+111111111")
        self.assertEqual(employee.salary, 5000.0)

    def test_unauthorized_access(self):
        """
        Testování nepovoleného přístupu na chráněné stránky.
        Nepřihlášený uživatel by měl být přesměrován na přihlašovací stránku.
        """
        response = self.client.get(reverse('guests'))
        self.assertEqual(response.status_code, 302)  # Přesměrování na přihlašovací stránku
        self.assertTrue(response.url.startswith(reverse('login')))

    def test_authorized_access(self):
        """
        Testování povoleného přístupu na chráněné stránky.
        Přihlášený uživatel by měl mít přístup.
        """
        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse('guests'))
        self.assertEqual(response.status_code, 200)  # Ověření úspěšného přístupu