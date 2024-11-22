from django.apps import AppConfig

class BookingsConfig(AppConfig):
    """
    Konfigurace aplikace `bookings`.
    Tato třída zajišťuje inicializaci aplikace při jejím spuštění.
    """
    default_auto_field = 'django.db.models.BigAutoField'  # Nastavení automatického ID pro modely
    name = 'bookings'  # Název aplikace

    def ready(self):
        """
        Inicializace aplikace `bookings`. 
        Připojuje signál `post_migrate`, který je použit pro vytvoření výchozích rezervací po migraci, 
        pokud žádné v databázi neexistují.
        """
        # Importujeme signály z modulu 'bookings.signals', které provedou výchozí rezervace po migraci
        import bookings.signals  # Importuje signály, které provádí výchozí rezervace po migraci