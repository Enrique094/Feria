from flask import redirect, session, render_template, request
from functools import wraps
import mysql.connector

def get_connection():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',  # Deja en blanco si no has establecido una contraseña
        database='Gestor' # Cambia 'Pruebas' por el nombre de tu base de datos
    )
    return conn

def login_requerido(f):
    @wraps(f)
    def decorada(*args, **kwargs):
        if 'user_id' not in session:
            return redirect('/login')
        return f(*args, **kwargs)
    return decorada


def login(Correo, Contraseña):
    if request.method == 'POST':
        conn = get_connection()
        with conn.cursor() as cursor:
            # Comparar la contraseña en texto plano con la base de datos
            cursor.execute("SELECT * FROM usuarios WHERE correo=%s AND contraseña=%s AND estado=1", (Correo, Contraseña))
            user = cursor.fetchone()
        conn.close()

        if user:
            session.permanent = True
            session['user_id'] = user[0]   # ID
            session['nombre'] = user[1]    # Nombre
            session['rango'] = user[4]     # Rango (si está en la 5ta columna)
            session['estado'] = user[5]     # Estado (si está en la 6ta columna)
            return redirect('/home')
        else:
            return redirect('/login')  # Puedes usar flash() para mensaje de error

    return render_template('login.html')


def Productos(nombre, descripcion, precio, imagen, cantidad, categoria):
    if request.method == 'POST':
        conn = get_connection()
        with conn.cursor() as cursor:
            # Insertar nuevo producto en la base de datos
            cursor.execute("""
                INSERT INTO productos (nombre, descripcion, precio, imagen, cantidad, categoria) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (nombre, descripcion, precio, imagen, cantidad, categoria))
            conn.commit()
        conn.close()
        return {"message": "Producto creado exitosamente"}
    
    elif request.method == 'GET':
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM productos WHERE estado=1")
            productos = cursor.fetchall()
        conn.close()
        return productos

def register(Nombre, Correo, Contraseña, id_rango):
    if request.method == 'POST':
        conn = get_connection()
        with conn.cursor() as cursor:
            # Verificar si el correo ya existe
            cursor.execute("SELECT * FROM usuarios WHERE correo=%s", (Correo,))
            existente = cursor.fetchone()
            if existente:
                return redirect('/login')  # El correo ya está registrado

            # Insertar nuevo usuario
            cursor.execute("INSERT INTO usuarios (nombre, correo, contraseña, id_rango, estado) VALUES (%s, %s, %s, %s, %s)",
                        (Nombre, Correo, Contraseña, id_rango, 1))
            conn.commit()
        conn.close()

        return redirect('/login')

    return render_template('register.html')

def logout():
    session.pop('user_id', None)
    session.pop('nombre', None)
    session.pop('rango', None)
    return redirect('/login')
