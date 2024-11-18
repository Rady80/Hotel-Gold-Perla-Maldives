from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import FoodMenu, Event, EventAttendees, Storage
from .forms import EditFoodMenuForm, CreateEventForm
from accounts.models import Guest

# ------------------------------
# Domovská stránka
# ------------------------------
@login_required(login_url='login')
def home(request):
    """
    Zajišťuje zobrazení domovské stránky s informacemi podle role uživatele.
    """
    role = str(request.user.groups.first()) if request.user.groups.exists() else "No Group"
    context = {"role": role}
    return render(request, "hotel/home.html", context)

# ------------------------------
# Zobrazení stránky "O hotelu"
# ------------------------------
def about_view(request):
    """
    Zobrazení stránky 'O hotelu'.
    """
    return render(request, 'hotel/about.html')

# ------------------------------
# Kontaktní stránka
# ------------------------------
def contact_view(request):
    """
    Zobrazení kontaktní stránky.
    """
    return render(request, 'hotel/contact.html')

# ------------------------------
# Zobrazení Zlaté Perly
# ------------------------------
def pearl_view(request):
    """
    Zobrazení stránky Zlatá Perla.
    """
    return render(request, 'hotel/pearl.html')

# ------------------------------
# Správa událostí
# ------------------------------
@login_required(login_url='login')
def events(request):
    """
    Správa událostí - filtrování a správa účasti na událostech.
    """
    role = str(request.user.groups.first())  # Role uživatele
    path = f"{role}/"  # Nastavení cesty šablony podle role

    events = Event.objects.all()  # Načtení všech událostí
    attended_events = None

    if role == 'guest':
        attended_events = EventAttendees.objects.filter(guest=request.user.guest)

    if request.method == "POST":
        # Filtrování událostí
        if "filter" in request.POST:
            filters = {
                "eventType__icontains": request.POST.get("type"),
                "location__icontains": request.POST.get("location"),
                "startDate__gte": request.POST.get("fd"),
                "endDate__lte": request.POST.get("ed"),
            }
            filters = {key: value for key, value in filters.items() if value}
            events = events.filter(**filters)

        # Přidání účasti
        if 'attend' in request.POST:
            temp_event = events.get(id=request.POST.get('id'))
            if not EventAttendees.objects.filter(event=temp_event, guest=request.user.guest).exists():
                EventAttendees.objects.create(event=temp_event, guest=request.user.guest)
            return redirect('events')

        # Odebrání účasti
        if 'remove' in request.POST:
            temp_event = events.get(id=request.POST.get('id'))
            EventAttendees.objects.filter(event=temp_event, guest=request.user.guest).delete()
            return redirect('events')

    context = {
        "role": role,
        'events': events,
        'attended_events': attended_events,
        "filters": request.POST,
    }
    return render(request, f"{path}events.html", context)

# ------------------------------
# Vytvoření nové události
# ------------------------------
@login_required(login_url='login')
def create_event(request):
    """
    Umožňuje vytvoření nové události.
    """
    role = str(request.user.groups.first())
    path = f"{role}/"

    form = CreateEventForm()
    if request.method == "POST":
        form = CreateEventForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Událost byla úspěšně vytvořena.")
            return redirect('events')

    return render(request, f"{path}create_event.html", {'form': form, "role": role})

# ------------------------------
# Editace jídelního menu
# ------------------------------
@login_required(login_url='login')
def edit_food_menu(request, menu_id):
    """
    Umožňuje úpravu konkrétního jídelního menu.
    """
    menu = get_object_or_404(FoodMenu, id=menu_id)
    if request.method == "POST":
        form = EditFoodMenuForm(request.POST, instance=menu)
        if form.is_valid():
            form.save()
            messages.success(request, "Menu bylo úspěšně upraveno.")
            return redirect("menu_list")
    else:
        form = EditFoodMenuForm(instance=menu)
    return render(request, "hotel/edit_food_menu.html", {"form": form, "menu": menu})

# ------------------------------
# Smazání události
# ------------------------------
@login_required(login_url='login')
def delete_event(request, pk):
    """
    Smazání vybrané události.
    """
    role = str(request.user.groups.first())
    path = f"{role}/"

    event = get_object_or_404(Event, id=pk)
    if request.method == "POST":
        event.delete()
        messages.success(request, "Událost byla úspěšně smazána.")
        return redirect('events')

    return render(request, f"{path}delete_event.html", {"event": event, "role": role})

# ------------------------------
# Správa skladových položek
# ------------------------------
@login_required(login_url='login')
def storage(request):
    """
    Správa skladových položek.
    """
    role = str(request.user.groups.first())
    path = f"{role}/"

    storage_items = Storage.objects.all()
    if request.method == "POST":
        # Přidání nové položky
        if "add" in request.POST:
            Storage.objects.create(
                itemName=request.POST.get("itemName"),
                itemType=request.POST.get("itemType"),
                quantity=request.POST.get("quantity"),
            )
            messages.success(request, "Položka byla úspěšně přidána.")
        # Filtrování skladu
        elif "filter" in request.POST:
            filters = {
                "itemName__icontains": request.POST.get("name"),
                "itemType__icontains": request.POST.get("type"),
            }
            filters = {key: value for key, value in filters.items() if value}
            storage_items = storage_items.filter(**filters)

    return render(request, f"{path}storage.html", {
        "role": role,
        "storage_items": storage_items,
        "filters": request.POST,
    })