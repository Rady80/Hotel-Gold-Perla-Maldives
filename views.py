from django.shortcuts import render

# Pohled pro domovskou stránku
def home(request):
    """
    Zobrazení domovské stránky.
    """
    return render(request, 'hotel/home.html')

# Pohled pro seznam událostí
def events(request):
    """
    Zobrazení seznamu událostí.
    """
    return render(request, 'hotel/events.html')

# Další pohledy...
