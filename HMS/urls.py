"""
HMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information, please see:
https://docs.djangoproject.com/en/3.1/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from hotel.views import edit_food_menu
from .views import pearl_view

from accounts.views import *
from room.views import *
from hotel.views import *

urlpatterns = [
    # Admin panel
    path('admin/', admin.site.urls, name="admin"),

    # Hlavní stránka
    path('', home, name="home"),

    # Autentizace uživatele
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('register/', register_page, name="register"),

    # Guests (hosté)
    path('guests/', guests, name="guests"),
    path('guest-profile/<str:pk>/', guest_profile, name="guest-profile"),
    path('guest-edit/<str:pk>/', guest_edit, name="guest-edit"),

    # Employees (zaměstnanci)
    path('employees/', employees, name="employees"),
    path('employee-profile/<str:pk>/', employee_details, name="employee-profile"),
    path('employee-edit/<str:pk>/', employee_details_edit, name="employee-edit"),
    path('employee-add/', add_employee, name="add-employee"),

    # Rooms (pokoje)
    path('rooms/', rooms, name="rooms"),
    path('room-profile/<str:pk>/', room_profile, name="room-profile"),
    path('room-edit/<str:pk>/', room_edit, name="room-edit"),
    path('add-room/', add_room, name="add-room"),
    path('room-services/', room_services, name="room-services"),
    path('current-room-services/', current_room_services, name="current-room-services"),

    # Bookings (rezervace)
    path('bookings/', bookings, name="bookings"),
    path('booking-make/', booking_make, name="booking-make"),
    path('deleteBooking/<str:pk>/', deleteBooking, name="deleteBooking"),

    # Events (události)
    path('events/', events, name="events"),
    path('event-profile/<str:pk>/', event_profile, name="event-profile"),
    path('event-edit/<str:pk>/', event_edit, name="event-edit"),
    path('createEvent/', createEvent, name="createEvent"),
    path('deleteEvent/<str:pk>/', deleteEvent, name="deleteEvent"),

    # Food menu (jídelní lístek)
    path('food-menu/', food_menu, name="food-menu"),
    path('food-menu/<str:pk>/', food_menu_edit, name="food-menu-edit"),
    path('deleteFoodMenu/<str:pk>/', deleteFoodMenu, name="deleteFoodMenu"),
    path('edit-food-menu/', edit_food_menu, name='edit-food-menu'),
    
    # Announcements (oznámení)
    path('announcements/', announcements, name="announcements"),
    path('deleteAnnouncement/<str:pk>/', deleteAnnouncement, name="deleteAnnouncement"),

    # Storage (sklad)
    path('storage/', storage, name="storage"),
    path('deleteStorage/<str:pk>/', deleteStorage, name="deleteStorage"),

    # Tasks (úkoly)
    path('tasks/', tasks, name="tasks"),
    path('completeTask/<str:pk>/', completeTask, name="completeTask"),

    # Refunds (vrácení peněz)
    path('refunds/', refunds, name="refunds"),
    path('request-refund/', request_refund, name="request-refund"),

    # Payment (platby)
    path('payment/', payment, name="payment"),
    path('verify/', verify, name="verify"),

    # Chyby
    path('error/', error, name="error"),
    
    # Obrázek Perly
    path('pearl/', pearl_view, name='pearl'),  # Odkaz na Zlatou perlu
]

# Statické a mediální soubory
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)