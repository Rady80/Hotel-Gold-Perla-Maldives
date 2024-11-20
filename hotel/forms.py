from django import forms
from django.forms import ModelForm
from .models import FoodMenu, Event, Announcement, Storage


# ------------------------------
# Formulář pro úpravu jídelního menu
# ------------------------------
class EditFoodMenuForm(ModelForm):
    """
    Formulář pro úpravu jídelního menu.
    Umožňuje editovat položky menu.
    """
    class Meta:
        model = FoodMenu
        fields = ['name', 'description', 'price', 'category']  # Pole definovaná v modelu
        labels = {
            "name": "Název jídla",
            "description": "Popis jídla",
            "price": "Cena",
            "category": "Kategorie",
        }
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "price": forms.NumberInput(attrs={"class": "form-control"}),
            "category": forms.TextInput(attrs={"class": "form-control"}),
        }


# ------------------------------
# Formulář pro vytvoření nové události
# ------------------------------
class CreateEventForm(ModelForm):
    """
    Formulář pro vytvoření nové události.
    """
    class Meta:
        model = Event
        fields = ['title', 'event_type', 'location', 'start_date', 'end_date', 'description']
        labels = {
            "title": "Název události",
            "event_type": "Typ události",
            "location": "Místo konání",
            "start_date": "Datum začátku",
            "end_date": "Datum konce",
            "description": "Popis události",
        }
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "event_type": forms.Select(attrs={"class": "form-control"}),  # Výběrový seznam
            "location": forms.TextInput(attrs={"class": "form-control"}),
            "start_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "end_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
        }


# ------------------------------
# Formulář pro úpravu událostí
# ------------------------------
class EditEventForm(ModelForm):
    """
    Formulář pro úpravu událostí.
    """
    class Meta:
        model = Event
        fields = ['title', 'event_type', 'location', 'start_date', 'end_date', 'description']
        labels = {
            "title": "Název události",
            "event_type": "Typ události",
            "location": "Místo konání",
            "start_date": "Datum začátku",
            "end_date": "Datum konce",
            "description": "Popis události",
        }
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "event_type": forms.Select(attrs={"class": "form-control"}),  # Výběrový seznam
            "location": forms.TextInput(attrs={"class": "form-control"}),
            "start_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "end_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
        }
        

# ------------------------------
# Formulář pro vytvoření oznámení
# ------------------------------
class CreateAnnouncementForm(ModelForm):
    """
    Formulář pro vytvoření oznámení.
    """
    class Meta:
        model = Announcement
        fields = ["title", "content"]
        labels = {
            "title": "Nadpis oznámení",
            "content": "Obsah oznámení",
        }
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
        }


# ------------------------------
# Formulář pro vytvoření položky ve skladu
# ------------------------------
class CreateItemForm(ModelForm):
    """
    Formulář pro vytvoření položky ve skladu.
    """
    class Meta:
        model = Storage
        fields = ["item_name", "quantity"]
        labels = {
            "item_name": "Název položky",
            "quantity": "Množství na skladě",
        }
        widgets = {
            "item_name": forms.TextInput(attrs={"class": "form-control"}),
            "quantity": forms.NumberInput(attrs={"class": "form-control"}),  # Číselný vstup
        }