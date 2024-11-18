from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

# Definice URL pro aplikaci accounts
urlpatterns = [
    # Registrace uživatele
    path('register/', views.register_page, name='register'),  
    # URL pro přihlášení uživatele
    path('login/', views.login_page, name='login'),          
    # URL pro odhlášení uživatele
    path('logout/', views.logout_user, name='logout'),       

    # Reset hesla
    # Krok 1: Zadání e-mailu pro reset hesla
    path(
        'password_reset/',
        auth_views.PasswordResetView.as_view(
            template_name='registration/password_reset_form.html'
        ),
        name='password_reset'
    ),
    # Krok 2: Potvrzení odeslání e-mailu
    path(
        'password_reset_done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='registration/password_reset_done.html'
        ),
        name='password_reset_done'
    ),
    # Krok 3: Nastavení nového hesla
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='registration/password_reset_confirm.html'
        ),
        name='password_reset_confirm'
    ),
    # Krok 4: Potvrzení úspěšného resetu hesla
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='registration/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),
]