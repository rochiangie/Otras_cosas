# Registro de Decisiones y Ciclo Menstrual

## Descripción
Esta aplicación de escritorio permite a los usuarios registrar decisiones importantes que tomen día a día, junto con su estado de ánimo, eventos inusuales y el ciclo menstrual. La información se almacena en una base de datos SQLite, y los registros se pueden visualizar en la interfaz.

## Funcionalidades
- **Registro de usuarios**: Los usuarios pueden registrarse con un nombre y contraseña únicos.
- **Login**: Ingreso con nombre de usuario y contraseña para acceder a las funcionalidades de la aplicación.
- **Registrar decisiones**: Los usuarios pueden registrar decisiones diarias, el estado de ánimo, si están premenstruales, y eventos inusuales.
- **Registrar ciclo menstrual**: Los usuarios pueden registrar los síntomas de su ciclo menstrual.
- **Visualización de registros**: Los usuarios pueden ver un historial de decisiones y ciclos menstruales en formato de tabla.
- **Calendario**: Se muestra un calendario donde los días premenstruales están marcados en rojo.

## Requisitos
- **Python 3.7 o superior**: Asegúrate de tener instalada una versión compatible de Python.
- **Librerías**:
  - `tkinter` para la interfaz gráfica.
  - `peewee` para manejar la base de datos SQLite.
  - `tkcalendar` para el calendario.
  - `datetime` para trabajar con fechas.

## Instalación
1. Clona este repositorio:
   ```bash
   git clone https://github.com/usuario/proyecto_decisiones.git
   cd proyecto_decisiones
