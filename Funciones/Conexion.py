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
            # Buscar al usuario junto con el nombre del rango
            cursor.execute("""
                SELECT u.id, u.nombre, u.correo, u.id_rango, u.estado, r.nombre 
                FROM usuarios u 
                JOIN rango r ON u.id_rango = r.id_rango 
                WHERE u.correo=%s AND u.contraseña=%s AND u.estado=1
            """, (Correo, Contraseña))
            user = cursor.fetchone()
        conn.close()

        if user:
            session.permanent = True
            session['user_id'] = user[0]        # ID usuario
            session['nombre'] = user[1]         # Nombre
            session['rango'] = user[3]          # id_rango (por ejemplo: 1)
            session['estado'] = user[4]         # Estado
            session['rango_nombre'] = user[5]   # 'Administrador', 'Vendedor', etc.
            return redirect('/home')
        else:
            return redirect('/login')  # Puedes usar flash para error

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

def register(Nombre, Correo, Contraseña, id_rango=2):
    if request.method == 'POST':
        conn = get_connection()
        cursor = conn.cursor()

        # Verificar si ya existe ese correo
        cursor.execute("SELECT * FROM usuarios WHERE correo=%s", (Correo,))
        existente = cursor.fetchone()
        if existente:
            cursor.close()
            conn.close()
            return redirect('/login')  # El usuario ya está registrado

        # Insertar en tabla usuarios
        cursor.execute("""
            INSERT INTO usuarios (nombre, correo, contraseña, id_rango, estado)
            VALUES (%s, %s, %s, %s, %s)
        """, (Nombre, Correo, Contraseña, id_rango, 1))
        conn.commit()

        # Obtener ID insertado
        cursor.execute("SELECT LAST_INSERT_ID()")
        nuevo_id = cursor.fetchone()[0]

        # Registrar en la tabla específica según el rango
        if id_rango == '2':  # Cliente
            cursor.execute("""
                INSERT INTO cliente (nombre, apellido, id_rango, tel, dui, correo, direccion)
                VALUES (%s, '', %s, '', '', %s, '')
            """, (Nombre, id_rango, Correo))
        
        elif id_rango == '3':  # Vendedor
            cursor.execute("""
                INSERT INTO vendedor (nombre, apellido, tel, id_rango, id_zona)
                VALUES (%s, '', '', %s, 1)
            """, (Nombre, id_rango))
        
        elif id_rango == '4':  # Cobrador
            cursor.execute("""
                INSERT INTO cobrador (nombre, apellido, tel, id_rango, id_zona)
                VALUES (%s, '', '', %s, 1)
            """, (Nombre, id_rango))

        conn.commit()
        cursor.close()
        conn.close()

        return redirect('/login')

    return render_template('register.html')


def registrar_venta(id_cliente, id_vendedor, id_producto, id_categoria, monto, fecha, hora):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO factura_venta (id_cliente, id_vende, id_product, id_catego, fecha, hora, monto)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (id_cliente, id_vendedor, id_producto, id_categoria, fecha, hora, monto))
        conn.commit()
        return True
    except Exception as e:
        print("Error al registrar venta:", e)
        return False
    finally:
        cursor.close()
        conn.close()



def logout():
    session.pop('user_id', None)
    session.pop('nombre', None)
    session.pop('rango', None)
    return redirect('/login')
