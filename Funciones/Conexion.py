from flask import redirect, session, render_template, request, flash
from functools import wraps
import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='Gestor'
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
def registrar_venta(id_cliente, id_vendedor, id_producto, id_categoria, monto, fecha, hora):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO factura_venta (id_cliente, id_vende, id_product, id_catego, fecha, hora, monto)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (id_cliente, id_vendedor, id_producto, id_categoria, fecha, hora, monto))
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
def obtener_clientes_de_cobrador(id_cobrador):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT c.id_cliente AS id, c.nombre AS nombre, c.apellido 
            FROM cliente c
            JOIN cobrador_cliente cc ON cc.id_cliente = c.id_cliente
            WHERE cc.id_cobrador = %s
        """, (id_cobrador,))
        clientes = cursor.fetchall()
        cursor.close()
        conn.close()
        return clientes
    except Exception as e:
        print("❌ Error al obtener clientes del cobrador:", e)
        return []

# ------------------------
# Obtener productos comprados por cliente
# ------------------------
def obtener_productos_cliente(id_cliente):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT p.nombre, p.precio 
            FROM producto p
            JOIN contrato c ON c.id_cliente = %s AND c.id_cobrador = (SELECT id_cobrador FROM cobrador WHERE id_cobrador = c.id_cobrador LIMIT 1) AND c.id_cliente = %s
            WHERE p.id_product = c.id_producto
        """, (id_cliente, id_cliente))
        productos = cursor.fetchall()
        cursor.close()
        conn.close()
        return productos
    except Exception as e:
        print("❌ Error al obtener productos del cliente:", e)
        return []

# ------------------------
# Obtener pagos realizados por cliente
# ------------------------
def obtener_pagos_cliente(id_cliente):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT monto FROM factura_cobro WHERE id_cliente = %s
        """, (id_cliente,))
        pagos = cursor.fetchall()
        cursor.close()
        conn.close()
        return pagos
    except Exception as e:
        print("❌ Error al obtener pagos del cliente:", e)
        return []

# ------------------------
# Registrar abono
# ------------------------
def registrar_abono(id_cliente, id_cobrador, monto):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO factura_cobro (id_cliente, id_cobrador, monto, fecha, id_zona)
            VALUES (
                %s,
                %s,
                %s,
                NOW(),
                (SELECT id_zona FROM cobrador WHERE id_cobrador = %s LIMIT 1)
            )
        """, (id_cliente, id_cobrador, monto, id_cobrador))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print("❌ Error al registrar abono:", e)

def registrar_abono(id_cliente, id_cobrador, monto):
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='Gestor'
    )
    cursor = conn.cursor()

    # Obtiene la factura más reciente del cliente
    cursor.execute("""
        SELECT id FROM factura_venta 
        WHERE id_cliente = %s 
        ORDER BY fecha DESC LIMIT 1
    """, (id_cliente,))
    factura = cursor.fetchone()
    id_factura = factura[0] if factura else None

    if id_factura:
        cursor.execute("""
            INSERT INTO abonos (id_cliente, id_cobrador, monto, id_factura)
            VALUES (%s, %s, %s, %s)
        """, (id_cliente, id_cobrador, monto, id_factura))
        conn.commit()
    
    cursor.close()
    conn.close()

def obtener_historial_abonos(id_cliente):
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='Gestor'
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT monto, fecha FROM abonos 
        WHERE id_cliente = %s
        ORDER BY fecha DESC
    """, (id_cliente,))
    historial = cursor.fetchall()
    cursor.close()
    conn.close()
    return historial

