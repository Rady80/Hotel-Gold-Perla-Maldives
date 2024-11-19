from django.apps import AppConfig
from django.core.exceptions import ImproperlyConfigured

class RoomConfig(AppConfig):
    """
    Konfigurace aplikace 'room' pro Django projekt.

    Tento soubor definuje nastavení pro aplikaci 'room', včetně inicializace aplikace a
    registrace signálů během spuštění.
    """
    default_auto_field = 'django.db.models.BigAutoField'  # Výchozí typ primárního klíče pro modely (automaticky generovaný)
    name = 'room'  # Název aplikace, jak je registrován v Django projektu
    verbose_name = "Pokoje a správa"  # Přátelský název aplikace pro administraci

    def ready(self):
        """
        Inicializační logika aplikace při jejím spuštění.

        Tato metoda je volána automaticky během startu Django aplikace. Slouží k registraci
        signálů aplikace, které umožňují provádět určité akce při událostech, jako je
        vytvoření nebo smazání objektů.

        Pokud dojde k chybě při importu signálů, vyvoláme výjimku s popisem chyby.
        """
        try:
            # Pokus o importování signálů aplikace z `room/signals.py`
            import room.signals  # Tento soubor je zodpovědný za registraci signálů
        except ImportError as e:
            # Pokud dojde k chybě při načítání signálů, vyvoláme výjimku a poskytneme detailní informaci
            raise ImproperlyConfigured(
                f"Chyba při načítání signálů aplikace 'room': {e}"  # Poskytuje podrobnosti o chybě
            )