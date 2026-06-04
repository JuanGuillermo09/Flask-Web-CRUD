from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import sqlite3
from datetime import datetime
import sys
import os

# ----------------------------
# Función para PyInstaller
# ----------------------------
def resource_path(relative_path):
    """Obtiene la ruta absoluta de los recursos, funciona con .exe de PyInstaller"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Ruta de la base de datos
# Reemplaza esto:
conn = sqlite3.connect('database.db')

# Por esto:
import os
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "database.db")
conn = sqlite3.connect(db_path)
# ----------------------------
# Crear la aplicación Flask
# ----------------------------
app = Flask(__name__)
app.secret_key = 'clave_secreta_para_sesiones'  # Clave para manejar sesiones seguras


# ----------------------------
# RUTA: Cerrar sesión
# ----------------------------
@app.route('/logout')
def logout():
    """
    Cierra la sesión del usuario actual.

    Elimina todos los datos de sesión y redirige al formulario de inicio de sesión.
    Retorna:
        redirect: Redirección a la ruta de login.
    """
    session.clear()
    flash("Has cerrado sesión correctamente")
    return redirect(url_for('login'))


# ----------------------------
# RUTA: Login
# ----------------------------
@app.route('/', methods=['GET', 'POST'])
def login():
    """
    Muestra el formulario de login o procesa el inicio de sesión.

    Métodos:
        GET: Renderiza el formulario de login.
        POST: Valida las credenciales del usuario en la base de datos.

    Retorna:
        render_template: Si es GET o credenciales incorrectas.
        redirect: Si el usuario inicia sesión correctamente, lo lleva a /index.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['user'] = username
            return redirect(url_for('index'))
        else:
            flash("Usuario o contraseña incorrectos")
            return redirect(url_for('login'))

    return render_template('login.html')


# ----------------------------
# RUTA: Página principal protegida
# ----------------------------
@app.route('/index', methods=['GET'])
def index():
    """
    Muestra la página principal con los registros guardados.

    Solo accesible si hay un usuario en sesión.
    Retorna:
        render_template: La página principal con los registros en una tabla.
    """
    if 'user' not in session:
        return redirect(url_for('login'))

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre_completo, correo_electronico, numero_telefono, comentarios, created_at FROM formularios")
    registros = cursor.fetchall()
    conn.close()

    registros_dict = []
    for r in registros:
        registros_dict.append({
            'id': r[0],
            'nombre': r[1],
            'email': r[2],
            'telefono': r[3],
            'comentarios': r[4],
            'created_at': r[5]
        })

    return render_template('index.html', registros=registros_dict)


# ----------------------------
# RUTA: Guardar o actualizar formulario
# ----------------------------
@app.route('/submit', methods=['POST'])
def submit():
    """
    Inserta un nuevo registro o actualiza uno existente en la base de datos.

    Parámetros (POST form):
        id (opcional): ID del registro existente para actualizar.
        nombre (str): Nombre completo.
        email (str): Correo electrónico.
        telefono (str): Número de teléfono.
        comentarios (str): Comentarios del usuario.

    Retorna:
        redirect: Redirección a la página principal tras guardar.
    """
    id = request.form.get('id')
    nombre = request.form['nombre']
    email = request.form['email']
    telefono = request.form['telefono']
    comentarios = request.form['comentarios']
    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    if id:
        cursor.execute("""
            UPDATE formularios
            SET nombre_completo=?, correo_electronico=?, numero_telefono=?, comentarios=?
            WHERE id=?
        """, (nombre, email, telefono, comentarios, id))
    else:
        cursor.execute("""
            INSERT INTO formularios (nombre_completo, correo_electronico, numero_telefono, comentarios, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (nombre, email, telefono, comentarios, created_at))

    conn.commit()
    conn.close()

    flash('Registro guardado correctamente')
    return redirect(url_for('index'))


# ----------------------------
# RUTA: Eliminar registro
# ----------------------------
@app.route('/delete', methods=['POST'])
def delete():
    """
    Elimina un registro de la base de datos.

    Parámetros (POST form):
        id (int): Identificador del registro a eliminar.

    Retorna:
        Response: Código 200 si la eliminación fue exitosa.
    """
    id = request.form.get('id')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM formularios WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return '', 200


# ----------------------------
# INICIAR SERVIDOR
# ----------------------------
if __name__ == '__main__':
    """
    Punto de entrada principal del servidor Flask.
    Ejecuta la aplicación en modo debug.
    """
    app.run(debug=True)
