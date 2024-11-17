from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """
    Konfigurace aplikace 'accounts'. Obsahuje základní nastavení a přátelský název aplikace pro administraci.
    """
    default_auto_field = 'django.db.models.BigAutoField'  # Automatické pole ID pro novější verze Django
    name = 'accounts'  # Název aplikace (důležité pro Django routing)
    verbose_name = 'Správa účtů'  # Přátelský název aplikace pro administraci
    
    def ready(self):
        import accounts.signals  # Registrace signálů při spuštění aplikace