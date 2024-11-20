from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Event, EventAttendees, Storage
from accounts.models import Guest
import logging

# ------------------------------
# Nastavení loggeru
# ------------------------------
logger = logging.getLogger(__name__)


# ------------------------------
# Signál: Logování vytvoření nebo aktualizace události
# ------------------------------
@receiver(post_save, sender=Event)
def log_event_creation_or_update(sender, instance, created, **kwargs):
    """
    Loguje vytvoření nebo aktualizaci události.

    Parametry:
    - sender: Model, který spustil signál (Event).
    - instance: Instance modelu Event.
    - created: True, pokud byla instance nově vytvořena; jinak False.
    """
    if created:
        logger.info(f"Nová událost vytvořena: {instance.eventType} na lokaci {instance.location}.")
    else:
        logger.info(f"Událost aktualizována: {instance.eventType} na lokaci {instance.location}.")


# ------------------------------
# Signál: Odstranění účastníků při smazání události
# ------------------------------
@receiver(post_delete, sender=Event)
def delete_event_attendees(sender, instance, **kwargs):
    """
    Odstraňuje účastníky přidružené k odstraněné události.

    Parametry:
    - sender: Model, který spustil signál (Event).
    - instance: Instance modelu Event, která byla odstraněna.
    """
    attendees = EventAttendees.objects.filter(event=instance)
    count = attendees.count()
    attendees.delete()
    logger.info(f"Odstraněno {count} účastníků z události: {instance.eventType}.")


# ------------------------------
# Signál: Kontrola skladového množství
# ------------------------------
@receiver(post_save, sender=Storage)
def check_storage_quantity(sender, instance, **kwargs):
    """
    Kontroluje skladové množství a loguje upozornění při nízké úrovni zásob.

    Parametry:
    - sender: Model, který spustil signál (Storage).
    - instance: Instance modelu Storage.
    """
    if instance.quantity < 10:
        logger.warning(f"Nízké množství položky '{instance.itemName}': {instance.quantity} ks.")


# ------------------------------
# Signál: Automatické přidání hosta na událost
# ------------------------------
@receiver(post_save, sender=Guest)
def create_event_attendance_for_guest(sender, instance, created, **kwargs):
    """
    Při registraci nového hosta automaticky přidává hosta na první dostupnou událost.

    Parametry:
    - sender: Model, který spustil signál (Guest).
    - instance: Instance modelu Guest.
    - created: True, pokud byla instance nově vytvořena; jinak False.
    """
    if created:
        # Výběr první dostupné události
        event = Event.objects.first()
        if event:
            # Vytvoření účasti hosta na události
            EventAttendees.objects.create(event=event, guest=instance, numberOfDependees=0)
            logger.info(f"Host {instance.user.username} automaticky přidán na událost '{event.eventType}'.")
        else:
            logger.warning(f"Není dostupná žádná událost pro hosta {instance.user.username}.")