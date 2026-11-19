from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# Configuración de ruta segura para la base de datos en servidores cloud
def get_db():
    db_path = os.path.join(os.path.dirname(__file__), 'escuela_cloud.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

# Inicialización automática de la tabla en la nube
with get_db() as conn:
    conn.execute('''CREATE TABLE IF NOT EXISTS alumnos 
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                     nombre TEXT NOT NULL, 
                     p1 REAL, p2 REAL, p3 REAL)''')
    conn.commit()

@app.route('/')
def inicio():
    try:
        conn = get_db()
        alumnos = conn.execute('SELECT *, (p1+p2+p3)/3.0 AS promedio FROM alumnos').fetchall()
        conn.close()
    except Exception:
        alumnos = []
    return render_template('index.html', alumnos=alumnos)

@app.route('/guardar', methods=['POST'])
def guardar():
    try:
        nombre = request.form.get('nombre', 'Sin Nombre').strip()
        p1 = float(request.form.get('p1', 0))
        p2 = float(request.form.get('p2', 0))
        p3 = float(request.form.get('p3', 0))
        
        conn = get_db()
        conn.execute('INSERT INTO alumnos (nombre, p1, p2, p3) VALUES (?, ?, ?, ?)',
                     (nombre, p1, p2, p3))
        conn.commit()
        conn.close()
    except Exception:
        pass
        
    return redirect(url_for('inicio'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
