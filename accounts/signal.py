# accounts/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Employee

@receiver(post_save, sender=User)
def create_employee_profile(sender, instance, created, **kwargs):
    """
    Signál pro vytvoření profilu zaměstnance.
    Při vytvoření nového uživatele (User) automaticky vytvoří záznam zaměstnance (Employee)
    s výchozí hodnotou platu 0.00.
    """