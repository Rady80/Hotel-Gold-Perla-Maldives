# accounts/urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

# Definice URL pro aplikaci accounts
urlpatterns = [
    # Registrace nového uživatele
    path(
        'register/',
        views.register_page,
        name='register'
    ),
    
    # Přihlášení uživatele
    path(
        'login/',
        views.login_page,
        name='login'
    ),
    
    # Odhlášení uživatele
    path(
        'logout/',
        views.logout_user,
        name='logout'
    ),

    # Reset hesla
    # Krok 1: Zadání e-mailu pro reset hesla
    path(
        'password_reset/',
        auth_views.PasswordResetView.as_view(
            template_name='registration/password_reset_form.html'
        ),
        name='password_reset'
    ),
    
    # Krok 2: Potvrzení odeslání e-mailu s instrukcemi pro reset hesla
    path(
        'password_reset_done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='registration/password_reset_done.html'
        ),
        name='password_reset_done'
    ),
    
    # Krok 3: Zadání nového hesla (po kliknutí na odkaz v e-mailu)
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='registration/password_reset_confirm.html'
        ),
        name='password_reset_confirm'
    ),
    
    # Krok 4: Potvrzení úspěšného resetování hesla
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='registration/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),
]