from django.urls import path
from . import views  # Import pohledů z accounts.views
from django.contrib.auth import views as auth_views  # Import vestavěných autentizačních pohledů

# ------------------------------
# Definice URL směrování pro aplikaci 'accounts'
# ------------------------------
urlpatterns = [
    # ------------------------------
    # Registrace nového uživatele
    # ------------------------------
    path(
        'register/',  # Adresa pro stránku registrace
        views.register_page,  # Pohled pro zpracování registrace
        name='register'  # Název URL pro použití v šablonách (např. `{% url 'register' %}`)
    ),

    # ------------------------------
    # Přihlášení uživatele
    # ------------------------------
    path(
        'login/',  # Adresa pro stránku přihlášení
        views.login_page,  # Pohled pro zpracování přihlášení
        name='login'  # Název URL pro použití v šablonách (např. `{% url 'login' %}`)
    ),

    # ------------------------------
    # Odhlášení uživatele
    # ------------------------------
    path(
        'logout/',  # Adresa pro odhlášení
        views.logout_user,  # Pohled pro zpracování odhlášení
        name='logout'  # Název URL pro použití v šablonách (např. `{% url 'logout' %}`)
    ),

    # ------------------------------
    # Reset hesla - proces krok za krokem
    # ------------------------------

    # Krok 1: Zadání e-mailu pro reset hesla
    path(
        'password_reset/',  # Adresa pro formulář resetování hesla
        auth_views.PasswordResetView.as_view(
            template_name='registration/password_reset_form.html'  # Šablona pro reset hesla
        ),
        name='password_reset'  # Název URL pro použití v šablonách
    ),

    # Krok 2: Potvrzení odeslání e-mailu
    path(
        'password_reset_done/',  # Adresa pro potvrzení odeslání e-mailu
        auth_views.PasswordResetDoneView.as_view(
            template_name='registration/password_reset_done.html'  # Šablona potvrzení
        ),
        name='password_reset_done'  # Název URL pro použití v šablonách
    ),

    # Krok 3: Zadání nového hesla (po kliknutí na odkaz v e-mailu)
    path(
        'reset/<uidb64>/<token>/',  # Dynamická cesta s identifikátorem uživatele a tokenem
        auth_views.PasswordResetConfirmView.as_view(
            template_name='registration/password_reset_confirm.html'  # Šablona pro zadání nového hesla
        ),
        name='password_reset_confirm'  # Název URL pro použití v šablonách
    ),

    # Krok 4: Potvrzení úspěšného resetování hesla
    path(
        'reset/done/',  # Adresa potvrzující úspěšné resetování hesla
        auth_views.PasswordResetCompleteView.as_view(
            template_name='registration/password_reset_complete.html'  # Šablona pro potvrzení
        ),
        name='password_reset_complete'  # Název URL pro použití v šablonách
    ),

    # ------------------------------
    # Profil uživatele
    # ------------------------------
    path(
        'profile/',  # Adresa pro stránku profilu uživatele
        views.profile_view,  # Pohled pro zpracování zobrazení profilu
        name='profile'  # Název URL pro použití v šablonách (např. `{% url 'profile' %}`)
    ),
]