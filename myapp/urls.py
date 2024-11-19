from django.urls import path
from . import views

# Definice URL pro aplikaci
urlpatterns = [
    # Domovská stránka - výchozí stránka aplikace
    path('', views.home, name='home'),

    # Stránka s přehledem pokojů
    path('rooms/', views.rooms, name='rooms'),

    # Stránka s rezervacemi - seznam nebo správa rezervací
    path('bookings/', views.bookings, name='bookings'),

    # Stránka s událostmi - přehled nebo správa událostí
    path('events/', views.events, name='events'),

    # Stránka se skladem - přehled nebo správa položek skladu
    path('storage/', views.storage, name='storage'),

    # Odhlášení uživatele - přesměrování na login po odhlášení
    path('logout/', views.logout_view, name='logout'),
    
    # Detail konkrétního pokoje (dynamický parametr ID pokoje)
path('rooms/<int:room_id>/', views.room_detail, name='room_detail'),
]