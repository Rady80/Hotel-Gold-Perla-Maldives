from django.forms import ModelForm, Form, ChoiceField
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Employee, Guest

# Formulář pro vytvoření uživatele (User)
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Uživatelské jméno'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Jméno'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Příjmení'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'E-mail'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Heslo'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Potvrzení hesla'}),
        }
        help_texts = {
            'username': 'Můžete použít písmena, čísla a @/./+/-/_',
        }

# Formulář pro vytvoření zaměstnance (Employee)
class CreateEmployeeForm(ModelForm):
    class Meta:
        model = Employee
        fields = ['phoneNumber', 'salary']
        widgets = {
            'phoneNumber': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefonní číslo'}),
            'salary': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Plat'}),
        }

    def clean_phoneNumber(self):
        phoneNumber = self.cleaned_data.get('phoneNumber')
        if len(phoneNumber) < 10:
            raise forms.ValidationError("Telefonní číslo musí mít minimálně 10 číslic.")
        return phoneNumber

# Formulář pro úpravu zaměstnance
class EditEmployeeForm(ModelForm):
    class Meta:
        model = Employee
        fields = ["phoneNumber", "salary"]
        widgets = {
            'phoneNumber': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefonní číslo'}),
            'salary': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Plat'}),
        }

# Formulář pro úpravu uživatele (User)
class EditUserForm(ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Jméno'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Příjmení'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'E-mail'}),
        }

# Formulář pro úpravu hosta (Guest)
class EditGuestForm(ModelForm):
    class Meta:
        model = Guest
        fields = ["phoneNumber"]
        widgets = {
            'phoneNumber': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefonní číslo'}),
        }

# Formulář pro výběr role
class RoleSelectionForm(Form):
    ROLE_CHOICES = [
        ('manager', 'Manažer'),
        ('receptionist', 'Recepční'),
        ('staff', 'Personál'),
    ]
    role = ChoiceField(
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        choices=ROLE_CHOICES,
        label="Role"
    )