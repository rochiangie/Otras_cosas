from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import Usuario
from django.contrib.auth.models import User

def login_view(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        contrasena = request.POST['contrasena']

        # Aquí puedes usar el sistema de autenticación de Django o uno personalizado
        try:
            usuario = Usuario.objects.get(nombre=nombre)
            if usuario.contrasena == contrasena:
                request.session['usuario_id'] = usuario.id
                return redirect('menu_principal')
            else:
                error = "Contraseña incorrecta"
        except Usuario.DoesNotExist:
            error = "Usuario no existe"

        return render(request, 'login.html', {'error': error})
    
    return render(request, 'login.html')
from django.shortcuts import render

def menu_principal(request):
    return render(request, 'menu_principal.html')  # Asegúrate de que la plantilla existe


