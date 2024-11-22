from django.urls import path
from . import views  # Importuje funkce z views.py

urlpatterns = [
    path('', views.home_view, name='home'),  # Root URL směřuje na home_view
    
    
]