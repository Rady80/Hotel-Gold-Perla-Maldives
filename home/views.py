from django.shortcuts import render

def home(request):
    """Domovská stránka"""
    return render(request, 'home/home.html')

def about_view(request):
    """Stránka 'O nás'"""
    return render(request, 'home/about.html')

def contact_view(request):
    """Kontaktní stránka"""
    return render(request, 'home/contact.html')