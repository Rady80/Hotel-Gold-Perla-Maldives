from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Event, EventAttendees, Storage
from accounts.models import Guest
import logging

# Nastavení loggeru pro ladění
logger = logging.getLogger(__name__)


# ------------------------------
# Signál pro vytvoření logu při uložení nebo změně události
# ------------------------------
@receiver(post_save, sender=Event)
def log_event_creation_or_update(sender, instance, created, **kwargs):
    """
    Signál pro logování vytvoření nebo aktualizace události.
    Spouští se pokaždé, když je instance modelu Event vytvořena nebo změněna.

    Parametry:
    - sender: Model, který spustil signál (Event).
    - instance: Instance modelu Event, která byla vytvořena nebo aktualizována.
    - created: Boolean označující, zda byla instance nově vytvořena.
    """
    if created:
        logger.info(f"Nová událost vytvořena: {instance.eventType} v {instance.location}.")
    else:
        logger.info(f"Událost aktualizována: {instance.eventType} v {instance.location}.")


# ------------------------------
# Signál pro odstranění účastníků události při odstranění události
# ------------------------------
@receiver(post_delete, sender=Event)
def delete_event_attendees(sender, instance, **kwargs):
    """
    Signál pro odstranění účastníků události při jejím smazání.
    Spouští se při odstranění instance modelu Event.

    Parametry:
    - sender: Model, který spustil signál (Event).
    - instance: Instance modelu Event, která byla odstraněna.
    """
    attendees = EventAttendees.objects.filter(event=instance)
    count = attendees.count()
    attendees.delete()
    logger.info(f"Odstraněno {count} účastníků z události: {instance.eventType}.")


# ------------------------------
# Signál pro kontrolu skladového množství po změně skladu
# ------------------------------
@receiver(post_save, sender=Storage)
def check_storage_quantity(sender, instance, **kwargs):
    """
    Signál pro kontrolu skladového množství.
    Spouští se po každém uložení instance modelu Storage.

    Parametry:
    - sender: Model, který spustil signál (Storage).
    - instance: Instance modelu Storage, která byla vytvořena nebo aktualizována.
    """
    if instance.quantity < 10:
        logger.warning(f"Nízké množství položky '{instance.itemName}': {instance.quantity} ks.")


# ------------------------------
# Signál pro vytvoření výchozího záznamu účastníka při přidání události
# ------------------------------
@receiver(post_save, sender=Guest)
def create_event_attendance_for_guest(sender, instance, created, **kwargs):
    """
    Signál pro automatické vytvoření výchozího záznamu účasti na události při registraci nového hosta.
    Spouští se při vytvoření instance modelu Guest.

    Parametry:
    - sender: Model, který spustil signál (Guest).
    - instance: Instance modelu Guest, která byla vytvořena.
    - created: Boolean označující, zda byla instance nově vytvořena.
    """
    if created:
        event = Event.objects.first()  # Získání první události (pro ukázkové účely)
        if event:
            EventAttendees.objects.create(event=event, guest=instance, numberOfDependees=0)
            logger.info(f"Host {instance.user.username} přidán na událost '{event.eventType}'.")