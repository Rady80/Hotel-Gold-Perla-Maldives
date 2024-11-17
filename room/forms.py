from django.forms import ModelForm
from django import forms
from .models import Room, Booking, Dependees

# Formulář pro úpravu pokojů
class EditRoomForm(ModelForm):
    """
    Formulář pro úpravu údajů o pokojích.
    """
    class Meta:
        model = Room
        fields = ["capacity", "numberOfBeds", "roomType", "price"]
        labels = {
            'capacity': 'Kapacita pokoje',
            'numberOfBeds': 'Počet postelí',
            'roomType': 'Typ pokoje',
            'price': 'Cena za noc',
        }
        widgets = {
            'capacity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Zadejte kapacitu'}),
            'numberOfBeds': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Počet postelí'}),
            'roomType': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Např. Deluxe'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cena v Kč'}),
        }

# Formulář pro úpravu rezervací
class EditBookingForm(ModelForm):
    """
    Formulář pro úpravu údajů o rezervacích.
    """
    class Meta:
        model = Booking
        fields = ["startDate", "endDate"]
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
        model = Dependees
        fields = ["booking", "name"]
        labels = {
            'booking': 'Rezervace',
            'name': 'Jméno osoby',
        }
        widgets = {
            'booking': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zadejte jméno'}),
        }