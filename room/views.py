from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.contrib import messages
from django.db.models import Q
from datetime import datetime, timedelta
from accounts.models import Guest
from room.models import Room, Booking, Dependees, RoomServices, Refund
from .forms import EditRoomForm

# Funkce pro určení role uživatele
def get_user_role(user):
    """
    Získá roli aktuálního uživatele. Pokud uživatel nemá žádnou skupinu, vrátí 'guest'.
    """
    return str(user.groups.first()) if user.groups.exists() else "guest"

# Funkce pro získání cesty k šabloně na základě role uživatele
def get_template_path(role, template_name):
    """
    Vrací cestu k šabloně na základě role uživatele.
    """
    return f"{role}/{template_name}"

# Zobrazení seznamu pokojů
@login_required(login_url='login')
def rooms(request):
    """
    Zobrazuje seznam pokojů a umožňuje jejich filtrování na základě parametrů (dostupnost, cena atd.).
    """
    role = get_user_role(request.user)  # Získání role uživatele
    rooms = Room.objects.all()  # Načtení všech pokojů
    first_day, last_day = None, None

    def check_availability(start_date, end_date):
        """
        Vrací seznam dostupných pokojů v zadaném období.
        """
        available_rooms = []
        for room in rooms:
            if not room.statusStartDate or (room.statusStartDate > end_date or room.statusEndDate < start_date):
                bookings = Booking.objects.filter(roomNumber=room)
                if all(b.startDate > end_date or b.endDate < start_date for b in bookings):
                    available_rooms.append(room)
        return available_rooms

    if request.method == "POST":
        if "dateFilter" in request.POST:
            # Filtrování podle dat
            first_day = datetime.strptime(request.POST.get("fd", ""), '%Y-%m-%d')
            last_day = datetime.strptime(request.POST.get("ld", ""), '%Y-%m-%d')
            rooms = check_availability(first_day.date(), last_day.date())

        if "filter" in request.POST:
            # Filtrování podle dalších kritérií
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
        "fd": first_day,
        "ld": last_day,
    }
    return render(request, get_template_path(role, "rooms.html"), context)

# Přidání nového pokoje
@login_required(login_url='login')
def add_room(request):
    """
    Umožňuje přidat nový pokoj do systému.
    """
    role = get_user_role(request.user)

    if request.method == "POST":
        room = Room(
            number=request.POST.get('number'),
            capacity=request.POST.get('capacity'),
            numberOfBeds=request.POST.get('beds'),
            roomType=request.POST.get('type'),
            price=request.POST.get('price'),
        )
        room.save()
        return redirect('rooms')

    return render(request, get_template_path(role, "add-room.html"), {"role": role})

# Profil pokoje
@login_required(login_url='login')
def room_profile(request, id):
    """
    Zobrazuje profil pokoje včetně rezervací a možností správy.
    """
    role = get_user_role(request.user)
    room = Room.objects.get(number=id)
    bookings = Booking.objects.filter(roomNumber=room)

    if request.method == "POST":
        if "lockRoom" in request.POST:
            # Zablokování pokoje
            start_date = datetime.strptime(request.POST.get("bsd"), '%Y-%m-%d').date()
            end_date = datetime.strptime(request.POST.get("bed"), '%Y-%m-%d').date()
            if not any(b.startDate <= end_date and b.endDate >= start_date for b in bookings):
                room.statusStartDate, room.statusEndDate = start_date, end_date
                room.save()
            else:
                messages.error(request, "Pokoj je v tomto období již rezervován.")
        elif "unlockRoom" in request.POST:
            # Odblokování pokoje
            room.statusStartDate, room.statusEndDate = None, None
            room.save()
        elif "deleteRoom" in request.POST:
            # Smazání pokoje
            if not any(b.startDate <= datetime.now().date() <= b.endDate for b in bookings):
                room.delete()
                return redirect("rooms")
            else:
                messages.error(request, "Pokoj nelze smazat, protože má aktivní rezervace.")

    context = {
        "role": role,
        "room": room,
        "bookings": bookings,
    }
    return render(request, get_template_path(role, "room-profile.html"), context)

# Editace pokoje
@login_required(login_url='login')
def room_edit(request, pk):
    """
    Umožňuje upravit detaily pokoje (kapacita, cena atd.).
    """
    role = get_user_role(request.user)
    room = Room.objects.get(number=pk)
    form = EditRoomForm(instance=room)

    if request.method == "POST":
        form = EditRoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect("room-profile", id=room.number)

    return render(request, get_template_path(role, "room-edit.html"), {"role": role, "form": form})