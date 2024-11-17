from django.apps import AppConfig

class RoomConfig(AppConfig):
    """
    Konfigurace aplikace 'room'.
    """
    default_auto_field = 'django.db.models.BigAutoField'  # Výchozí typ primárního klíče pro modely
    name = 'room'  # Název aplikace, kterou Django registruje

    def ready(self):
        """
        Registrace signálů při startu aplikace.
        """
        try:
            import room.signals  # Importuje signály z room/signals.py
        except ImportError:
            # Pokud signály neexistují nebo obsahují chybu, ignoruje import
            pass