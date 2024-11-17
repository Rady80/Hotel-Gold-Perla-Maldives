from django import forms
from .models import Room, Booking, Dependees

# Formulář pro úpravu pokojů
class EditRoomForm(forms.ModelForm):
    """
    Formulář pro úpravu údajů o pokojích.
    """
    class Meta:
        model = Room  # Model, který tento formulář reprezentuje
        fields = ["capacity", "numberOfBeds", "roomType", "price"]  # Pole, která lze upravovat
        labels = {
            'capacity': 'Kapacita pokoje',  # Popis pro pole kapacity
            'numberOfBeds': 'Počet postelí',  # Popis pro pole počtu postelí
            'roomType': 'Typ pokoje',  # Popis pro pole typu pokoje
            'price': 'Cena za noc',  # Popis pro pole ceny
        }
        widgets = {
            'capacity': forms.NumberInput(attrs={
                'class': 'form-control', 'placeholder': 'Zadejte kapacitu'
            }),  # Vstupní pole pro kapacitu
            'numberOfBeds': forms.NumberInput(attrs={
                'class': 'form-control', 'placeholder': 'Počet postelí'
            }),  # Vstupní pole pro počet postelí
            'roomType': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Např. Deluxe'
            }),  # Textové pole pro typ pokoje
            'price': forms.NumberInput(attrs={
                'class': 'form-control', 'placeholder': 'Cena v Kč'
            }),  # Vstupní pole pro cenu
        }

    def clean(self):
        """
        Dodatečná validace formuláře.
        """
        from .validators import validate_room_capacity  # Lazy import validátoru pro kapacitu
        validate_room_capacity(self.cleaned_data.get("capacity"))  # Validace kapacity pokoje
        return self.cleaned_data  # Vrací vyčištěná data

# Formulář pro rezervace
class EditBookingForm(forms.ModelForm):
    """
    Formulář pro úpravu rezervací.
    """
    class Meta:
        model = Booking  # Model rezervací
        fields = ["startDate", "endDate"]  # Pole, která lze upravovat
        labels = {
            'startDate': 'Datum začátku',  # Popis pro pole začátku rezervace
            'endDate': 'Datum konce',  # Popis pro pole konce rezervace
        }
        widgets = {
            'startDate': forms.DateInput(attrs={
                'class': 'form-control', 'type': 'date'
            }),  # Datumový vstup pro začátek
            'endDate': forms.DateInput(attrs={
                'class': 'form-control', 'type': 'date'
            }),  # Datumový vstup pro konec
        }

# Formulář pro správu závislých osob
class EditDependeesForm(forms.ModelForm):
    """
    Formulář pro úpravu údajů o závislých osobách.
    """
    class Meta:
        model = Dependees  # Model závislých osob
        fields = ["booking", "name"]  # Pole, která lze upravovat
        labels = {
            'booking': 'Rezervace',  # Popis pro pole rezervace
            'name': 'Jméno osoby',  # Popis pro pole jména osoby
        }
        widgets = {
            'booking': forms.Select(attrs={
                'class': 'form-control'
            }),  # Výběrové pole pro rezervaci
            'name': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Zadejte jméno'
            }),  # Textové pole pro jméno osoby
        }