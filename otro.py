import tkinter as tk
from tkinter import ttk, messagebox
from peewee import *
from tkcalendar import Calendar
from datetime import datetime
from otro import *

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
    fecha = DateField()
    sintomas = TextField()
    
    class Meta:
        database = db

# Crear las tablas en la base de datos
db.connect()
db.create_tables([Usuario, RegistroDecision, RegistroMenstrual])

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Registro de Decisiones")
        self.geometry("600x700")
        self.configure(bg='#FADADD')  # Fondo en rosa pastel

        # Usuario actual (luego de login)
        self.usuario_actual = None

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
        
        try:
            nuevo_usuario = Usuario.create(nombre=usuario, contrasena=contrasena)
            nuevo_usuario.save()
            messagebox.showinfo("Registro", "¡Usuario registrado exitosamente!")
        except IntegrityError:
            messagebox.showerror("Error", "El nombre de usuario ya existe.")
    
    def abrir_menu_principal(self):
        # Ocultar elementos de login
        for widget in self.winfo_children():
            widget.pack_forget()

        # Calendario
        self.calendar = Calendar(self, selectmode='day', year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)
        self.calendar.pack(pady=10)

        # Botones del menú principal
        self.btn_registrar_decision = tk.Button(self, text="Registrar Decisión", command=self.registrar_decision, bg='#FFB6C1', fg='white', font=('Arial', 12, 'bold'))
        self.btn_registrar_decision.pack(pady=10)
        
        self.btn_registrar_menstrual = tk.Button(self, text="Registrar Ciclo Menstrual", command=self.registrar_menstrual, bg='#FFB6C1', fg='white', font=('Arial', 12, 'bold'))
        self.btn_registrar_menstrual.pack(pady=10)

        self.btn_ver_decisiones = tk.Button(self, text="Ver Decisiones", command=self.ver_decisiones, bg='#FFB6C1', fg='white', font=('Arial', 12, 'bold'))
        self.btn_ver_decisiones.pack(pady=10)

        self.btn_ver_menstrual = tk.Button(self, text="Ver Ciclos Menstruales", command=self.ver_menstruales, bg='#FFB6C1', fg='white', font=('Arial', 12, 'bold'))
        self.btn_ver_menstrual.pack(pady=10)

        self.actualizar_calendario()

    def actualizar_calendario(self):
        ciclos = RegistroMenstrual.select().where(RegistroMenstrual.usuario == self.usuario_actual)
        for ciclo in ciclos:
            self.calendar.calevent_create(ciclo.fecha, 'Premenstrual', 'premenstrual')
        self.calendar.tag_config('premenstrual', background='red', foreground='white')
    
    def registrar_decision(self):
        def guardar_decision():
            decision = entry_decision.get("1.0", "end-1c")
            nota = entry_nota.get("1.0", "end-1c")
            fecha = cal.selection_get()
            estado_animo = combo_animo.get()
            premenstrual = var_premenstrual.get()
            evento_inusual = entry_evento.get("1.0", "end-1c")

            if not decision:
                messagebox.showerror("Error", "La decisión no puede estar vacía.")
                return

            RegistroDecision.create(
                usuario=self.usuario_actual, 
                fecha=fecha, 
                decision=decision, 
                nota=nota,
                estado_animo=estado_animo,
                premenstrual=premenstrual,
                evento_inusual=evento_inusual
            )
            messagebox.showinfo("Registro", "Decisión registrada exitosamente.")
            ventana_decision.destroy()
            self.actualizar_calendario()

        ventana_decision = tk.Toplevel(self)
        ventana_decision.title("Registrar Decisión")
        ventana_decision.geometry("400x600")
        
        cal = Calendar(ventana_decision, selectmode='day', year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)
        cal.pack(pady=10)

        lbl_decision = tk.Label(ventana_decision, text="Decisión:")
        lbl_decision.pack(pady=5)
        entry_decision = tk.Text(ventana_decision, height=4)
        entry_decision.pack(pady=5)

        lbl_animo = tk.Label(ventana_decision, text="¿Cómo te sientes hoy?")
        lbl_animo.pack(pady=5)
        combo_animo = ttk.Combobox(ventana_decision, values=["Muy contenta", "Normal", "Algo molesta", "Muy enojada"])
        combo_animo.pack(pady=5)

        var_premenstrual = tk.BooleanVar()
        chk_premenstrual = tk.Checkbutton(ventana_decision, text="¿Estás premenstrual?", variable=var_premenstrual)
        chk_premenstrual.pack(pady=5)

        lbl_evento = tk.Label(ventana_decision, text="¿Te ha pasado algo inusual?")
        lbl_evento.pack(pady=5)
        entry_evento = tk.Text(ventana_decision, height=3)
        entry_evento.pack(pady=5)

        lbl_nota = tk.Label(ventana_decision, text="Nota adicional:")
        lbl_nota.pack(pady=5)
        entry_nota = tk.Text(ventana_decision, height=3)
        entry_nota.pack(pady=5)
        
        btn_guardar = tk.Button(ventana_decision, text="Guardar", command=guardar_decision, bg='#FFB6C1', fg='white', font=('Arial', 12, 'bold'))
        btn_guardar.pack(pady=10)
    
    def registrar_menstrual(self):
        def guardar_menstrual():
            sintomas = entry_sintomas.get("1.0", "end-1c")
            fecha = cal.selection_get()

            if not sintomas:
                messagebox.showerror("Error", "Los síntomas no pueden estar vacíos.")
                return

            RegistroMenstrual.create(usuario=self.usuario_actual, fecha=fecha, sintomas=sintomas)
            messagebox.showinfo("Registro", "Ciclo menstrual registrado exitosamente.")
            ventana_menstrual.destroy()
            self.actualizar_calendario()

        ventana_menstrual = tk.Toplevel(self)
        ventana_menstrual.title("Registrar Ciclo Menstrual")
        ventana_menstrual.geometry("400x400")
        
        cal = Calendar(ventana_menstrual, selectmode='day', year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)
        cal.pack(pady=20)

        lbl_sintomas = tk.Label(ventana_menstrual, text="Síntomas:")
        lbl_sintomas.pack(pady=5)

        entry_sintomas = tk.Text(ventana_menstrual, height=4)
        entry_sintomas.pack(pady=5)
        
        btn_guardar = tk.Button(ventana_menstrual, text="Guardar", command=guardar_menstrual, bg='#FFB6C1', fg='white', font=('Arial', 12, 'bold'))
        btn_guardar.pack(pady=10)
    
    def ver_decisiones(self):
        ventana_decisiones = tk.Toplevel(self)
        ventana_decisiones.title("Ver Decisiones")
        ventana_decisiones.geometry("800x400")
        
        tree = ttk.Treeview(ventana_decisiones, columns=('Fecha', 'Decisión', 'Estado Ánimo', 'Premenstrual', 'Evento Inusual', 'Nota'), show='headings')
        tree.heading('Fecha', text='Fecha')
        tree.heading('Decisión', text='Decisión')
        tree.heading('Estado Ánimo', text='Estado Ánimo')
        tree.heading('Premenstrual', text='Premenstrual')
        tree.heading('Evento Inusual', text='Evento Inusual')
        tree.heading('Nota', text='Nota')
        tree.pack(fill='both', expand=True)

        decisiones = RegistroDecision.select().where(RegistroDecision.usuario == self.usuario_actual)
        for decision in decisiones:
            tree.insert('', 'end', values=(decision.fecha, decision.decision, decision.estado_animo, 
                                           'Sí' if decision.premenstrual else 'No', 
                                           decision.evento_inusual, decision.nota))
    
    def ver_menstruales(self):
        ventana_menstruales = tk.Toplevel(self)
        ventana_menstruales.title("Ver Ciclos Menstruales")
        ventana_menstruales.geometry("400x400")
        
        tree = ttk.Treeview(ventana_menstruales, columns=('Fecha', 'Síntomas'), show='headings')
        tree.heading('Fecha', text='Fecha')
        tree.heading('Síntomas', text='Síntomas')
        tree.pack(fill='both', expand=True)

        ciclos = RegistroMenstrual.select().where(RegistroMenstrual.usuario == self.usuario_actual)
        for ciclo in ciclos:
            tree.insert('', 'end', values=(ciclo.fecha, ciclo.sintomas))

if __name__ == "__main__":
    app = App()
    app.mainloop()