from django.apps import AppConfig

class AccountsConfig(AppConfig):
    """
    Konfigurace aplikace 'accounts'.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        """
        Registrace signálů při startu aplikace.
        """
        try:
            import accounts.signals  # Import signálů
        except ImportError:
            pass  # Pokud signály neexistují, chyba se ignoruje