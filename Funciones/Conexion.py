from flask import redirect, session, render_template, request, flash
from functools import wraps
import mysql.connector
import datetime

def get_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='Gestor3'
    )

# ------------------------
# Decorador para login
# ------------------------
def login_requerido(f):
    @wraps(f)
    def decorada(*args, **kwargs):
        if 'user_id' not in session:
            return redirect('/login')
        return f(*args, **kwargs)
    return decorada

# ------------------------
# Login
# ------------------------
def login(Correo, Contraseña):
    if request.method == 'POST':
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT u.id, u.nombre, u.apellido, u.correo, u.contraseña, u.id_rango, u.estado, r.nombre 
                FROM usuarios u 
                JOIN rango r ON u.id_rango = r.id_rango 
                WHERE u.correo=%s AND u.contraseña=%s AND u.estado=1
            """, (Correo, Contraseña))
            user = cursor.fetchone()
            if user:
                user_id, nombre, apellido, correo, contra, id_rango, estado, rango_nombre = user
                
                # Si es cobrador (id_rango == 4), obtener id_cobrador real
                if id_rango == 4:
                    cursor.execute("""
                        SELECT id_cobrador FROM cobrador WHERE nombre=%s AND apellido=%s LIMIT 1
                    """, (nombre, apellido))
                    cobrador = cursor.fetchone()
                    if cobrador:
                        user_id = cobrador[0]  # Reemplaza id_usuario por id_cobrador

                session.permanent = True
                session['user_id'] = user_id
                session['nombre'] = nombre
                session['apellido'] = apellido
                session['correo'] = correo
                session['rango'] = id_rango
                session['rango_nombre'] = rango_nombre
                session['estado'] = estado
                cursor.close()
                conn.close()
                return redirect('/home')
            else:
                cursor.close()
                conn.close()
                flash("❌ Correo o contraseña incorrectos")
                return redirect('/login')
        except Exception as e:
            print("❌ Error en login:", e)
            flash("❌ Error interno al iniciar sesión")
            return redirect('/login')
    return render_template('login.html')

# ------------------------
# Registro general y admin
# ------------------------
def register(Nombre, Correo, Contraseña, id_rango=2, datos_extra=None):
    if request.method == 'POST':
        try:
            conn = get_connection()
            cursor = conn.cursor()

            id_rango = int(id_rango)

            cursor.execute("SELECT * FROM usuarios WHERE correo=%s", (Correo,))
            if cursor.fetchone():
                cursor.close()
                conn.close()
                flash("❌ El correo ya existe.")
                return redirect('/register_admin?error=correo_existente')

            cursor.execute("""
                INSERT INTO usuarios (nombre, correo, contraseña, id_rango, estado)
                VALUES (%s, %s, %s, %s, %s)
            """, (Nombre, Correo, Contraseña, id_rango, 1))
            conn.commit()

            # Extra info según el rango
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
            cursor.close()
            conn.close()
            flash("✅ Registro exitoso.")
            return redirect('/register_admin?registro=exitoso')
        except Exception as e:
            print("❌ Error al registrar usuario:", e)
            flash("❌ Error interno al registrar usuario")
            return redirect('/register_admin?error=fallo_en_registro')
    return render_template('register_admin.html')

# ------------------------
# Registrar venta
# ------------------------
def registrar_venta(id_cliente, id_vendedor, id_producto, fecha, hora):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO factura_venta (id_cliente, id_vende, id_product, fecha, hora)
            VALUES (%s, %s, %s, %s, %s)
        """, (id_cliente, id_vendedor, id_producto, fecha, hora))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print("❌ Error al registrar venta:", e)
        return False

# ------------------------
# Logout
# ------------------------
def logout():
    session.pop('user_id', None)
    session.pop('nombre', None)
    session.pop('apellido', None)
    session.pop('rango', None)
    session.pop('rango_nombre', None)
    session.pop('estado', None)
    return redirect('/login')

# ------------------------
# Obtener clientes asignados a cobrador
# ------------------------

# Obtener clientes asignados al cobrador
def obtener_clientes_de_cobrador(id_cobrador):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT c.* FROM cliente c
        JOIN cobrador_cliente cc ON c.id_cliente = cc.id_cliente
        WHERE cc.id_cobrador = %s
    """, (id_cobrador,))
    clientes = cursor.fetchall()
    cursor.close()
    conn.close()
    return clientes

# Obtener productos comprados por el cliente
def obtener_productos_cliente(id_cliente):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT p.nombre, p.descripcion, p.precio
        FROM factura_venta fv
        JOIN producto p ON fv.id_product = p.id_product
        WHERE fv.id_cliente = %s
    """, (id_cliente,))
    productos = cursor.fetchall()
    cursor.close()
    conn.close()
    return productos

# Obtener abonos realizados por un cliente
def obtener_pagos_cliente(id_cliente):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT monto_abonado AS monto, fecha
        FROM abono_venta
        WHERE id_cliente = %s
        ORDER BY fecha ASC
    """, (id_cliente,))
    pagos = cursor.fetchall()
    cursor.close()
    conn.close()
    return pagos

# Registrar nuevo abono
def registrar_abono(id_cliente, id_cobrador, monto):
    fecha = datetime.today().strftime('%Y-%m-%d')
    conn = get_connection()
    cursor = conn.cursor()
    
    # Buscar la factura de venta más reciente del cliente
    cursor.execute("""
        SELECT id_factura_venta FROM factura_venta
        WHERE id_cliente = %s
        ORDER BY fecha DESC LIMIT 1
    """, (id_cliente,))
    result = cursor.fetchone()

    if result:
        id_factura_venta = result[0]
        cursor.execute("""
            INSERT INTO abono_venta (id_factura_venta, id_cliente, id_cobrador, monto_abonado, fecha)
            VALUES (%s, %s, %s, %s, %s)
        """, (id_factura_venta, id_cliente, id_cobrador, monto, fecha))
        conn.commit()

    cursor.close()
    conn.close()