from django.shortcuts import render

# Domovská stránka aplikace
def home(request):
    """
    Zobrazuje domovskou stránku aplikace.
    
    Tato funkce vrací šablonu obsahující uvítací zprávu.
    """
    context = {
        'title': 'Domovská stránka',  # Název stránky
        'message': 'Vítejte v aplikaci myapp!',  # Zpráva pro uživatele
    }
    return render(request, 'home.html', context)