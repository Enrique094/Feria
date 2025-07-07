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

from flask import redirect, session, render_template, request
import mysql.connector

def register(Nombre, Correo, Contraseña, id_rango=2, datos_extra=None):
    if request.method == 'POST':
        try:
            conn = get_connection()
            cursor = conn.cursor()

            # Convertir rango a entero si viene como string
            id_rango = int(id_rango)

            # Verificar si el correo ya está en uso
            cursor.execute("SELECT * FROM usuarios WHERE correo=%s", (Correo,))
            if cursor.fetchone():
                return redirect('/register_admin?error=correo_existente')

            # Insertar en tabla usuarios
            cursor.execute("""
                INSERT INTO usuarios (nombre, correo, contraseña, id_rango, estado)
                VALUES (%s, %s, %s, %s, %s)
            """, (Nombre, Correo, Contraseña, id_rango, 1))
            conn.commit()

            # Insertar en tabla correspondiente al rango
            if datos_extra:
                if id_rango == 2:  # Cliente
                    cursor.execute("""
                        INSERT INTO cliente (nombre, apellido, id_rango, tel, dui, correo, direccion)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """, (
                        Nombre,
                        datos_extra.get("cliente_apellido", ""),
                        id_rango,
                        datos_extra.get("cliente_tel", ""),
                        datos_extra.get("cliente_dui", ""),
                        Correo,
                        datos_extra.get("cliente_direccion", "")
                    ))

                elif id_rango == 3:  # Vendedor
                    cursor.execute("""
                        INSERT INTO vendedor (nombre, apellido, tel, id_rango, id_zona)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (
                        Nombre,
                        datos_extra.get("vendedor_apellido", ""),
                        datos_extra.get("vendedor_tel", ""),
                        id_rango,
                        int(datos_extra.get("vendedor_zona", 1))
                    ))

                elif id_rango == 4:  # Cobrador
                    cursor.execute("""
                        INSERT INTO cobrador (nombre, apellido, tel, id_rango, id_zona)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (
                        Nombre,
                        datos_extra.get("cobrador_apellido", ""),
                        datos_extra.get("cobrador_tel", ""),
                        id_rango,
                        int(datos_extra.get("cobrador_zona", 1))
                    ))

            conn.commit()
            return redirect('/register_admin?registro=exitoso')

        except Exception as e:
            print("❌ Error al registrar usuario:", str(e))
            return redirect('/register_admin?error=fallo_en_registro')

        finally:
            if cursor: cursor.close()
            if conn: conn.close()

    # Si es GET, solo devuelve el HTML
    return render_template('register_admin.html')





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
