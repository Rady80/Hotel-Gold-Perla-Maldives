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

    Parametry:
    - sender: Model, který signál vyvolal (v tomto případě User).
    - instance: Instance modelu User, která byla vytvořena nebo aktualizována.
    - created: Boolean označující, zda byla instance vytvořena (True) nebo aktualizována (False).
    - kwargs: Další parametry signálu.
    """
    if created:
        Employee.objects.create(user=instance, phoneNumber="", salary=0.00)
        print(f"Byl vytvořen profil zaměstnance pro uživatele {instance.username}.")