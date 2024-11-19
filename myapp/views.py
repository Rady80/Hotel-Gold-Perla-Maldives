from django.shortcuts import render

# ------------------------------
# Domovská stránka aplikace
# ------------------------------
def home(request):
    """
    Zobrazuje domovskou stránku aplikace.

    Tato funkce zpracovává požadavky na domovskou stránku a vrací šablonu
    s uvítací zprávou a dalšími informacemi.

    Kontext (proměnné předané šabloně):
        - title: Název stránky (zobrazený v záhlaví prohlížeče).
        - message: Uvítací zpráva pro uživatele.
    """
    # Definice kontextu s proměnnými předávanými do šablony
    context = {
        'title': 'Domovská stránka',  # Název stránky pro šablonu
        'message': 'Vítejte v naší aplikaci! Prozkoumejte funkce níže.',  # Uvítací zpráva
    }

    # Vykreslení šablony a vrácení odpovědi
    return render(request, 'home.html', context)