from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import FoodMenu
from .forms import EditFoodMenuForm
from hotel.models import *
from accounts.models import Guest, Employee
from room.models import *

# Domovská stránka
@login_required(login_url='login')
def home(request):
    """
    Zajišťuje zobrazení domovské stránky s informacemi podle role uživatele.
    """
    role = str(request.user.groups.first()) if request.user.groups.exists() else "No Group"
    context = {"role": role}
    return render(request, "home.html", context)

# Události
@login_required(login_url='login')
def events(request):
    """
    Správa událostí - filtrování a správa účasti na událostech.
    """
    role = str(request.user.groups.first())  # Získání role přihlášeného uživatele
    path = f"{role}/"  # Nastavení cesty šablony na základě role

    events = Event.objects.all()  # Načtení všech událostí
    attended_events = None

    if role == 'guest':
        attended_events = EventAttendees.objects.filter(guest=request.user.guest)

    if request.method == "POST":
        # Filtrování událostí podle kritérií
        if "filter" in request.POST:
            filters = {
                "eventType__contains": request.POST.get("type"),
                "location__contains": request.POST.get("location"),
                "startDate__gte": request.POST.get("fd"),
                "endDate__lte": request.POST.get("ed"),
            }
            filters = {key: value for key, value in filters.items() if value}
            events = events.filter(**filters)

        # Přidání účasti na události
        if 'attend' in request.POST:
            temp_event = events.get(id=request.POST.get('id'))
            if not EventAttendees.objects.filter(event=temp_event, guest=request.user.guest).exists():
                EventAttendees.objects.create(event=temp_event, guest=request.user.guest)
            return redirect('events')

        # Odebrání účasti na události
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

# Vytvoření události
@login_required(login_url='login')
def create_event(request):
    """
    Umožňuje vytvoření nové události.
    """
    role = str(request.user.groups.first())  # Získání role přihlášeného uživatele
    path = f"{role}/"  # Nastavení cesty šablony na základě role

    form = CreateEventForm()
    if request.method == "POST":
        form = CreateEventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('events')

    return render(request, f"{path}create_event.html", {'form': form, "role": role})

# Editace jídelního menu
@login_required(login_url='login')
def edit_food_menu(request, menu_id):
    """
    View pro úpravu jídelního menu.
    """
    menu = get_object_or_404(FoodMenu, id=menu_id)  # Načtení konkrétního menu
    if request.method == "POST":
        form = EditFoodMenuForm(request.POST, instance=menu)
        if form.is_valid():
            form.save()
            return redirect("menu_list")  # Přesměrování na seznam menu po uložení
    else:
        form = EditFoodMenuForm(instance=menu)
    return render(request, "hotel/edit_food_menu.html", {"form": form, "menu": menu})

# Smazání události
@login_required(login_url='login')
def delete_event(request, pk):
    """
    Smazání vybrané události.
    """
    role = str(request.user.groups.first())  # Získání role přihlášeného uživatele
    path = f"{role}/"  # Nastavení cesty šablony na základě role

    event = Event.objects.get(id=pk)
    if request.method == "POST":
        event.delete()
        return redirect('events')

    return render(request, f"{path}delete_event.html", {"event": event, "role": role})

# Sklad
@login_required(login_url='login')
def storage(request):
    """
    Správa skladových položek.
    """
    role = str(request.user.groups.first())  # Získání role přihlášeného uživatele
    path = f"{role}/"  # Nastavení cesty šablony na základě role

    storage_items = Storage.objects.all()  # Načtení všech skladových položek
    if request.method == "POST":
        # Přidání položky do skladu
        if "add" in request.POST:
            Storage.objects.create(
                itemName=request.POST.get("itemName"),
                itemType=request.POST.get("itemType"),
                quantity=request.POST.get("quantity"),
            )
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

# hotel/views.py
from django.shortcuts import render

def pearl_view(request):
    """
    View pro zobrazení Zlaté Perly.
    """
    return render(request, 'pearl.html')