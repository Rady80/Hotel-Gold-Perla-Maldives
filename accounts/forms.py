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
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
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
            'phoneNumber': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'salary': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Salary'}),
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
            'phoneNumber': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'salary': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Salary'}),
        }


# Formulář pro úpravu uživatele (User)
class EditUserForm(ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        }


# Formulář pro úpravu hosta (Guest)
class EditGuestForm(ModelForm):
    class Meta:
        model = Guest
        fields = ["phoneNumber"]
        widgets = {
            'phoneNumber': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
        }


# Formulář pro výběr role
class ROLES(Form):
    ROLES_TYPES = [
        ('manager', 'Manager'),
        ('receptionist', 'Receptionist'),
        ('staff', 'Staff'),
    ]
    ROLES_TYPES = ChoiceField(
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        choices=ROLES_TYPES,
        label="Role"
    )