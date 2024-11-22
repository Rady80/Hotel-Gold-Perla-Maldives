from django.urls import path
from . import views

urlpatterns = [
    path('', views.rooms_list, name='rooms_list'),  # Hlavní stránka pokojů
]