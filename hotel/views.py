# ------------------------------
# Základní Django funkce pro práci s pohledy
# ------------------------------
from django.shortcuts import render, get_object_or_404, redirect  # Pro práci s šablonami, získání objektů a přesměrování
from django.contrib.auth.decorators import login_required  # Omezení přístupu pouze na přihlášené uživatele
from django.contrib import messages  # Pro zobrazování zpráv uživateli
from django.apps import apps  # Pro dynamické načítání modelů
from .forms import CreateEventForm  # Import formuláře pro vytvoření události
from .models import Event
from .models import Room  # Ujistěte se, že model Room je správně definován
from .models import Guest 

# ------------------------------
# Import modelů
# ------------------------------
from .models import Event, FoodMenu, EventAttendees, Room  # Import modelů používaných v aplikaci

# ------------------------------
# Pohled pro domovskou stránku
# ------------------------------
@login_required(login_url='login')
def home(request):
    """
    Pohled pro zobrazení domovské stránky aplikace 'hotel'.
    """
    return render(request, 'index.html') # Šablona `home.html` musí existovat.


# ------------------------------
# Pohled pro seznam událostí
# ------------------------------
@login_required(login_url='login')
def events_view(request):
    """
    Zobrazení seznamu událostí s možností účasti na událostech.
    """
    role = str(request.user.groups.first()) if request.user.groups.exists() else "guest"
    events = Event.objects.all()
    attended_events = None

    # Načtení událostí, kterých se uživatel účastní
    if role == 'guest':
        attended_events = EventAttendees.objects.filter(guest=request.user.guest)

    # Zpracování formulářových požadavků (např. filtrování nebo účast na události)
    if request.method == "POST":
        if "filter" in request.POST:
            filters = {
                "event_type__icontains": request.POST.get("type"),
                "location__icontains": request.POST.get("location"),
                "start_date__gte": request.POST.get("fd"),
                "end_date__lte": request.POST.get("ed"),
            }
            filters = {key: value for key, value in filters.items() if value}
            events = events.filter(**filters)

        if 'attend' in request.POST:
            event_id = request.POST.get('id')
            event = get_object_or_404(Event, id=event_id)
            if not EventAttendees.objects.filter(event=event, guest=request.user.guest).exists():
                EventAttendees.objects.create(event=event, guest=request.user.guest)
                messages.success(request, f"Byli jste přidáni na událost '{event.title}'.")
            return redirect('events_view')

        if 'remove' in request.POST:
            event_id = request.POST.get('id')
            event = get_object_or_404(Event, id=event_id)
            EventAttendees.objects.filter(event=event, guest=request.user.guest).delete()
            messages.success(request, f"Vaše účast na události '{event.title}' byla zrušena.")
            return redirect('events_view')

    context = {
        "role": role,
        'events': events,
        'attended_events': attended_events,
        "filters": request.POST,
    }
    return render(request, "hotel/events.html", context)


# ------------------------------
# Pohled pro detail události
# ------------------------------
def event_detail(request, event_id):
    """
    Zobrazení detailu konkrétní události.
    """
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'hotel/event_detail.html', {'event': event})


# ------------------------------
# Pohled pro úpravu jídelního menu
# ------------------------------
@login_required(login_url='login')
def edit_food_menu(request, menu_id):
    """
    Pohled pro úpravu konkrétního jídelního menu.
    """
    menu = get_object_or_404(FoodMenu, id=menu_id)
    if request.method == "POST":
        # Pokud formuláře neexistují, je potřeba je vytvořit v souboru `forms.py`
        from .forms import EditFoodMenuForm  # Import formuláře pro úpravu menu
        form = EditFoodMenuForm(request.POST, instance=menu)
        if form.is_valid():
            form.save()
            messages.success(request, "Menu bylo úspěšně upraveno.")
            return redirect("menu_view")
    else:
        from .forms import EditFoodMenuForm  # Import formuláře
        form = EditFoodMenuForm(instance=menu)
    return render(request, "hotel/edit_food_menu.html", {"form": form, "menu": menu})


# ------------------------------
# Pohled pro zobrazení jídelního menu
# ------------------------------
def menu_view(request):
    """
    Zobrazení jídelního lístku s možností filtrování a řazení.
    """
    menu_items = FoodMenu.objects.all()

    # Filtrování a řazení
    category = request.GET.get('category')
    if category:
        menu_items = menu_items.filter(category__icontains=category)

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        menu_items = menu_items.filter(price__gte=min_price)
    if max_price:
        menu_items = menu_items.filter(price__lte=max_price)

    sort_by = request.GET.get('sort_by', 'name')
    if sort_by in ['name', '-name', 'price', '-price']:
        menu_items = menu_items.order_by(sort_by)

    context = {
        'menu_items': menu_items,
        'category': category,
        'min_price': min_price,
        'max_price': max_price,
        'sort_by': sort_by,
    }
    return render(request, 'hotel/menu.html', context)


# ------------------------------
# Pohled pro detail pokoje
# ------------------------------
def room_detail(request, room_id):
    """
    Zobrazení detailu konkrétního pokoje.
    """
    room = get_object_or_404(Room, id=room_id)
    return render(request, 'hotel/room_detail.html', {'room': room})


# ------------------------------
# Funkce pro dynamické načtení modelu Event
# ------------------------------
def get_event_model():
    """
    Funkce pro dynamické načtení modelu Event.
    """
    return apps.get_model('hotel', 'Event')

@login_required(login_url='login')
def create_event(request):
    """
    Pohled pro vytvoření nové události.
    """
    if request.method == 'POST':
        form = CreateEventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('events_view')  # Přesměrování na seznam událostí
    else:
        form = CreateEventForm()
    return render(request, 'hotel/create_event.html', {'form': form})

@login_required(login_url='login')
def delete_event(request, pk):
    """
    Pohled pro smazání události.
    """
    event = get_object_or_404(Event, id=pk)
    event.delete()
    messages.success(request, f"Událost '{event.title}' byla úspěšně smazána.")
    return redirect('events_view')

@login_required(login_url='login')
def pearl_view(request):
    """
    Pohled pro zobrazení statické stránky "Zlatá Perla".
    """
    return render(request, 'hotel/pearl.html')  # Předpokládá existenci šablony `hotel/pearl.html`.

@login_required(login_url='login')
def rooms_list(request):
    """
    Pohled pro zobrazení seznamu pokojů.
    """
    rooms = Room.objects.all()  # Načtení všech pokojů z databáze
    return render(request, 'hotel/rooms_list.html', {'rooms': rooms})  # Šablona `rooms_list.html`

@login_required(login_url='login')
def event_profile(request, event_id):
    """
    Pohled pro zobrazení detailu konkrétní události.
    """
    event = get_object_or_404(Event, id=event_id)  # Načtení události nebo 404
    return render(request, 'hotel/event_profile.html', {'event': event})

# Pohled pro zobrazení seznamu refundací
def refunds_view(request):
    # Logika pro získání dat o refundacích
    refunds = []  # Nahraďte reálnými daty
    return render(request, 'refunds.html', {'refunds': refunds})

login_required
def events_view(request):
    try:
        guest = request.user.guest  # Pokus o přístup k souvisejícímu objektu Guest
    except Guest.DoesNotExist:  # Pokud objekt Guest pro uživatele neexistuje
        guest = None  # Pokud neexistuje, nastavíme guest na None

    return render(request, 'events.html', {'guest': guest})