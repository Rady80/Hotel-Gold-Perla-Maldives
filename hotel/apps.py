from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class HotelConfig(AppConfig):
    """
    Konfigurace aplikace 'hotel'.
    """
    default_auto_field = 'django.db.models.BigAutoField'  # Nastavení výchozího pole ID pro modely
    name = 'hotel'  # Název aplikace
    verbose_name = _('Správa hotelu')  # Přátelský název aplikace pro administraci (s lokalizací)

    def ready(self):
        """
        Inicializace aplikace při startu Django, například registrace signálů.
        """
        try:
            import hotel.signals  # Registrace signálů
        except ImportError:
            # Pokud signály nejsou potřeba nebo soubor neexistuje, chyba je ignorována
            pass