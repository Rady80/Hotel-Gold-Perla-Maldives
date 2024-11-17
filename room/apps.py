from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class RoomConfig(AppConfig):
    """
    Konfigurace aplikace 'room'.
    """
    default_auto_field = 'django.db.models.BigAutoField'  # Nastavení výchozího pole ID pro modely
    name = 'room'  # Název aplikace
    verbose_name = _('Správa pokojů')  # Přátelský název aplikace pro administraci

    def ready(self):
        """
        Metoda, která se spouští při inicializaci aplikace.
        Zde můžete například registrovat signály.
        """
        import room.signals  # Zajistěte, že existují signály v `room/signals.py`