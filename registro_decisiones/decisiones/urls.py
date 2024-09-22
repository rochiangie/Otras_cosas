from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('menu_principal/', views.menu_principal, name='menu_principal'),
    # Agregar más rutas para registrar decisiones y ver registros
]
