import logging
from django.apps import AppConfig

# Nastavení loggeru pro aplikaci
logger = logging.getLogger(__name__)

class AccountsConfig(AppConfig):
    """
    Konfigurace aplikace 'accounts'.
    Třída zajišťuje nastavení aplikace a inicializační logiku.
    """
    # Výchozí nastavení primárního klíče v modelech
    default_auto_field = 'django.db.models.BigAutoField'
    # Název aplikace (odpovídá názvu složky aplikace)
    name = 'accounts'

    def ready(self):
        """
        Metoda, která se volá při inicializaci aplikace.
        Používá se k registraci signálů nebo jiných funkcí, které
        mají být spuštěny při startu aplikace.
        """
        try:
            # Importuje soubor se signály (accounts/signals.py)
            import accounts.signals
        except ImportError as e:
            # Zaznamenání varování do logu při chybě načítání signálů
            logger.warning(f"Chyba při načítání signálů: {e}")
