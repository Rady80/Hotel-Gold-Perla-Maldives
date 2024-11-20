from django.urls import path
from . import views  # Import všech pohledů z aplikace

# ------------------------------
# Definice URL směrování pro aplikaci
# ------------------------------
urlpatterns = [
    # Domovská stránka - výchozí stránka aplikace
    path(
        '',  # Kořenová URL (např. 'http://localhost:8000/')
        views.home,  # Pohled, který zpracuje tuto URL
        name='home'  # Název URL pro použití v šablonách (např. `{% url 'home' %}`)
    ),

    # Stránka s přehledem pokojů
    path(
        'rooms/',  # URL pro přehled pokojů
        views.rooms,  # Pohled, který zobrazí pokoje
        name='rooms'  # Název URL (např. `{% url 'rooms' %}`)
    ),

    # Stránka s rezervacemi - seznam nebo správa rezervací
    path(
        'bookings/',  # URL pro přehled rezervací
        views.bookings,  # Pohled, který zobrazí nebo spravuje rezervace
        name='bookings'  # Název URL (např. `{% url 'bookings' %}`)
    ),

    # Stránka s událostmi - přehled nebo správa událostí
    path(
        'events/',  # URL pro přehled událostí
        views.events,  # Pohled, který zobrazí události
        name='events'  # Název URL (např. `{% url 'events' %}`)
    ),

    # Stránka se skladem - přehled nebo správa položek skladu
    path(
        'storage/',  # URL pro přehled skladu
        views.storage,  # Pohled, který zobrazí skladové položky
        name='storage'  # Název URL (např. `{% url 'storage' %}`)
    ),

    # Odhlášení uživatele - přesměrování na přihlašovací stránku po odhlášení
    path(
        'logout/',  # URL pro odhlášení
        views.logout_view,  # Pohled, který zpracuje odhlášení
        name='logout'  # Název URL (např. `{% url 'logout' %}`)
    ),

    # Detail konkrétního pokoje (dynamický parametr ID pokoje)
    path(
        'rooms/<int:room_id>/',  # Dynamická URL s ID pokoje
        views.room_detail,  # Pohled, který zobrazí detaily pokoje
        name='room_detail'  # Název URL (např. `{% url 'room_detail' room_id=1 %}`)
    ),

    # URL pro úpravu jídelního menu
    path(
        'edit-menu/',  # Adresa pro úpravu menu
        views.edit_food_menu,  # Pohled, který zpracuje editaci menu
        name='edit_food_menu'  # Název URL (např. `{% url 'edit_food_menu' %}`)
    ),
]
