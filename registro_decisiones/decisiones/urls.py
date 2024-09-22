from django.urls import path
from . import views  # Importamos las vistas de la aplicación

urlpatterns = [
    path('login/', views.login, name='login'),
    path('menu_principal/', views.menu_principal, name='menu_principal'),
]
