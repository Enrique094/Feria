from flask import redirect, session, render_template, request, flash
from functools import wraps
import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='GestorPlus'
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
                SELECT u.id, u.nombre, u.apellido, u.correo, u.contraseña, 
                       u.id_rango, u.estado, r.nombre 
                FROM usuarios u 
                JOIN rango r ON u.id_rango = r.id_rango 
                WHERE u.correo=%s AND u.contraseña=%s AND u.estado=1
            """, (Correo, Contraseña))
            user = cursor.fetchone()
            if user:
                user_id, nombre, apellido, correo, contra, id_rango, estado, rango_nombre = user

                session.permanent = True
                session['user_id'] = user_id
                session['nombre'] = nombre
                session['apellido'] = apellido
                session['correo'] = correo
                session['rango'] = id_rango
                session['rango_nombre'] = rango_nombre
                session['estado'] = estado

                # 🔹 Guardar IDs reales según el rol
                if id_rango == 2:  # Vendedor
                    cursor.execute("SELECT id_vendedor FROM vendedor WHERE id_usuario=%s LIMIT 1", (user_id,))
                    vendedor = cursor.fetchone()
                    session['vendedor_id'] = vendedor[0] if vendedor else None

                elif id_rango == 3:  # Cliente
                    cursor.execute("SELECT id_cliente FROM cliente WHERE id_usuario=%s LIMIT 1", (user_id,))
                    cliente = cursor.fetchone()
                    session['cliente_id'] = cliente[0] if cliente else None

                elif id_rango == 4:  # Cobrador
                    cursor.execute("SELECT id_cobrador FROM cobrador WHERE id_usuario=%s LIMIT 1", (user_id,))
                    cobrador = cursor.fetchone()
                    session['cobrador_id'] = cobrador[0] if cobrador else None

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

            # Verificar si ya existe el correo
            cursor.execute("SELECT * FROM usuarios WHERE correo=%s", (Correo,))
            if cursor.fetchone():
                cursor.close()
                conn.close()
                flash("❌ El correo ya existe.")
                return redirect('/register_admin?error=correo_existente')

            # Insertar en usuarios
            cursor.execute("""
                INSERT INTO usuarios (nombre, correo, contraseña, id_rango, estado)
                VALUES (%s, %s, %s, %s, %s)
            """, (Nombre, Correo, Contraseña, id_rango, 1))
            conn.commit()

            # 🔹 Guardar el ID de usuario recién creado
            id_usuario = cursor.lastrowid

            # Insertar en la tabla correspondiente según el rango
            if datos_extra:
                if id_rango == 2:  # Cliente
                    cursor.execute("""
                        INSERT INTO cliente (id_usuario, nombre, apellido, id_rango, tel, dui, correo, direccion)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                        id_usuario,
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
                        INSERT INTO vendedor (id_usuario, nombre, apellido, tel, id_rango, id_zona)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (
                        id_usuario,
                        Nombre,
                        datos_extra.get("vendedor_apellido", ""),
                        datos_extra.get("vendedor_tel", ""),
                        id_rango,
                        int(datos_extra.get("vendedor_zona", 1))
                    ))

                elif id_rango == 4:  # Cobrador
                    cursor.execute("""
                        INSERT INTO cobrador (id_usuario, nombre, apellido, tel, id_rango, id_zona)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (
                        id_usuario,
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

def obtener_ventas():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT fv.id_factura_venta, fv.fecha, fv.hora, fv.total, fv.cuotas, fv.precio_mensual,
               c.nombre AS cliente, 
               p.nombre AS producto, 
               v.nombre AS vendedor, 
               cb.nombre AS cobrador
        FROM factura_venta fv
        JOIN cliente c ON fv.id_cliente = c.id_cliente
        JOIN producto p ON fv.id_product = p.id_product
        JOIN vendedor v ON fv.id_vende = v.id_vende
        LEFT JOIN cobrador cb ON fv.id_cobrador = cb.id_cobrador
    """)
    ventas = cursor.fetchall()
    cursor.close()
    conn.close()
    return ventas



def asignar_cobrador(id_factura_venta, id_cobrador):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE factura_venta
        SET id_cobrador = %s
        WHERE id_factura_venta = %s
    """, (id_cobrador, id_factura_venta))
    conn.commit()
    cursor.close()
    conn.close()
    return True

def obtener_cobradores():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT c.id_cobrador, u.nombre, u.apellido
        FROM cobrador c
        JOIN usuarios u ON c.id_usuario = u.id
    """)
    cobradores = cursor.fetchall()
    conn.close()
    return cobradores








