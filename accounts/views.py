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

# ------------------------------
# Registrace nového uživatele
# ------------------------------
def register_page(request):
    """
    Registrace nového uživatele a vytvoření profilu hosta.
    Při úspěšné registraci je uživatel automaticky přihlášen.
    """
    if request.user.is_authenticated:
        return redirect('home')  # Přesměrování přihlášeného uživatele na domovskou stránku
    else:
        form = CreateUserForm()  # Inicializace registračního formuláře
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data.get("email")
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'Tento e-mail je již používán.')
                    return redirect('register')

                # Vytvoření uživatele
                user = form.save()
                username = form.cleaned_data.get('username')

                # Přidání uživatele do skupiny "guest"
                group, _ = Group.objects.get_or_create(name="guest")
                user.groups.add(group)

                # Vytvoření hosta s telefonním číslem
                phone_number = request.POST.get("phoneNumber")
                Guest.objects.create(user=user, phoneNumber=phone_number)

                login(request, user)  # Automatické přihlášení
                messages.success(request, f'Uživatelský účet {username} byl úspěšně vytvořen.')
                return redirect('home')
            else:
                messages.error(request, 'Došlo k chybě během registrace. Zkontrolujte zadané údaje.')

        return render(request, 'accounts/register.html', {'form': form})


# ------------------------------
# Přihlášení uživatele
# ------------------------------
def login_page(request):
    """
    Přihlášení uživatele do systému.
    Při neúspěšném přihlášení je zobrazena chybová zpráva.
    """
    if request.user.is_authenticated:
        return redirect('home')  # Přesměrování přihlášeného uživatele
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Nesprávné uživatelské jméno nebo heslo.")

        return render(request, 'accounts/login.html')


# ------------------------------
# Odhlášení uživatele
# ------------------------------
def logout_user(request):
    """
    Odhlášení uživatele a přesměrování na přihlašovací stránku.
    """
    logout(request)
    messages.info(request, "Byli jste úspěšně odhlášeni.")
    return redirect('login')


# ------------------------------
# Seznam hostů
# ------------------------------
@login_required(login_url='login')
def guests(request):
    """
    Zobrazení seznamu hostů s možností filtrování podle atributů nebo data rezervací.
    """
    role = str(request.user.groups.first()) if request.user.groups.exists() else "guest"
    path = f"{role}/"  # Cesta k šablonám dle role
    bookings = Booking.objects.all()

    # Výchozí časové období pro filtrování
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
    return render(request, f"{path}guests.html", context)


# ------------------------------
# Seznam zaměstnanců
# ------------------------------
@login_required(login_url='login')
def employees(request):
    """
    Zobrazení seznamu zaměstnanců.
    """
    role = str(request.user.groups.first()) if request.user.groups.exists() else "guest"
    path = f"{role}/"  # Cesta k šablonám dle role
    employees = Employee.objects.all()

    context = {
        "role": role,
        "employees": employees,
    }
    return render(request, f"{path}employees.html", context)


# ------------------------------
# Statická stránka Zlaté Perly
# ------------------------------
def pearl_view(request):
    """
    Zobrazení statické stránky Zlaté Perly.
    """
    return render(request, 'pearl.html')


# ------------------------------
# Pohled pro zobrazení profilu uživatele
# ------------------------------
@login_required
def profile_view(request):
    """
    Pohled pro zobrazení profilu uživatele.
    """
    return render(request, 'accounts/profile.html', {'user': request.user})