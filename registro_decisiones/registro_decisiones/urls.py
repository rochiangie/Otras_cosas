from django.urls import path
from decisiones import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login, name='login'),
    path('menu_principal/', views.menu_principal, name='menu_principal'),
    path('', views.menu_principal, name='home'),  # Redirigir la raíz a 'menu_principal'
]
