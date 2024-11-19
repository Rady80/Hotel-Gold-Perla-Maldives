from django import forms
from .models import Room, Booking, Dependees


# ------------------------------
# Formulář pro úpravu pokojů
# ------------------------------
class EditRoomForm(forms.ModelForm):
    """
    Formulář pro úpravu údajů o pokojích.
    """
    class Meta:
        model = Room  # Model reprezentující pokoje
        fields = ["capacity", "numberOfBeds", "roomType", "price"]  # Pole, která lze editovat
        labels = {
            'capacity': 'Kapacita pokoje',  # Popis pole kapacity
            'numberOfBeds': 'Počet postelí',  # Popis pole počtu postelí
            'roomType': 'Typ pokoje',  # Popis pole typu pokoje
            'price': 'Cena za noc (Kč)',  # Popis pole ceny
        }
        widgets = {
            'capacity': forms.NumberInput(attrs={
                'class': 'form-control', 'placeholder': 'Zadejte kapacitu pokoje'
            }),
            'numberOfBeds': forms.NumberInput(attrs={
                'class': 'form-control', 'placeholder': 'Zadejte počet postelí'
            }),
            'roomType': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Např. Deluxe, Standard'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control', 'placeholder': 'Cena v Kč za noc'
            }),
        }

    def clean_capacity(self):
        """
        Validace kapacity pokoje.
        """
        capacity = self.cleaned_data.get("capacity")
        if capacity < 1:
            raise forms.ValidationError("Kapacita pokoje musí být alespoň 1.")
        return capacity

    def clean_price(self):
        """
        Validace ceny pokoje.
        """
        price = self.cleaned_data.get("price")
        if price <= 0:
            raise forms.ValidationError("Cena musí být kladné číslo.")
        return price


# ------------------------------
# Formulář pro úpravu rezervací
# ------------------------------
class EditBookingForm(forms.ModelForm):
    """
    Formulář pro úpravu rezervací.
    """
    class Meta:
        model = Booking  # Model reprezentující rezervace
        fields = ["startDate", "endDate"]  # Pole, která lze editovat
        labels = {
            'startDate': 'Datum začátku rezervace',
            'endDate': 'Datum konce rezervace',
        }
        widgets = {
            'startDate': forms.DateInput(attrs={
                'class': 'form-control', 'type': 'date'
            }),
            'endDate': forms.DateInput(attrs={
                'class': 'form-control', 'type': 'date'
            }),
        }

    def clean(self):
        """
        Dodatečná validace pro začátek a konec rezervace.
        """
        cleaned_data = super().clean()
        start_date = cleaned_data.get("startDate")
        end_date = cleaned_data.get("endDate")

        if start_date and end_date and start_date >= end_date:
            raise forms.ValidationError("Datum konce rezervace musí být později než datum začátku.")
        return cleaned_data


# ------------------------------
# Formulář pro správu závislých osob
# ------------------------------
class EditDependeesForm(forms.ModelForm):
    """
    Formulář pro úpravu údajů o závislých osobách.
    """
    class Meta:
        model = Dependees  # Model reprezentující závislé osoby
        fields = ["booking", "name", "relation"]  # Pole, která lze editovat
        labels = {
            'booking': 'Rezervace',
            'name': 'Jméno osoby',
            'relation': 'Vztah k hostovi',
        }
        widgets = {
            'booking': forms.Select(attrs={
                'class': 'form-control'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Zadejte jméno osoby'
            }),
            'relation': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Např. Manžel, Dcera, Syn'
            }),
        }

    def clean_name(self):
        """
        Validace jména osoby.
        """
        name = self.cleaned_data.get("name")
        if len(name) < 2:
            raise forms.ValidationError("Jméno musí mít alespoň 2 znaky.")
        return name