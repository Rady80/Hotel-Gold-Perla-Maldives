from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.contrib import messages
from django.db.models import Q
from datetime import datetime
from accounts.models import Guest
from room.models import Room, Booking
from .forms import EditRoomForm


# ------------------------------
# Funkce pro určení role uživatele
# ------------------------------
def get_user_role(user):
    """
    Vrací roli aktuálního uživatele.
    Pokud uživatel nemá přiřazenou skupinu, vrátí 'guest'.
    """
    return str(user.groups.first()) if user.groups.exists() else "guest"


# ------------------------------
# Funkce pro generování cesty k šabloně
# ------------------------------
def get_template_path(role, template_name):
    """
    Generuje cestu k šabloně na základě role uživatele a názvu šablony.
    """
    return f"{role}/{template_name}"


# ------------------------------
# Zobrazení seznamu pokojů
# ------------------------------
@login_required(login_url='login')
def rooms(request):
    """
    Zobrazuje seznam pokojů s možností filtrování podle dostupnosti, kapacity a dalších kritérií.
    """
    role = get_user_role(request.user)  # Získání role uživatele
    rooms = Room.objects.all()  # Načtení všech pokojů

    if request.method == "POST":
        if "filter" in request.POST:
            # Filtrování podle zadaných kritérií
            filters = {
                'number__icontains': request.POST.get("number"),
                'capacity__gte': request.POST.get("capacity"),
                'numberOfBeds__gte': request.POST.get("nob"),
                'roomType__icontains': request.POST.get("type"),
                'price__lte': request.POST.get("price"),
            }
            filters = {key: value for key, value in filters.items() if value}
            rooms = rooms.filter(**filters)

    context = {
        "role": role,
        "rooms": rooms,
    }
    return render(request, get_template_path(role, "rooms.html"), context)


# ------------------------------
# Přidání nového pokoje
# ------------------------------
@login_required(login_url='login')
def add_room(request):
    """
    Umožňuje přidání nového pokoje do systému.
    """
    role = get_user_role(request.user)

    if request.method == "POST":
        # Vytvoření nového pokoje na základě odeslaných dat
        room = Room(
            number=request.POST.get('number'),
            capacity=request.POST.get('capacity'),
            numberOfBeds=request.POST.get('beds'),
            roomType=request.POST.get('type'),
            price=request.POST.get('price'),
        )
        room.save()
        messages.success(request, f"Pokoj číslo {room.number} byl úspěšně přidán.")
        return redirect('rooms')

    return render(request, get_template_path(role, "add-room.html"), {"role": role})


# ------------------------------
# Profil pokoje
# ------------------------------
@login_required(login_url='login')
def room_profile(request, id):
    """
    Zobrazuje detail pokoje, včetně jeho rezervací a správy.
    """
    role = get_user_role(request.user)
    room = get_object_or_404(Room, number=id)  # Získání pokoje podle čísla
    bookings = Booking.objects.filter(roomNumber=room)  # Načtení rezervací pro daný pokoj

    if request.method == "POST":
        if "lockRoom" in request.POST:
            # Zablokování pokoje na zadané období
            start_date = datetime.strptime(request.POST.get("bsd", ""), '%Y-%m-%d').date()
            end_date = datetime.strptime(request.POST.get("bed", ""), '%Y-%m-%d').date()
            room.statusStartDate, room.statusEndDate = start_date, end_date
            room.save()
            messages.success(request, f"Pokoj číslo {room.number} byl zablokován od {start_date} do {end_date}.")
        elif "unlockRoom" in request.POST:
            # Odblokování pokoje
            room.statusStartDate, room.statusEndDate = None, None
            room.save()
            messages.success(request, f"Pokoj číslo {room.number} byl odblokován.")
        elif "deleteRoom" in request.POST:
            # Smazání pokoje (pouze pokud nemá aktivní rezervace)
            if not bookings.filter(startDate__lte=datetime.now().date(), endDate__gte=datetime.now().date()).exists():
                room.delete()
                messages.success(request, f"Pokoj číslo {room.number} byl úspěšně smazán.")
                return redirect("rooms")
            else:
                messages.error(request, "Pokoj nelze smazat, protože má aktivní rezervace.")

    context = {
        "role": role,
        "room": room,
        "bookings": bookings,
    }
    return render(request, get_template_path(role, "room-profile.html"), context)


# ------------------------------
# Editace pokoje
# ------------------------------
@login_required(login_url='login')
def room_edit(request, pk):
    """
    Umožňuje upravit údaje o pokoji.
    """
    role = get_user_role(request.user)
    room = get_object_or_404(Room, number=pk)  # Načtení pokoje podle čísla
    form = EditRoomForm(instance=room)  # Formulář předvyplněný daty pokoje

    if request.method == "POST":
        form = EditRoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            messages.success(request, f"Pokoj číslo {room.number} byl úspěšně aktualizován.")
            return redirect("room-profile", id=room.number)

    context = {
        "role": role,
        "form": form,
    }
    return render(request, get_template_path(role, "room-edit.html"), context)