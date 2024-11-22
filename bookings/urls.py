from django.urls import path
from . import views  # Importujeme views, ne modely
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.bookings_list, name='bookings_list'),  # Hlavní stránka rezervací
    path('reservations/', views.reservations, name='reservations'),  # Cesta pro seznam rezervací
    path('logout/', LogoutView.as_view(), name='logout'),  # URL pro odhlášení
]

