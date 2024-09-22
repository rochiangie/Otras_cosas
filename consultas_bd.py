from otro import Usuario, RegistroDecision, RegistroMenstrual
from peewee import SqliteDatabase


db = SqliteDatabase('decisiones.db')
db.execute_sql('ALTER TABLE RegistroDecision ADD COLUMN estado_animo TEXT;')




usuarios = Usuario.select()
for usuario in usuarios:
    print(usuario.nombre, usuario.contrasena)

def ver_usuarios(self):
    usuarios = Usuario.select()
    for usuario in usuarios:
        print(f"Usuario: {usuario.nombre}, Contraseña: {usuario.contrasena}")

def ver_decisiones(self):
    decisiones = RegistroDecision.select()
    for decision in decisiones:
        print(f"Decisión: {decision.decision}, Nota: {decision.nota}, Fecha: {decision.fecha}")

def ver_ciclos_menstruales(self):
    ciclos = RegistroMenstrual.select()
    for ciclo in ciclos:
        print(f"Sintomas: {ciclo.sintomas}, Fecha: {ciclo.fecha}")
