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
    fecha = DateField()
    es_inicio_ciclo = BooleanField(default=False)
    
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

        self.usuario_actual = None
        self.fecha_actual = datetime.now().date()

        self.lbl_usuario = tk.Label(self, text="Usuario:", bg='#FADADD')
        self.lbl_usuario.pack(pady=5)

        self.entry_usuario = tk.Entry(self)
        self.entry_usuario.pack(pady=5)

        self.lbl_contrasena = tk.Label(self, text="Contraseña:", bg='#FADADD')
        self.lbl_contrasena.pack(pady=5)

        self.entry_contrasena = tk.Entry(self, show='*')
        self.entry_contrasena.pack(pady=5)

        self.btn_ingresar = tk.Button(self, text="Ingresar", command=self.login, bg='#FFB6C1', fg='white', font=('Arial', 12, 'bold'))
        self.btn_ingresar.pack(pady=10)

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

        usuario_existente = Usuario.select().where(Usuario.nombre == usuario).first()

        if usuario_existente:
            messagebox.showerror("Error", "El nombre de usuario ya existe. Elige otro.")
            return

        try:
            nuevo_usuario = Usuario.create(nombre=usuario, contrasena=contrasena)
            messagebox.showinfo("Registro", "¡Usuario registrado exitosamente!")
        except IntegrityError:
            messagebox.showerror("Error", "El nombre de usuario ya existe. Elige otro.")

    def abrir_menu_principal(self):
        for widget in self.winfo_children():
            widget.pack_forget()

        frame_contenedor = tk.Frame(self, bg='#FADADD')
        frame_contenedor.pack(fill='both', expand=True)

        self.calendar = Calendar(frame_contenedor, selectmode='day', year=self.fecha_actual.year, month=self.fecha_actual.month, day=self.fecha_actual.day)
        self.calendar.pack(pady=10)

        self.btn_registrar_decision = tk.Button(frame_contenedor, text="Registrar Decisión", command=self.registrar_decision, bg='#FFB6C1', fg='white', font=('Arial', 12, 'bold'))
        self.btn_registrar_decision.pack(pady=10)

        self.btn_registrar_menstrual = tk.Button(frame_contenedor, text="Registrar Ciclo Menstrual", command=self.registrar_menstrual, bg='#FFB6C1', fg='white', font=('Arial', 12, 'bold'))
        self.btn_registrar_menstrual.pack(pady=10)

        self.btn_ver_decisiones = tk.Button(frame_contenedor, text="Ver Decisiones", command=self.ver_decisiones, bg='#FFB6C1', fg='white', font=('Arial', 12, 'bold'))
        self.btn_ver_decisiones.pack(pady=10)

        self.btn_ver_menstrual = tk.Button(frame_contenedor, text="Ver Ciclos Menstruales", command=self.ver_menstruales, bg='#FFB6C1', fg='white', font=('Arial', 12, 'bold'))
        self.btn_ver_menstrual.pack(pady=10)

        self.btn_simular_dias = tk.Button(frame_contenedor, text="Simular Paso de Días", command=self.simular_paso_dias, bg='#FFB6C1', fg='white', font=('Arial', 12, 'bold'))
        self.btn_simular_dias.pack(pady=10)

        self.mostrar_colores_calendario()
        self.actualizar_calendario()
        self.comenzar_recordatorios()

    def mostrar_colores_calendario(self):
        leyenda = tk.Toplevel(self)
        leyenda.title("Leyenda del Calendario")
        leyenda.geometry("300x200")

        tk.Label(leyenda, text="Rojo: Inicio de la menstruación", bg='#FADADD').pack(pady=5)
        tk.Label(leyenda, text="Verde: Ovulación", bg='#FADADD').pack(pady=5)
        tk.Label(leyenda, text="Amarillo: Periodo premenstrual", bg='#FADADD').pack(pady=5)

    def actualizar_calendario(self):
        # Aquí puedes actualizar los colores del calendario según los registros menstruales
        registros = RegistroMenstrual.select().where(RegistroMenstrual.usuario == self.usuario_actual)
        for registro in registros:
            fecha_inicio = registro.fecha_inicio
            fecha_final = fecha_inicio + timedelta(days=5)  # Ejemplo de periodo menstrual de 5 días
            self.calendar.calevent_create(fecha_inicio, 'Inicio Menstrual', 'menstrual')
            self.calendar.tag_config('menstrual', background='red', foreground='white')

    def convertir_fecha(self, fecha_str):
        return datetime.strptime(fecha_str, '%m/%d/%y').date()

    def registrar_decision(self):
        def guardar_decision():
            decision = entry_decision.get("1.0", "end-1c")
            nota = entry_nota.get("1.0", "end-1c")
            estado_animo = combo_estado.get()
            premenstrual = var_premenstrual.get()
            evento_inusual = entry_evento.get("1.0", "end-1c")
            fecha_seleccionada = self.convertir_fecha(calendar.get_date())

            if decision and estado_animo and fecha_seleccionada:
                RegistroDecision.create(
                    usuario=self.usuario_actual,
                    fecha=fecha_seleccionada,
                    decision=decision,
                    nota=nota,
                    estado_animo=estado_animo,
                    premenstrual=bool(premenstrual),
                    evento_inusual=evento_inusual
                )
                messagebox.showinfo("Registro", "Decisión registrada exitosamente.")
                ventana_decision.destroy()
            else:
                messagebox.showerror("Error", "Por favor, complete los campos obligatorios.")

        ventana_decision = tk.Toplevel(self)
        ventana_decision.title("Registrar Decisión")
        ventana_decision.geometry("400x500")
        ventana_decision.configure(bg='#FADADD')

        tk.Label(ventana_decision, text="Selecciona la fecha:", bg='#FADADD').pack(pady=5)

        calendar = Calendar(ventana_decision, selectmode='day', year=self.fecha_actual.year, month=self.fecha_actual.month, day=self.fecha_actual.day)
        calendar.pack(pady=5)

        tk.Label(ventana_decision, text="Describe tu decisión:", bg='#FADADD').pack(pady=5)
        entry_decision = tk.Text(ventana_decision, height=5, width=40)
        entry_decision.pack(pady=5)

        tk.Label(ventana_decision, text="Nota adicional:", bg='#FADADD').pack(pady=5)
        entry_nota = tk.Text(ventana_decision, height=5, width=40)
        entry_nota.pack(pady=5)

        tk.Label(ventana_decision, text="Estado de ánimo:", bg='#FADADD').pack(pady=5)
        combo_estado = ttk.Combobox(ventana_decision, values=["Feliz", "Triste", "Enojado", "Ansioso", "Relajado"])
        combo_estado.pack(pady=5)

        tk.Label(ventana_decision, text="¿Periodo premenstrual?", bg='#FADADD').pack(pady=5)
        var_premenstrual = tk.IntVar()
        tk.Checkbutton(ventana_decision, variable=var_premenstrual, bg='#FADADD').pack(pady=5)

        tk.Label(ventana_decision, text="Evento inusual (opcional):", bg='#FADADD').pack(pady=5)
        entry_evento = tk.Text(ventana_decision, height=3, width=40)
        entry_evento.pack(pady=5)

        btn_guardar = tk.Button(ventana_decision, text="Guardar", command=guardar_decision, bg='#FFB6C1', fg='white', font=('Arial', 12, 'bold'))
        btn_guardar.pack(pady=10)

    def registrar_menstrual(self):
        def guardar_menstrual():
            sintomas = entry_sintomas.get("1.0", "end-1c")
            fecha_seleccionada = self.convertir_fecha(calendar.get_date())
            es_inicio_ciclo = var_inicio_ciclo.get()

            if fecha_seleccionada and sintomas:
                RegistroMenstrual.create(
                    usuario=self.usuario_actual,
                    fecha_inicio=fecha_seleccionada if es_inicio_ciclo else None,
                    sintomas=sintomas,
                    fecha=fecha_seleccionada,
                    es_inicio_ciclo=bool(es_inicio_ciclo)
                )
                messagebox.showinfo("Registro", "Registro menstrual guardado exitosamente.")
                ventana_menstrual.destroy()
            else:
                messagebox.showerror("Error", "Por favor, complete los campos obligatorios.")

        ventana_menstrual = tk.Toplevel(self)
        ventana_menstrual.title("Registrar Ciclo Menstrual")
        ventana_menstrual.geometry("400x500")
        ventana_menstrual.configure(bg='#FADADD')

        tk.Label(ventana_menstrual, text="Selecciona la fecha:", bg='#FADADD').pack(pady=5)

        calendar = Calendar(ventana_menstrual, selectmode='day', year=self.fecha_actual.year, month=self.fecha_actual.month, day=self.fecha_actual.day)
        calendar.pack(pady=5)

        tk.Label(ventana_menstrual, text="Describe tus síntomas:", bg='#FADADD').pack(pady=5)
        entry_sintomas = tk.Text(ventana_menstrual, height=5, width=40)
        entry_sintomas.pack(pady=5)

        tk.Label(ventana_menstrual, text="¿Es el inicio del ciclo menstrual?", bg='#FADADD').pack(pady=5)
        var_inicio_ciclo = tk.IntVar()
        tk.Checkbutton(ventana_menstrual, variable=var_inicio_ciclo, bg='#FADADD').pack(pady=5)

        btn_guardar = tk.Button(ventana_menstrual, text="Guardar", command=guardar_menstrual, bg='#FFB6C1', fg='white', font=('Arial', 12, 'bold'))
        btn_guardar.pack(pady=10)

    def ver_decisiones(self):
        ventana_decisiones = tk.Toplevel(self)
        ventana_decisiones.title("Decisiones Registradas")
        ventana_decisiones.geometry("600x400")
        ventana_decisiones.configure(bg='#FADADD')

        registros = RegistroDecision.select().where(RegistroDecision.usuario == self.usuario_actual)

        for registro in registros:
            texto = f"Fecha: {registro.fecha}\nDecisión: {registro.decision}\nEstado de ánimo: {registro.estado_animo}\nPremenstrual: {registro.premenstrual}\nEvento Inusual: {registro.evento_inusual}\n"
            tk.Label(ventana_decisiones, text=texto, bg='#FADADD').pack(pady=5)

    def ver_menstruales(self):
        ventana_menstruales = tk.Toplevel(self)
        ventana_menstruales.title("Ciclos Menstruales Registrados")
        ventana_menstruales.geometry("600x400")
        ventana_menstruales.configure(bg='#FADADD')

        registros = RegistroMenstrual.select().where(RegistroMenstrual.usuario == self.usuario_actual)

        for registro in registros:
            texto = f"Fecha: {registro.fecha}\nSíntomas: {registro.sintomas}\nEs inicio del ciclo: {registro.es_inicio_ciclo}\n"
            tk.Label(ventana_menstruales, text=texto, bg='#FADADD').pack(pady=5)

    def simular_paso_dias(self):
        ventana_simular = tk.Toplevel(self)
        ventana_simular.title("Simular Paso de Días")
        ventana_simular.geometry("400x200")
        ventana_simular.configure(bg='#FADADD')

        tk.Label(ventana_simular, text="Ingrese la cantidad de días a simular:", bg='#FADADD').pack(pady=10)
        entry_dias = tk.Entry(ventana_simular)
        entry_dias.pack(pady=5)

        def simular():
            dias = int(entry_dias.get())
            self.fecha_actual += timedelta(days=dias)
            self.actualizar_calendario()
            ventana_simular.destroy()

        btn_simular = tk.Button(ventana_simular, text="Simular", command=simular, bg='#FFB6C1', fg='white', font=('Arial', 12, 'bold'))
        btn_simular.pack(pady=10)

    def comenzar_recordatorios(self):
        # Aquí puedes implementar recordatorios si es necesario
        pass

if __name__ == "__main__":
    app = App()
    app.mainloop()

