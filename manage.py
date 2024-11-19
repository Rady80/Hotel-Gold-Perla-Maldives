#!/usr/bin/env python
"""
Hlavní skript pro administrativní úlohy Django projektu.

Tento soubor slouží k interakci s Django projektem z příkazového řádku.
Můžete jej použít pro spuštění serveru, migrace databáze, správu aplikací a další.
"""

import os
import sys


def main():
    """
    Spustí administrativní úlohy.

    Tento kód nastaví výchozí konfiguraci projektu Django a zpracuje příkazy
    zadané uživatelem prostřednictvím příkazového řádku.
    """
    # Nastavení výchozího konfiguračního modulu pro Django projekt
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HMS.settings')
    try:
        # Importuje funkci pro spouštění příkazů Django
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Pokud Django není dostupné, vyvolá chybu s vysvětlením
        raise ImportError(
            "Nepodařilo se importovat Django. Je nainstalované a dostupné na "
            "PYTHONPATH? Nezapomněli jste aktivovat virtuální prostředí?"
        ) from exc
    # Spustí příkazy zadané z příkazového řádku
    execute_from_command_line(sys.argv)


# Hlavní bod spuštění skriptu
if __name__ == '__main__':
    main()