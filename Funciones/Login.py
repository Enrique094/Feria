from flask import redirect, session, render_template, request, flash
from functools import wraps
import mysql.connector
import hashlib
from Funciones import confi
from router.admin import admin_bp 

def get_connection():
    conn = mysql.connector.connect(
        host=confi.host,
        user=confi.user,
        password = confi.password,  # Deja en blanco si no has establecido una contraseña
        database=confi.database
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
        # Convertimos la contraseña ingresada a hash
        contraseña_hash = hashlib.sha256(Contraseña.encode()).hexdigest()

        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM usuarios WHERE correo=%s AND contraseña=%s AND estado=1", (Correo, contraseña_hash))
            user = cursor.fetchone()
        conn.close()

        if user:
            session.permanent = True
            session['user_id'] = user[0]
            session['nombre'] = user[1]
            session['rango'] = user[4]
            session['estado'] = user[5]
            return redirect('/')
        else:
            flash('Usuario o contraseña incorrectos, Verifique si su cuenta está activa.') 
            return redirect('/login')

    return render_template('login.html')



@admin_bp.route('/adduser', methods=['GET', 'POST'])
@login_requerido
def register(Nombre, Correo, Contraseña, Rango):
    if request.method == 'POST':
        # Hasheamos la contraseña
        contraseña_hash = hashlib.sha256(Contraseña.encode()).hexdigest()

        conn = get_connection()
        with conn.cursor() as cursor:
            # Verificar si el correo ya existe
            cursor.execute("SELECT * FROM usuarios WHERE correo=%s", (Correo,))
            existente = cursor.fetchone()
            if existente:
                return redirect('/')  # El correo ya está registrado

            # Insertar nuevo usuario con la contraseña hasheada
            cursor.execute("INSERT INTO usuarios (nombre, correo, contraseña, rango, estado) VALUES (%s, %s, %s, %s, %s)",
                   (Nombre, Correo, contraseña_hash, Rango, 1))
            conn.commit()
        conn.close()

        return redirect('/admin')

    return render_template('admin.html')


def logout():
    session.pop('user_id', None)
    session.pop('nombre', None)
    session.pop('rango', None)
    return redirect('/login')
