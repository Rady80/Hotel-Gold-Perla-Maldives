from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from room.models import Room  # Importujeme pouze Room pro naše signály

# ------------------------------
# Logování aktualizace nebo vytvoření pokoje
# ------------------------------
@receiver(post_save, sender='room.Room')  # Použití řetězcového odkazu pro Room
def log_room_update(sender, instance, created, **kwargs):
    """
    Logování událostí spojených s pokoji (vytvoření nebo aktualizace).
    """
    if created:
        # Pokud byl pokoj právě vytvořen, logujeme tuto událost
        print(f"Nový pokoj vytvořen: {instance.name} (číslo: {instance.number})")
    else:
        # Pokud byl pokoj aktualizován, logujeme tuto změnu
        print(f"Pokoj {instance.name} (číslo: {instance.number}) byl aktualizován.")

# ------------------------------
# Vytvoření záznamu úklidu při vytvoření nového pokoje
# ------------------------------
@receiver(post_save, sender='room.Room')  # Používáme řetězcový odkaz pro Room
def create_cleaning_record(sender, instance, created, **kwargs):
    """
    Vytvoření výchozího záznamu úklidu po vytvoření nového pokoje.
    """
    if created:  # Pokud je pokoj nově vytvořen
        from room.models import CleaningRecord  # Importujeme zde, abychom předešli kruhovému importu
        CleaningRecord.objects.create(room=instance, cleaner_name="Unknown", notes="Initial cleaning")
        # Po vytvoření pokoje automaticky vytvoříme výchozí záznam úklidu
        print(f"Byl vytvořen výchozí záznam úklidu pro pokoj {instance.name}.")

# ------------------------------
# Odstranění rezervací při smazání pokoje
# ------------------------------
@receiver(post_delete, sender='room.Room')  # Používáme řetězcový odkaz pro Room
def delete_related_bookings(sender, instance, **kwargs):
    """
    Odstranění všech rezervací spojených s pokojem po jeho smazání.
    """
    from room.models import Booking  # Importujeme Booking až zde, aby nedošlo k cyklickému importu
    related_bookings = Booking.objects.filter(room=instance)  # Najdeme všechny rezervace spojené s tímto pokojem
    count = related_bookings.count()  # Spočítáme počet těchto rezervací
    related_bookings.delete()  # Smažeme všechny nalezené rezervace
    # Vypíšeme informaci o počtu odstraněných rezervací
    print(f"Bylo odstraněno {count} rezervací spojených s pokojem {instance.name} (číslo: {instance.number}).")

# ------------------------------
# Logování vytvoření nové rezervace
# ------------------------------
@receiver(post_save, sender='room.Booking')  # Použití řetězcového odkazu pro Booking
def log_booking_creation(sender, instance, created, **kwargs):
    """
    Logování vytvoření nové rezervace.
    """
    if created:  # Pokud je rezervace nově vytvořena
        print(f"Nová rezervace vytvořena pro pokoj {instance.room.number} - {instance.guest_name}.")
    # Vytiskneme informaci o nové rezervaci

# ------------------------------
# Aktualizace stavu pokoje při vytvoření nové rezervace
# ------------------------------
@receiver(post_save, sender='room.Booking')  # Použití řetězcového odkazu pro Booking
def update_room_status(sender, instance, created, **kwargs):
    """
    Aktualizace stavu pokoje při vytvoření nové rezervace.
    """
    if created:  # Pokud je rezervace nově vytvořena
        instance.room.status = 'Occupied'  # Označení pokoje jako obsazený
        instance.room.save()  # Uložíme změny stavu pokoje
        # Vytiskneme informaci o změně stavu pokoje
        print(f"Pokoj {instance.room.number} byl označen jako obsazený.")