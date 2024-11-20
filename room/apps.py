from django.apps import AppConfig
from django.core.exceptions import ImproperlyConfigured


class RoomConfig(AppConfig):
    """
    Konfigurace aplikace 'room' pro Django projekt.

    Tento soubor definuje základní nastavení aplikace 'room', včetně jejího názvu,
    popisu a inicializační logiky při spuštění aplikace.
    """
    # ------------------------------
    # Výchozí nastavení aplikace
    # ------------------------------
    
    # Výchozí typ primárního klíče pro modely v této aplikaci
    default_auto_field = 'django.db.models.BigAutoField'
    
    # Název aplikace, jak je registrována v Django projektu
    name = 'room'
    
    # Přátelský název aplikace, který se zobrazuje v administraci
    verbose_name = "Pokoje a správa"

    # ------------------------------
    # Inicializační logika při spuštění aplikace
    # ------------------------------
    def ready(self):
        """
        Inicializační logika aplikace při jejím spuštění.

        Tato metoda se volá automaticky během startu Django aplikace. Její hlavní úlohou je:
        - Načítat a registrovat signály aplikace (definované v `room/signals.py`).
        - Zajistit, že všechny potřebné komponenty aplikace jsou správně inicializovány.

        Pokud se při importu signálů vyskytne chyba, metoda vyvolá výjimku
        `ImproperlyConfigured`, která poskytuje detailní informace o problému.
        """
        try:
            # Pokus o import signálů aplikace z modulu `room.signals`
            import room.signals
        except ImportError as e:
            # Pokud se import nezdaří, vyvolá se výjimka s podrobnou chybovou zprávou
            raise ImproperlyConfigured(
                f"Chyba při načítání signálů aplikace 'room': {e}"
            )