from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

# Definice URL pro aplikaci accounts
urlpatterns = [
    path('register/', views.register_page, name='register'),  # URL pro registraci uživatele
    path('login/', views.login_page, name='login'),          # URL pro přihlášení uživatele
    path('logout/', views.logout_user, name='logout'),       # URL pro odhlášení uživatele
    
    # Reset hesla
    # Reset hesla - krok 1 (zadání e-mailu)
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),

    # Reset hesla - krok 2 (potvrzení odeslání e-mailu)
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),

    # Reset hesla - krok 3 (nastavení nového hesla)
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),

    # Reset hesla - krok 4 (potvrzení úspěšného resetu)
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
]
