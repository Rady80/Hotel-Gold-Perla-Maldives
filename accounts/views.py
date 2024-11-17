from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.contrib import messages
from django.db.models import Q
from datetime import datetime, date, timedelta
from accounts.models import Guest, Employee
from room.models import Booking
from .forms import CreateUserForm
from django.contrib.auth.forms import UserCreationForm

# ------------------------------
# Pohled pro registraci uživatele
# ------------------------------
def register_page(request):
    """
    Registrace nového uživatele a vytvoření profilu hosta.
    """
    if request.user.is_authenticated:
        return redirect('home')  # Pokud je uživatel přihlášen, přesměrovat na domovskou stránku
    else:
        form = CreateUserForm()  # Instance registračního formuláře
        if request.method == 'POST':  # Kontrola odeslání formuláře
            form = CreateUserForm(request.POST)
            if form.is_valid():
                email = request.POST.get("email")
                # Kontrola, zda e-mail již existuje
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'Tento e-mail je již používán.')
                    return redirect('register')

                # Uložení nového uživatele
                user = form.save()
                username = form.cleaned_data.get('username')

                # Přidání uživatele do skupiny "guest"
                group, _ = Group.objects.get_or_create(name="guest")
                user.groups.add(group)

                # Vytvoření záznamu hosta
                phone_number = request.POST.get("phoneNumber")
                Guest.objects.create(user=user, phoneNumber=phone_number)

                login(request, user)  # Automatické přihlášení uživatele po registraci
                messages.success(request, f'Uživatelský účet pro {username} byl úspěšně vytvořen.')
                return redirect('home')  # Přesměrování na domovskou stránku
            else:
                messages.error(request, 'Došlo k chybě během registrace. Zkontrolujte zadané údaje.')

        context = {'form': form}
        return render(request, 'accounts/register.html', context)

# ------------------------------
# Pohled pro přihlášení uživatele
# ------------------------------
def login_page(request):
    """
    Přihlášení uživatele k systému.
    """
    if request.user.is_authenticated:
        return redirect('home')  # Pokud je uživatel přihlášen, přesměrovat na domovskou stránku
    else:
        if request.method == "POST":  # Kontrola odeslání přihlašovacího formuláře
            username = request.POST.get('username')
            password = request.POST.get('password')

            # Autentizace uživatele
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)  # Přihlášení uživatele
                return redirect('home')  # Přesměrování na domovskou stránku
            else:
                messages.error(request, "Nesprávné uživatelské jméno nebo heslo.")

        return render(request, 'accounts/login.html')

# ------------------------------
# Pohled pro odhlášení uživatele
# ------------------------------
def logout_user(request):
    """
    Odhlášení uživatele a přesměrování na přihlašovací stránku.
    """
    logout(request)
    return redirect('login')

# ------------------------------
# Pohled pro zobrazení hostů
# ------------------------------
@login_required(login_url='login')
def guests(request):
    """
    Zobrazení seznamu hostů s možností filtrování.
    """
    role = str(request.user.groups.first()) if request.user.groups.exists() else "guest"
    path = f"{role}/"

    # Výchozí seznam hostů za posledních 30 dní
    bookings = Booking.objects.all()
    fd = datetime.combine(date.today() - timedelta(days=30), datetime.min.time())
    ld = datetime.combine(date.today(), datetime.min.time())
    guests = [b.guest for b in bookings if b.endDate >= fd.date() and b.startDate <= ld.date()]

    if request.method == "POST":
        if "filterDate" in request.POST:  # Filtrování podle data
            fd = request.POST.get("f_day") or "1970-01-01"
            ld = request.POST.get("l_day") or "2030-01-01"

            fd = datetime.strptime(fd, '%Y-%m-%d')
            ld = datetime.strptime(ld, '%Y-%m-%d')

            guests = [b.guest for b in bookings if b.endDate >= fd.date() and b.startDate <= ld.date()]

        if "filterGuest" in request.POST:  # Filtrování podle atributů uživatele
            users = User.objects.all()

            if request.POST.get("id"):
                users = users.filter(id__icontains=request.POST.get("id"))

            if request.POST.get("name"):
                users = users.filter(
                    Q(first_name__icontains=request.POST.get("name")) |
                    Q(last_name__icontains=request.POST.get("name"))
                )

            if request.POST.get("email"):
                users = users.filter(email__icontains=request.POST.get("email"))

            guests = Guest.objects.filter(user__in=users)

        context = {
            "role": role,
            "guests": guests,
            "fd": fd,
            "ld": ld,
        }
        return render(request, path + "guests.html", context)

    context = {
        "role": role,
        "guests": guests,
    }
    return render(request, path + "guests.html", context)

# ------------------------------
# Pohled pro zaměstnance
# ------------------------------
@login_required(login_url='login')
def employees(request):
    """
    Zobrazení seznamu zaměstnanců.
    """
    role = str(request.user.groups.first()) if request.user.groups.exists() else "guest"
    path = f"{role}/"
    employees = Employee.objects.all()

    context = {
        "role": role,
        "employees": employees,
    }
    return render(request, path + "employees.html", context)

# ------------------------------
# Pohled pro statickou stránku Zlaté Perly
# ------------------------------
def pearl_view(request):
    """
    Zobrazení statické stránky Zlaté Perly.
    """
    return render(request, 'pearl.html')  # Odkaz na šablonu pearl.html