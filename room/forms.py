from django.forms import ModelForm
from django import forms
from .models import Room, Booking, Dependees


# Formulář pro úpravu pokojů
class EditRoomForm(ModelForm):
    """
    Formulář pro úpravu údajů o pokojích.
    """
    class Meta:
        model = Room  # Odkaz na model Room
        fields = ["capacity", "numberOfBeds", "roomType", "price"]  # Pole, která se budou upravovat
        labels = {
            'capacity': 'Kapacita pokoje',
            'numberOfBeds': 'Počet postelí',
            'roomType': 'Typ pokoje',
            'price': 'Cena za noc',
        }
        widgets = {
            'capacity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Zadejte kapacitu'}),
            'numberOfBeds': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Počet postelí'}),
            'roomType': forms.Select(attrs={'class': 'form-control'}),  # Použití Select pro typ pokoje
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cena v Kč'}),
        }


# Formulář pro úpravu rezervací
class EditBookingForm(ModelForm):
    """
    Formulář pro úpravu údajů o rezervacích.
    """
    class Meta:
        model = Booking  # Odkaz na model Booking
        fields = ["startDate", "endDate"]  # Pole, která se budou upravovat
        labels = {
            'startDate': 'Datum začátku',
            'endDate': 'Datum konce',
        }
        widgets = {
            'startDate': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'endDate': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


# Formulář pro úpravu údajů o závislých osobách
class EditDependeesForm(ModelForm):
    """
    Formulář pro úpravu údajů o závislých osobách.
    """
    class Meta:
        model = Dependees  # Odkaz na model Dependees
        fields = ["booking", "name"]  # Pole, která se budou upravovat
        labels = {
            'booking': 'Rezervace',
            'name': 'Jméno osoby',
        }
        widgets = {
            'booking': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zadejte jméno'}),
        }


# Alternativní formulář pro úpravu pokojů
class AlternativeEditRoomForm(forms.ModelForm):
    """
    Alternativní formulář pro úpravu informací o pokoji.
    """
    class Meta:
        model = Room  # Odkaz na model Room
        fields = ['room_number', 'roomType', 'price', 'capacity', 'numberOfBeds', 'status']  # Pole, která se budou upravovat
        labels = {
            'room_number': 'Číslo pokoje',
            'roomType': 'Typ pokoje',  # Správný název pole podle modelu
            'price': 'Cena za noc',
            'capacity': 'Kapacita pokoje',
            'numberOfBeds': 'Počet postelí',
            'status': 'Stav pokoje',
        }
        widgets = {
            'room_number': forms.TextInput(attrs={'class': 'form-control'}),
            'roomType': forms.Select(attrs={'class': 'form-control'}),  # Použití Select pro výběr z možností
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control'}),
            'numberOfBeds': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }