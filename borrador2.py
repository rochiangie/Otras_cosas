import tkinter as tk
from tkinter import ttk, messagebox
from peewee import *
from tkcalendar import Calendar
from datetime import datetime, timedelta
import threading
from peewee import IntegrityError

# Conexión a la base de datos
db = SqliteDatabase('decisiones.db')

# Modelos de la base de datos
class Usuario(Model):
    nombre = CharField(unique=True)
    contrasena = CharField()

    class Meta:
        database = db

class RegistroDecision(Model):
    usuario = ForeignKeyField(Usuario, backref='decisiones')
    fecha = DateField()
    decision = TextField()
    nota = TextField(null=True)
    estado_animo = CharField()
    premenstrual = BooleanField()
    evento_inusual = TextField(null=True)

    class Meta:
        database = db

class RegistroMenstrual(Model):
    usuario = ForeignKeyField(Usuario, backref='ciclos_menstruales')
    fecha_inicio = DateField()
    sintomas = TextField()
    es_inicio_ciclo = BooleanField()

    class Meta:
        database = db

# Conectar a la base de datos y crear tablas
db.connect()
db.create_tables([Usuario, RegistroDecision, RegistroMenstrual], safe=True)

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Registro de Decisiones")
        self.geometry("600x700")
        self.configure(bg='#FADADD')

        # Usuario actual (luego de login)
        self.usuario_actual = None

        # Fecha actual para la simulación de días
        self.fecha_actual = datetime.now().date()

        # Etiquetas y entradas
        self.lbl_usuario = tk.Label(self, text="Usuario:", bg='#FADADD')
        self.lbl_usuario.pack(pady=5)

        self.entry_usuario = tk.Entry(self)
        self.entry_usuario.pack(pady=5)

        self.lbl_contrasena = tk.Label(self, text="Contraseña:", bg='#FADADD')
        self.lbl_contrasena.pack(pady=5)

        self.entry_contrasena = tk.Entry(self, show='*')
        self.entry_contrasena.pack(pady=5)

        # Botón para ingresar
        self.btn_ingresar = tk.Button(self, text="Ingresar", command=self.login, bg='#FFB6C1', fg='white', font=('Arial', 12, 'bold'))
        self.btn_ingresar.pack(pady=10)

        # Botón para registrarse
        self.btn_registrar = tk.Button(self, text="Registrar", command=self.registrar, bg='#FFB6C1', fg='white', font=('Arial', 12, 'bold'))
        self.btn_registrar.pack(pady=10)

    def login(self):
        usuario = self.entry_usuario.get()
        contrasena = self.entry_contrasena.get()

        try:
            user = Usuario.get(Usuario.nombre == usuario)
            if user.contrasena == contrasena:
                self.usuario_actual = user
                messagebox.showinfo("Login", "¡Login exitoso!")
                self.abrir_menu_principal()
            else:
                messagebox.showerror("Login", "Contraseña incorrecta.")
        except Usuario.DoesNotExist:
            messagebox.showerror("Login", "El usuario no existe.")

    def registrar(self):
        usuario = self.entry_usuario.get()
        contrasena = self.entry_contrasena.get()

        if not usuario or not contrasena:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        # Verifica si el usuario ya existe
        usuario_existente = Usuario.select().where(Usuario.nombre == usuario).first()

        if usuario_existente:
            messagebox.showerror("Error", "El nombre de usuario ya existe. Elige otro.")
            return

        try:
            # Intenta crear el nuevo usuario
            nuevo_usuario = Usuario.create(nombre=usuario, contrasena=contrasena)
            messagebox.showinfo("Registro", "¡Usuario registrado exitosamente!")
        except IntegrityError:
            messagebox.showerror("Error", "El nombre de usuario ya existe. Elige otro.")

    def abrir_menu_principal(self):
        # Ocultar elementos de login
        for widget in self.winfo_children():
            widget.pack_forget()

        # Crear un marco (Frame) para contener todo
        frame_contenedor = tk.Frame(self, bg='#FADADD')
        frame_contenedor.pack(fill='both', expand=True)

        # **Calendario en la ventana principal** 
        self.calendar = Calendar(frame_contenedor, selectmode='day', year=self.fecha_actual.year, month=self.fecha_actual.month, day=self.fecha_actual.day)
        self.calendar.pack(pady=10)

        # Botones del menú principal
        self.btn_registrar_decision = tk.Button(frame_contenedor, text="Registrar Decisión", command=self.registrar_decision, bg='#FFB6C1', fg='white', font=('Arial', 12, 'bold'))
        self.btn_registrar_decision.pack(pady=10)

        self.btn_registrar_menstrual = tk.Button(frame_contenedor, text="Registrar Ciclo Menstrual", command=self.registrar_menstrual, bg='#FFB6C1', fg='white', font=('Arial', 12, 'bold'))
        self.btn_registrar_menstrual.pack(pady=10)

        self.btn_ver_decisiones = tk.Button(frame_contenedor, text="Ver Decisiones", command=self.ver_decisiones, bg='#FFB6C1', fg='white', font=('Arial', 12, 'bold'))
        self.btn_ver_decisiones.pack(pady=10)

        self.btn_ver_menstrual = tk.Button(frame_contenedor, text="Ver Ciclos Menstruales", command=self.ver_menstruales, bg='#FFB6C1', fg='white', font=('Arial', 12, 'bold'))
        self.btn_ver_menstrual.pack(pady=10)

        # Simulación del paso de días
        self.btn_simular_dias = tk.Button(frame_contenedor, text="Simular Paso de Días", command=self.simular_paso_dias, bg='#FFB6C1', fg='white', font=('Arial', 12, 'bold'))
        self.btn_simular_dias.pack(pady=10)

        # **Mostrar colores del calendario**
        self.mostrar_colores_calendario()
        self.actualizar_calendario()
        self.comenzar_recordatorios()

    def mostrar_colores_calendario(self):
        # Mostrar leyenda de colores
        leyenda = tk.Toplevel(self)
        leyenda.title("Leyenda del Calendario")
        leyenda.geometry("300x200")

        tk.Label(leyenda, text="Rojo: Inicio de la menstruación", bg='#FADADD').pack(pady=5)
        tk.Label(leyenda, text="Verde: Ovulación", bg='#FADADD').pack(pady=5)
        tk.Label(leyenda, text="Amarillo: Periodo premenstrual", bg='#FADADD').pack(pady=5)
        tk.Label(leyenda, text="Azul: Inicio del próximo periodo", bg='#FADADD').pack(pady=5)

    def convertir_fecha(self, fecha_str):
        formatos = ['%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y', '%d/%m/%y', '%m/%d/%y']
        for formato in formatos:
            try:
                return datetime.strptime(fecha_str, formato).date()
            except ValueError:
                continue
        raise ValueError(f"Fecha '{fecha_str}' no coincide con ningún formato conocido")

    def actualizar_calendario(self):
        # Limpia todos los colores del calendario
        self.calendar.calevent_remove('all')

        # Obtén todos los ciclos menstruales del usuario actual
        ciclos = RegistroMenstrual.select().where(RegistroMenstrual.usuario == self.usuario_actual)

        for ciclo in ciclos:
            fecha_inicio_str = ciclo.fecha_inicio

            if fecha_inicio_str is None:
                continue  # Si fecha_inicio es None, salta este ciclo

            try:
                fecha_inicio = self.convertir_fecha(fecha_inicio_str)
            except ValueError as e:
                print(e)
                continue  # Si la fecha no es válida, salta este ciclo

            # Calcula las fechas basadas en la fecha de inicio
            fecha_ovulacion = fecha_inicio + timedelta(days=14)
            fecha_proximo_periodo = fecha_inicio + timedelta(days=28)
            fecha_premenstrual = fecha_proximo_periodo - timedelta(days=3)  # 3 días antes del próximo período

            # Marca la fecha de inicio de la menstruación en rojo
            self.calendar.calevent_create(fecha_inicio, 'Inicio de menstruación', 'red')

            # Marca la fecha de ovulación en verde
            self.calendar.calevent_create(fecha_ovulacion, 'Ovulación', 'green')

            # Marca el periodo premenstrual en amarillo
            self.calendar.calevent_create(fecha_premenstrual, 'Premenstrual', 'yellow')

            # Marca el próximo periodo en azul
            self.calendar.calevent_create(fecha_proximo_periodo, 'Inicio próximo periodo', 'blue')

        # Configura los colores de los eventos en el calendario
        self.calendar.tag_config('red', background='red', foreground='white')
        self.calendar.tag_config('green', background='green', foreground='white')
        self.calendar.tag_config('yellow', background='yellow', foreground='black')
        self.calendar.tag_config('blue', background='blue', foreground='white')

    def registrar_decision(self):
        # Código para registrar una decisión
        pass

    def registrar_menstrual(self):
        # Código para registrar un ciclo menstrual
        pass

    def ver_decisiones(self):
        # Código para ver decisiones
        pass

    def ver_menstruales(self):
        # Código para ver ciclos menstruales
        pass

    def simular_paso_dias(self):
        # Código para simular el paso de días
        pass

    def comenzar_recordatorios(self):
        # Código para comenzar recordatorios
        pass

if __name__ == "__main__":
    app = App()
    app.mainloop()
