<!-- #  Proyecto: Formulario con Login (Flask + SQLite)

##  Descripción breve del proyecto
Este proyecto es una aplicación web básica desarrollada con **Flask (Python)** que permite:
- Autenticar un usuario mediante login.
- Mostrar una página protegida con un **formulario HTML**.
- Guardar los datos ingresados (nombre, correo, teléfono, comentarios) en una base de datos **SQLite**.
- Visualizar los registros almacenados.

Es un ejemplo funcional de integración entre **frontend (HTML, CSS, JS)** y **backend (Python + SQLite)**.

---

##  Pasos para instalar y ejecutar localmente con el app.exe o

### 1️ Requisitos previos
Asegúrate de tener instalado **Python 3.10 o superior**.

### 2️ Instalar dependencias
Abre una terminal en la carpeta del proyecto y ejecuta:

```bash
- pip install flask
---

### 3 Crear la base de datos

- python init_db.py
---

### 4 Ejecutar la aplicación

- python app.py


### 5 Estructura de carpetas

Proyecto/
│
├── app   
│   ├── app.py         # Archivo principal con las rutas de Flask
│   ├── init_db.py             # Script para inicializar la base de datos SQLite (database.db) y crear las tablas necesarias para la aplicación.
│   ├── database.db            # Base de datos SQLite generada automáticamente
│   ├── static/                # Archivos estáticos
│   │    ├── styles.css         # Estilos para la interfaz, botones, formularios y layout general.
│   │    └── script.js          # Funciones JavaScript para validaciones, envío de formularios y recarga dinámica de contenido.
│   │
│   │
│   ├── templates/             # Plantillas HTML
│   │   ├── base.html          # Plantilla base que incluye header, footer y bloques reutilizables para otras páginas.
│   │   ├── login.html         # Página de inicio de sesión donde los usuarios ingresan sus credenciales.
│   │   └── index.html         # Página principal protegida que contiene el formulario a llenar.
│   │
│   ├── requirements.txt       # Lista de dependencias necesarias para ejecutar la aplicación. Se usa para instalar los paquetes con pip install -r requirements.txt.
│   └── README.md              # Archivo de documentación que describe el proyecto, su instalación, uso y estructura.
│
├── build          # Carpeta generada por PyInstaller durante la creación del ejecutable. Contiene archivos temporales de compilación.          
├── app.exe        # Ejecutable generado por PyInstaller a partir de app.py. Permite ejecutar la aplicación en Windows sin necesidad de tener Python instalado.
├── app.spec       # Archivo de configuración usado por PyInstaller para construir el ejecutable, indicando qué archivos incluir, rutas, iconos, etc.
└── venv           # Entorno virtual de Python que contiene todas las dependencias instaladas para el proyecto de manera aislada.
                   Esto asegura que la aplicación funcione sin conflictos con otras instalaciones de Python en el sistema. 
                   
                   
                   
                   Para generar el ejecutable =
                   pyinstaller --onefile --add-data "app\templates;templates" --add-data "app\static;static" --add-data "app\database.db;." app\app.py
--> 