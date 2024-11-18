from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class HotelConfig(AppConfig):
    """
    Konfigurace aplikace 'hotel'.
    """
    default_auto_field = 'django.db.models.BigAutoField'  # Výchozí pole ID pro modely
    name = 'hotel'  # Název aplikace (musí odpovídat názvu složky aplikace)
    verbose_name = _('Správa hotelu')  # Přátelský název aplikace pro administraci (s podporou lokalizace)

    def ready(self):
        """
        Inicializace aplikace při startu Django.

        Tato metoda se používá například pro:
        - Registraci signálů
        - Nastavení specifických procesů při spuštění aplikace
        """
        try:
            import hotel.signals  # Registrace signálů (pokud existují)
        except ImportError as e:
            # Pokud soubor se signály neexistuje, chyba je ignorována
            # Můžete přidat logování chyby, pokud je to vhodné pro ladění
            pass