from django.shortcuts import render  # Import pro renderování šablon

# Domovská stránka
def home_view(request):
    """
    Zobrazuje domovskou stránku.
    """
    return render(request, 'home/home.html')

# Stránka "O nás"
def about_view(request):
    """
    Zobrazuje stránku 'O nás'.
    """
    return render(request, 'home/about.html')

# Kontaktní stránka
def contact_view(request):
    """
    Zobrazuje kontaktní stránku.
    """
    return render(request, 'home/contact.html')