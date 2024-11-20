from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from room.models import Room, Booking

# ------------------------------
# Logování aktualizace nebo vytvoření pokoje
# ------------------------------
@receiver(post_save, sender=Room)
def log_room_update(sender, instance, created, **kwargs):
    """
    Logování událostí spojených s pokoji (vytvoření nebo aktualizace).

    - created: True, pokud byl pokoj právě vytvořen.
    """
    if created:
        # Logování nového pokoje
        print(f"Nový pokoj vytvořen: {instance.name} (číslo: {instance.number})")
    else:
        # Logování aktualizace pokoje
        print(f"Pokoj {instance.name} (číslo: {instance.number}) byl aktualizován.")

# ------------------------------
# Vytvoření záznamu úklidu při vytvoření nového pokoje
# ------------------------------
@receiver(post_save, sender=Room)
def create_cleaning_record(sender, instance, created, **kwargs):
    """
    Automatické vytvoření záznamu úklidu při vytvoření nového pokoje.
    """
    if created:
        from room.models import CleaningRecord  # Import pro záznamy úklidu (předcházení cyklickým importům)
        CleaningRecord.objects.create(
            room=instance, cleaner_name="Nepřiřazen", notes="Počáteční úklid"
        )
        print(f"Byl vytvořen výchozí záznam úklidu pro pokoj {instance.name}.")

# ------------------------------
# Odstranění rezervací při smazání pokoje
# ------------------------------
@receiver(post_delete, sender=Room)
def delete_related_bookings(sender, instance, **kwargs):
    """
    Automatické odstranění všech rezervací při smazání pokoje.
    """
    related_bookings = Booking.objects.filter(room=instance)  # Vyhledání rezervací spojených s pokojem
    count = related_bookings.count()  # Počet rezervací
    related_bookings.delete()  # Smazání všech nalezených rezervací
    print(f"Bylo odstraněno {count} rezervací spojených s pokojem {instance.name} (číslo: {instance.number}).")

# ------------------------------
# Logování vytvoření nové rezervace
# ------------------------------
@receiver(post_save, sender=Booking)
def log_booking_creation(sender, instance, created, **kwargs):
    """
    Logování vytvoření nové rezervace.
    """
    if created:
        print(f"Nová rezervace vytvořena pro pokoj {instance.room.number} - {instance.guest.user.username}.")

# ------------------------------
# Aktualizace stavu pokoje při vytvoření nové rezervace
# ------------------------------
@receiver(post_save, sender=Booking)
def update_room_status(sender, instance, created, **kwargs):
    """
    Automatické označení pokoje jako obsazeného při vytvoření rezervace.
    """
    if created:
        instance.room.status = 'Occupied'  # Nastavení stavu pokoje na "Obsazené"
        instance.room.save()  # Uložení změn v databázi
        print(f"Pokoj {instance.room.number} byl označen jako obsazený.")

# ------------------------------
# Uvolnění pokoje při smazání rezervace
# ------------------------------
@receiver(post_delete, sender=Booking)
def free_room_on_booking_delete(sender, instance, **kwargs):
    """
    Automatické označení pokoje jako dostupného po smazání rezervace.
    """
    instance.room.status = 'Available'  # Nastavení stavu pokoje na "Dostupné"
    instance.room.save()  # Uložení změn v databázi
    print(f"Pokoj {instance.room.number} byl označen jako dostupný po smazání rezervace.")