import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
import unittest
from unittest.mock import patch, MagicMock
from peewee import *
from datetime import date
from otro import Usuario, RegistroDecision, RegistroMenstrual, App

# Configura una base de datos de prueba en memoria
test_db = SqliteDatabase(':memory:')

class TestApp(unittest.TestCase):

    def setUp(self):
        # Cambia a la base de datos de prueba
        test_db.bind([Usuario, RegistroDecision, RegistroMenstrual], bind_refs=False, bind_backrefs=False)
        test_db.connect()
        test_db.create_tables([Usuario, RegistroDecision, RegistroMenstrual])

    def tearDown(self):
        # Cierra la conexión a la base de datos de prueba
        test_db.drop_tables([Usuario, RegistroDecision, RegistroMenstrual])
        test_db.close()

    def test_crear_usuario(self):
        usuario = Usuario.create(nombre="test_user", contrasena="test_pass")
        self.assertEqual(Usuario.select().count(), 1)
        self.assertEqual(usuario.nombre, "test_user")

    def test_crear_registro_decision(self):
        usuario = Usuario.create(nombre="test_user", contrasena="test_pass")
        decision = RegistroDecision.create(
            usuario=usuario,
            fecha=date.today(),
            decision="Test decision",
            nota="Test note",
            estado_animo="Normal",
            premenstrual=False,
            evento_inusual="Nada inusual"
        )
        self.assertEqual(RegistroDecision.select().count(), 1)
        self.assertEqual(decision.decision, "Test decision")

    def test_crear_registro_menstrual(self):
        usuario = Usuario.create(nombre="test_user", contrasena="test_pass")
        registro = RegistroMenstrual.create(
            usuario=usuario,
            fecha=date.today(),
            sintomas="Test sintomas"
        )
        self.assertEqual(RegistroMenstrual.select().count(), 1)
        self.assertEqual(registro.sintomas, "Test sintomas")

    @patch('tkinter.messagebox.showinfo')
    @patch('tkinter.messagebox.showerror')
    def test_login_exitoso(self, mock_showerror, mock_showinfo):
        app = App()
        Usuario.create(nombre="test_user", contrasena="test_pass")
        app.entry_usuario.insert(0, "test_user")
        app.entry_contrasena.insert(0, "test_pass")
        app.login()
        mock_showinfo.assert_called_with("Login", "¡Login exitoso!")

    @patch('tkinter.messagebox.showinfo')
    @patch('tkinter.messagebox.showerror')
    def test_login_fallido(self, mock_showerror, mock_showinfo):
        app = App()
        Usuario.create(nombre="test_user", contrasena="test_pass")
        app.entry_usuario.insert(0, "test_user")
        app.entry_contrasena.insert(0, "wrong_pass")
        app.login()
        mock_showerror.assert_called_with("Login", "Contraseña incorrecta.")

    @patch('tkinter.messagebox.showinfo')
    def test_registrar_usuario(self, mock_showinfo):
        app = App()
        app.entry_usuario.insert(0, "new_user")
        app.entry_contrasena.insert(0, "new_pass")
        app.registrar()
        self.assertEqual(Usuario.select().count(), 1)
        mock_showinfo.assert_called_with("Registro", "¡Usuario registrado exitosamente!")

    # Agrega más pruebas según sea necesario para otras funciones

if __name__ == '__main__':
    unittest.main()