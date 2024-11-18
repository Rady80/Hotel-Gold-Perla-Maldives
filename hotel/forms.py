from django import forms
from django.forms import ModelForm
from .models import FoodMenu, Event, Announcement, Storage


class EditFoodMenuForm(ModelForm):
    """
    Formulář pro úpravu jídelního menu.
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
            "itemType": forms.Select(attrs={"class": "form-control"}),
            "quantity": forms.NumberInput(attrs={"class": "form-control"}),
        }
