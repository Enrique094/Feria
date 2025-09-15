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
    """
    Función de registro adaptada para usar solo la tabla usuarios consolidada
    """
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

        # Preparar campos base
        campos_base = ['nombre', 'correo', 'contraseña', 'id_rango', 'estado']
        valores_base = [Nombre, Correo, Contraseña, id_rango, 1]

        # Agregar datos extra si existen
        if datos_extra:
            if datos_extra.get("apellido"):
                campos_base.append('apellido')
                valores_base.append(datos_extra.get("apellido"))

            if datos_extra.get("telefono"):
                campos_base.append('telefono')
                valores_base.append(datos_extra.get("telefono"))

            if datos_extra.get("DUI"):
                campos_base.append('DUI')
                valores_base.append(datos_extra.get("DUI"))

            if datos_extra.get("direccion"):
                campos_base.append('direccion')
                valores_base.append(datos_extra.get("direccion"))

        # Construir query dinámico
        campos_str = ', '.join(campos_base)
        placeholders = ', '.join(['%s'] * len(valores_base))
        query = f"INSERT INTO usuarios ({campos_str}) VALUES ({placeholders})"

        # Ejecutar inserción
        cursor.execute(query, valores_base)
        conn.commit()

        # Obtener ID del usuario recién creado
        id_usuario = cursor.lastrowid

        cursor.close()
        conn.close()

        # Mensaje de éxito
        rangos_nombres = {1: 'Administrador', 2: 'Cliente', 3: 'Vendedor', 4: 'Cobrador'}
        rango_nombre = rangos_nombres.get(id_rango, 'Usuario')

        flash(f"✅ {rango_nombre} '{Nombre}' registrado exitosamente.")
        return redirect('/register_admin?registro=exitoso')

    except mysql.connector.IntegrityError as e:
        if 'correo' in str(e):
            flash("❌ El correo ya está registrado.")
        elif 'DUI' in str(e):
            flash("❌ El DUI ya está registrado.")
        else:
            flash("❌ Ya existe un registro con esos datos.")
        print(f"❌ Error de integridad: {e}")
        return redirect('/register_admin?error=datos_duplicados')

    except Exception as e:
        print(f"❌ Error al registrar usuario: {e}")
        flash(f"❌ Error interno al registrar usuario: {str(e)}")
        return redirect('/register_admin?error=fallo_en_registro')

def registrar_venta(id_cliente, id_vendedor, id_producto, fecha, hora, total=0, cuotas=1, precio_mensual=0, interes_aplicado=0, es_credito=0, direccion=""):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Obtener un cobrador por defecto (el primero disponible)
        cursor.execute("SELECT id FROM usuarios WHERE id_rango = 4 AND estado = 1 LIMIT 1")
        cobrador_result = cursor.fetchone()
        if not cobrador_result:
            print("❌ No hay cobradores disponibles")
            return False
        
        id_cobrador = cobrador_result[0]
        
        # USAR LOS NOMBRES CORRECTOS DE LAS COLUMNAS DE TU BD
        cursor.execute("""
            INSERT INTO factura_venta (
                id_cliente, id_cobrador, id_vendedor, id_product, interes_aplicado, es_credito,
                estado_pago, monto_abonado, total, cuotas, precio_mensual,
                fecha, hora, direccion
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            id_cliente, id_cobrador, id_vendedor, id_producto, interes_aplicado, es_credito,
            'pendiente', 0.00, total, cuotas, precio_mensual,
            fecha, hora, direccion
        ))

        conn.commit()
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error al registrar venta: {e}")
        if conn:
            conn.rollback()
        cursor.close()
        conn.close()
        return False





# ------------------------
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
    """Obtener ventas con nombres de columnas correctos"""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT fv.id_factura_venta, fv.fecha, fv.hora, fv.total, fv.cuotas, fv.precio_mensual,
                   fv.estado_pago, fv.monto_abonado,
                   cli.nombre AS cliente, cli.apellido AS cliente_apellido,
                   p.nombre AS producto, 
                   ven.nombre AS vendedor, ven.apellido AS vendedor_apellido,
                   cb.nombre AS cobrador, cb.apellido AS cobrador_apellido
            FROM factura_venta fv
            JOIN usuarios cli ON fv.id_cliente = cli.id
            JOIN producto p ON fv.id_product = p.id_product
            JOIN usuarios ven ON fv.id_vendedor = ven.id
            LEFT JOIN usuarios cb ON fv.id_cobrador = cb.id
            ORDER BY fv.fecha DESC, fv.hora DESC
        """)
        ventas = cursor.fetchall()
        return ventas
    except Exception as e:
        print(f"❌ Error al obtener ventas: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

# ------------------------
# Asignar cobrador
# ------------------------
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








