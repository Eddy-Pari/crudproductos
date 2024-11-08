from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

import sqlite3

# Conexión y creación de la base de datos
conn = sqlite3.connect('almacen.db')
cursor = conn.cursor()

# Crear la tabla producto
conn.execute("""CREATE TABLE IF NOT EXISTS producto (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                descripcion TEXT NOT NULL,
                cantidad INTEGER NOT NULL,
                precio REAL NOT NULL
            )
            """)

# Cerrar conexión
conn.commit()
conn.close()

# Conectar a la base de datos
def get_db_connection():
    conn = sqlite3.connect('almacen.db')
    conn.row_factory = sqlite3.Row
    return conn

# Ruta para ver todos los productos (Read)
@app.route('/')
def index():
    conn = get_db_connection()
    productos = conn.execute('SELECT * FROM producto').fetchall()
    conn.close()
    return render_template('index.html', productos=productos)

# Ruta para crear un nuevo producto (Create)
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        descripcion = request.form['descripcion']
        cantidad = request.form['cantidad']
        precio = request.form['precio']

        conn = get_db_connection()
        conn.execute('INSERT INTO producto (descripcion, cantidad, precio) VALUES (?, ?, ?)',
                     (descripcion, cantidad, precio))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('create.html')

# Ruta para actualizar un producto (Update)
@app.route('/<int:id>/update', methods=('GET', 'POST'))
def update(id):
    conn = get_db_connection()
    producto = conn.execute('SELECT * FROM producto WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        descripcion = request.form['descripcion']
        cantidad = request.form['cantidad']
        precio = request.form['precio']

        conn.execute('UPDATE producto SET descripcion = ?, cantidad = ?, precio = ? WHERE id = ?',
                     (descripcion, cantidad, precio, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    conn.close()
    return render_template('update.html', producto=producto)

# Ruta para eliminar un producto (Delete)
@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM producto WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == "__name__":
    app.run(debug=True)