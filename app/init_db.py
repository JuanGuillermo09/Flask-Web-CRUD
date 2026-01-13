import sqlite3

# Conectarse (crea database.db si no existe)
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# ---------------------------
# 1️⃣ Crear tabla usuarios
# ---------------------------
cursor.execute('''
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL
)
''')

# Verificar si usuario 'admin' ya existe
cursor.execute("SELECT * FROM usuarios WHERE username = ?", ('admin',))
user = cursor.fetchone()

if user:
    print("ℹ Usuario 'admin' ya existe en la base de datos.")
else:
    cursor.execute('INSERT INTO usuarios (username, password) VALUES (?, ?)', ('admin', '1234'))
    print("✅ Usuario 'admin' insertado correctamente.")

# ---------------------------
# 2️⃣ Crear tabla formularios
# ---------------------------
cursor.execute('''
CREATE TABLE IF NOT EXISTS formularios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_completo VARCHAR(100),
    correo_electronico VARCHAR(50),
    numero_telefono NUMERIC,
    comentarios TEXT,
    created_at TEXT
)
''')

# ---------------------------
# 3️⃣ Agregar columna created_at si no existe
# ---------------------------
try:
    cursor.execute("ALTER TABLE formularios ADD COLUMN created_at TEXT")
    print("✅ Columna 'fecha_creacion DATETIME' agregada correctamente a 'formularios'.")
except sqlite3.OperationalError:
    print("ℹ La columna 'created_at' ya existe en 'formularios'.")

# ---------------------------
# Guardar cambios y cerrar
# ---------------------------
conn.commit()
conn.close()

print("🎉 Base de datos lista para usar con Flask.")
