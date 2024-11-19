from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _
import logging

# Nastavení loggeru pro aplikaci 'hotel'
logger = logging.getLogger(__name__)


class HotelConfig(AppConfig):
    """
    Konfigurace aplikace 'hotel'.
    Tato třída obsahuje základní nastavení a inicializaci aplikace.
    """
    default_auto_field = 'django.db.models.BigAutoField'  # Výchozí typ primárního klíče pro modely
    name = 'hotel'  # Název aplikace (odpovídá názvu složky aplikace)
    verbose_name = _('Správa hotelu')  # Přátelský název aplikace v administraci (s podporou lokalizace)

    def ready(self):
        """
        Inicializace aplikace při startu Django.

        Používá se například pro:
        - Registraci signálů
        - Nastavení specifických procesů při spuštění aplikace
        """
        try:
            import hotel.signals  # Registrace signálů (pokud existují)
            logger.info("Signály aplikace 'hotel' byly úspěšně načteny.")
        except ImportError as e:
            # Pokud soubor se signály neexistuje, zaznamenáme varování
            logger.warning(f"Soubor 'hotel.signals' nebyl nalezen: {e}")