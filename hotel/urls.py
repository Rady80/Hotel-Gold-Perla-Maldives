from django.urls import path  # Pro definování URL cest
from hotel import views as hotel_views  # Import pohledů z aplikace hotel
from django.views.generic import TemplateView  # Pro použití šablony
from . import views

# ------------------------------
# Definice URL směrování pro aplikaci 'hotel'
# ------------------------------
urlpatterns = [
    # ------------------------------
    # Domovská stránka aplikace 'hotel'
    # ------------------------------
    path(
        '', 
        TemplateView.as_view(template_name='index.html'),  # Zobrazení šablony index.html pro domovskou stránku
        name='home'  # Název URL pro použití v šablonách (např. `{% url 'home' %}`)
    ),

    # ------------------------------
    # Správa událostí
    # ------------------------------
    path(
        'events/', 
        hotel_views.events_view,  # Pohled pro zobrazení seznamu událostí
        name='events_view'  # Název URL pro použití v šablonách (např. `{% url 'events_view' %}`)
    ),

    path(
        'events/<int:event_id>/',  # Dynamická cesta obsahující ID události
        hotel_views.event_detail,  # Pohled pro zobrazení detailu konkrétní události
        name='event_detail'  # Název URL pro použití v šablonách (např. `{% url 'event_detail' event_id=1 %}`)
    ),

    # ------------------------------
    # Zobrazení a správa pokojů
    # ------------------------------
    path(
        'rooms/', 
        hotel_views.rooms_list,  # Pohled pro zobrazení seznamu pokojů
        name='rooms_list'  # Název URL pro použití v šablonách (např. `{% url 'rooms_list' %}`)
    ),

    path(
        'rooms/<int:room_id>/',  # Dynamická cesta obsahující ID pokoje
        hotel_views.room_detail,  # Pohled pro zobrazení detailu konkrétního pokoje
        name='room_detail'  # Název URL pro použití v šablonách (např. `{% url 'room_detail' room_id=1 %}`)
    ),

    # ------------------------------
    # Detail konkrétní události
    # ------------------------------
    path(
        'event/<int:event_id>/', 
        hotel_views.event_profile,  # Pohled pro detail konkrétní události
        name='event_profile'  # Název URL pro použití v šablonách (např. `{% url 'event_profile' event_id=1 %}`)
    ),

    # ------------------------------
    # Zobrazení seznamu refundací
    # ------------------------------
    path(
        'refunds/', 
        hotel_views.refunds_view,  # Pohled pro zobrazení seznamu refundací
        name='refunds'  # Název URL pro použití v šablonách (např. `{% url 'refunds' %}`)
        
    ),
    path('', views.home, name='home'),
]