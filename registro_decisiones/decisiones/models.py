from django.db import models

class Usuario(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    contrasena = models.CharField(max_length=255)

class RegistroDecision(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='decisiones')
    fecha = models.DateField()
    decision = models.TextField()
    nota = models.TextField(null=True, blank=True)
    estado_animo = models.CharField(max_length=50)
    premenstrual = models.BooleanField(default=False)
    evento_inusual = models.TextField(null=True, blank=True)

class RegistroMenstrual(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='ciclos_menstruales')
    fecha = models.DateField()
    sintomas = models.TextField()
