from django.apps import AppConfig


class RoomConfig(AppConfig):
    """
    Konfigurace aplikace 'room'.
    Obsahuje nastavení pro správu aplikace a její inicializaci.
    """
    default_auto_field = 'django.db.models.BigAutoField'  # Výchozí typ primárního klíče pro modely
    name = 'room'  # Název aplikace registrované v Django projektu
    verbose_name = "Pokoje a správa"  # Čitelný název aplikace v administraci

    def ready(self):
        """
        Provádí inicializační kroky při spuštění aplikace, jako je registrace signálů.
        """
        try:
            import room.signals  # Importuje signály z room/signals.py
        except ImportError as e:
            # Pokud signály neexistují nebo obsahují chybu, zaloguje chybu
            from django.core.exceptions import ImproperlyConfigured
            raise ImproperlyConfigured(f"Chyba při načítání signálů aplikace 'room': {e}")