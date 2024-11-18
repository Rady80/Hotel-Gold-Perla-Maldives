from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Domovská stránka
    path('rooms/', views.rooms, name='rooms'),  # Stránka s pokoji
    path('bookings/', views.bookings, name='bookings'),  # Stránka s rezervacemi
    path('events/', views.events, name='events'),  # Stránka s událostmi
    path('storage/', views.storage, name='storage'),  # Stránka se skladem
    path('logout/', views.logout_view, name='logout'),  # Odhlášení uživatele
]