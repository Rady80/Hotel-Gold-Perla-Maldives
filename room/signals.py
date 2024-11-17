from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Room, CleaningRecord, Booking  # Import relevantních modelů

# Signál pro logování vytvoření nebo aktualizace pokoje
@receiver(post_save, sender=Room)
def log_room_update(sender, instance, created, **kwargs):
    """
    Logování, když je pokoj vytvořen nebo aktualizován.
    
    Parametry:
    - sender: Model, který spustil signál (v tomto případě Room).
    - instance: Konkrétní instance modelu Room.
    - created: Boolean označující, zda byla instance nově vytvořena.
    """
    if created:
        print(f"Nový pokoj vytvořen: {instance.name}")  # Log zpráva při vytvoření
    else:
        print(f"Pokoj {instance.name} byl aktualizován.")  # Log zpráva při aktualizaci


# Signál pro vytvoření výchozího záznamu úklidu při vytvoření pokoje
@receiver(post_save, sender=Room)
def create_cleaning_record(sender, instance, created, **kwargs):
    """
    Vytvoření výchozího záznamu úklidu po vytvoření nového pokoje.
    
    Parametry:
    - sender: Model, který spustil signál (v tomto případě Room).
    - instance: Konkrétní instance modelu Room.
    - created: Boolean označující, zda byla instance nově vytvořena.
    """
    if created:  # Kontrola, zda byl pokoj právě vytvořen
        CleaningRecord.objects.create(room=instance, status="Ready")  # Vytvoření záznamu úklidu


# Signál pro odstranění rezervací spojených s pokojem při jeho smazání
@receiver(post_delete, sender=Room)
def delete_related_bookings(sender, instance, **kwargs):
    """
    Odstranění všech rezervací spojených s pokojem po jeho smazání.
    
    Parametry:
    - sender: Model, který spustil signál (v tomto případě Room).
    - instance: Konkrétní instance modelu Room.
    """
    Booking.objects.filter(room=instance).delete()  # Odstranění všech rezervací souvisejících s daným pokojem
