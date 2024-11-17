from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import Group
from django.db.models import Q
from datetime import datetime, date, timedelta
from .forms import *
from accounts.models import Guest, Employee
from hotel.models import *
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
    role = str(request.user.groups.first())
    path = f"{role}/"

    events = Event.objects.all()
    attended_events = None

    if role == 'guest':
        attended_events = EventAttendees.objects.filter(guest=request.user.guest)

    if request.method == "POST":
        # Filtrování událostí
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


# Vytvoření události
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
            return redirect('events')

    return render(request, f"{path}create_event.html", {'form': form, "role": role})


# Smazání události
@login_required(login_url='login')
def delete_event(request, pk):
    """
    Smazání vybrané události.
    """
    role = str(request.user.groups.first())
    path = f"{role}/"

    event = Event.objects.get(id=pk)
    if request.method == "POST":
        event.delete()
        return redirect('events')

    return render(request, f"{path}delete_event.html", {"event": event, "role": role})


# Oznámení
@login_required(login_url='login')
def announcements(request):
    """
    Správa oznámení - filtrování a přidávání nových oznámení.
    """
    role = str(request.user.groups.first())
    path = f"{role}/"

    announcements = Announcement.objects.all()
    if request.method == "POST":
        # Filtrování oznámení
        if "filter" in request.POST:
            filters = {
                "content__icontains": request.POST.get("content"),
                "date": request.POST.get("date"),
            }
            filters = {key: value for key, value in filters.items() if value}
            announcements = announcements.filter(**filters)

        # Přidání oznámení
        if "sendAnnouncement" in request.POST:
            Announcement.objects.create(
                sender=request.user.employee,
                content=request.POST.get('textid')
            )
            return redirect('announcements')

    return render(request, f"{path}announcements.html", {
        "role": role,
        "announcements": announcements,
        "filters": request.POST,
    })


# Smazání oznámení
@login_required(login_url='login')
def delete_announcement(request, pk):
    """
    Smazání vybraného oznámení.
    """
    role = str(request.user.groups.first())
    path = f"{role}/"

    announcement = Announcement.objects.get(id=pk)
    if request.method == "POST":
        announcement.delete()
        return redirect('announcements')

    return render(request, f"{path}delete_announcement.html", {"announcement": announcement, "role": role})


# Sklad
@login_required(login_url='login')
def storage(request):
    """
    Správa skladových položek.
    """
    role = str(request.user.groups.first())
    path = f"{role}/"

    storage_items = Storage.objects.all()
    if request.method == "POST":
        # Přidání položky do skladu
        if "add" in request.POST:
            Storage.objects.create(
                itemName=request.POST.get("itemName"),
                itemType=request.POST.get("itemType"),
                quantitiy=request.POST.get("quantitiy"),
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


# Smazání skladové položky
@login_required(login_url='login')
def delete_storage(request, pk):
    """
    Smazání položky ze skladu.
    """
    role = str(request.user.groups.first())
    path = f"{role}/"

    storage_item = Storage.objects.get(id=pk)
    if request.method == "POST":
        storage_item.delete()
        return redirect('storage')

    return render(request, f"{path}delete_storage.html", {"storage_item": storage_item, "role": role})