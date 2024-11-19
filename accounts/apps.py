import logging
from django.apps import AppConfig

# Nastavení loggeru pro aplikaci 'accounts'
logger = logging.getLogger(__name__)

class AccountsConfig(AppConfig):
    """
    Konfigurace aplikace 'accounts'.
    Zajišťuje nastavení aplikace a inicializační logiku při startu.
    """
    # Výchozí nastavení primárního klíče pro modely v této aplikaci
    default_auto_field = 'django.db.models.BigAutoField'
    # Název aplikace (musí odpovídat názvu složky aplikace)
    name = 'accounts'

    def ready(self):
        """
        Metoda, která se volá při inicializaci aplikace.
        Používá se pro registraci signálů nebo jiných funkcí,
        které mají být spuštěny při startu aplikace.
        """
        try:
            # Import souboru se signály (accounts/signals.py)
            import accounts.signals
            logger.info("Signály aplikace 'accounts' byly úspěšně načteny.")
        except ImportError as e:
            # Pokud se signály nepodaří načíst, zaznamená chybu do logu
            logger.warning(f"Chyba při načítání signálů aplikace 'accounts': {e}")
        except Exception as e:
            # Obecné zachycení neočekávaných chyb
            logger.error(f"Neočekávaná chyba při načítání signálů: {e}")