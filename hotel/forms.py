from django import forms
from django.forms import ModelForm
from .models import FoodMenu, Event, Announcement, Storage


class EditFoodMenuForm(ModelForm):
    """
    Formulář pro úpravu jídelního menu.
    Umožňuje editovat položky menu a nastavit období platnosti.
    """
    class Meta:
        model = FoodMenu
        fields = ["menuItems", "startDate", "endDate"]
        labels = {
            "menuItems": "Položky menu",
            "startDate": "Datum začátku",
            "endDate": "Datum konce",
        }
        widgets = {
            "menuItems": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "startDate": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "endDate": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
        }


class EditEventForm(ModelForm):
    """
    Formulář pro úpravu událostí.
    Umožňuje upravit typ, místo, období a další detaily události.
    """
    class Meta:
        model = Event
        fields = ["eventType", "location", "startDate", "endDate", "explanation"]
        labels = {
            "eventType": "Typ události",
            "location": "Místo",
            "startDate": "Datum začátku",
            "endDate": "Datum konce",
            "explanation": "Vysvětlení",
        }
        widgets = {
            "eventType": forms.TextInput(attrs={"class": "form-control"}),
            "location": forms.TextInput(attrs={"class": "form-control"}),
            "startDate": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "endDate": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "explanation": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
        }


class CreateEventForm(ModelForm):
    """
    Formulář pro vytvoření nové události.
    Zahrnuje typ, místo, datumy a vysvětlení.
    """
    class Meta:
        model = Event
        fields = ["eventType", "location", "startDate", "endDate", "explanation"]
        labels = {
            "eventType": "Typ události",
            "location": "Místo",
            "startDate": "Datum začátku",
            "endDate": "Datum konce",
            "explanation": "Vysvětlení",
        }
        widgets = {
            "eventType": forms.TextInput(attrs={"class": "form-control"}),
            "location": forms.TextInput(attrs={"class": "form-control"}),
            "startDate": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "endDate": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "explanation": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
        }


class CreateAnnouncementForm(ModelForm):
    """
    Formulář pro vytvoření oznámení.
    Obsahuje nadpis, obsah a datum vytvoření.
    """
    class Meta:
        model = Announcement
        fields = ["title", "content", "date_created"]
        labels = {
            "title": "Nadpis",
            "content": "Obsah",
            "date_created": "Datum vytvoření",
        }
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
            "date_created": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
        }


class CreateItemForm(ModelForm):
    """
    Formulář pro vytvoření položky ve skladu.
    Umožňuje zadat název, typ a množství položky.
    """
    class Meta:
        model = Storage
        fields = ["itemName", "itemType", "quantity"]
        labels = {
            "itemName": "Název položky",
            "itemType": "Typ položky",
            "quantity": "Množství",
        }
        widgets = {
            "itemName": forms.TextInput(attrs={"class": "form-control"}),
            "itemType": forms.Select(attrs={"class": "form-control"}),  # Použití výběrového seznamu
            "quantity": forms.NumberInput(attrs={"class": "form-control"}),  # Číselný vstup
        }