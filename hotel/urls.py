from django.urls import path
from . import views  # Import všech pohledů z aplikace

# ------------------------------
# Definice URL směrování
# ------------------------------
urlpatterns = [
    # URL pro profil konkrétní události
    path(
        'event/<int:event_id>/',  # Cesta obsahující ID události jako proměnnou
        views.event_profile,  # Pohled zobrazený pro tuto URL
        name='event-profile'  # Název URL pro použití v šablonách nebo přesměrování
    ),
]