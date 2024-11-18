from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Room, CleaningRecord, Booking  # Import relevantních modelů


@receiver(post_save, sender=Room)
def log_room_update(sender, instance, created, **kwargs):
    """
    Logování událostí spojených s pokoji (vytvoření nebo aktualizace).
    
    Parametry:
    - sender: Model, který spustil signál (v tomto případě Room).
    - instance: Instance modelu Room, která byla vytvořena nebo aktualizována.
    - created: Boolean označující, zda byla instance nově vytvořena.
    """
    if created:
        print(f"Nový pokoj vytvořen: {instance.name} (číslo: {instance.number})")
    else:
        print(f"Pokoj {instance.name} (číslo: {instance.number}) byl aktualizován.")


@receiver(post_save, sender=Room)
def create_cleaning_record(sender, instance, created, **kwargs):
    """
    Vytvoření výchozího záznamu úklidu po vytvoření nového pokoje.
    
    Parametry:
    - sender: Model, který spustil signál (v tomto případě Room).
    - instance: Instance modelu Room, která byla vytvořena.
    - created: Boolean označující, zda byla instance nově vytvořena.
    """
    if created:  # Pokud je pokoj nově vytvořen
        CleaningRecord.objects.create(room=instance, status="Ready")
        print(f"Byl vytvořen výchozí záznam úklidu pro pokoj {instance.name}.")


@receiver(post_delete, sender=Room)
def delete_related_bookings(sender, instance, **kwargs):
    """
    Odstranění všech rezervací spojených s pokojem po jeho smazání.
    
    Parametry:
    - sender: Model, který spustil signál (v tomto případě Room).
    - instance: Instance modelu Room, která byla smazána.
    """
    related_bookings = Booking.objects.filter(room=instance)
    count = related_bookings.count()
    related_bookings.delete()
    print(f"Bylo odstraněno {count} rezervací spojených s pokojem {instance.name} (číslo:  {instance.number}).")