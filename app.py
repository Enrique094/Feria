from flask import Flask, render_template, redirect, request, session, url_for, flash, send_file
from Funciones import Conexion
from datetime import datetime, date
import mysql.connector
from functools import wraps
import io
import calendar
from decimal import Decimal
from Funciones.PDF import recibos_bp
app = Flask(__name__)
app.secret_key = 'Quemen el ina'

def get_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='Gestor'
    )

def admin_required(f):
    @wraps(f)
    def decorada(*args, **kwargs):
        if 'rango' not in session or session['rango'] != 1:
            flash("❌ Acceso denegado. Solo administradores pueden acceder a esta página.")
            return redirect('/home')
        return f(*args, **kwargs)
    return decorada

def to_float(value):
    """Convierte valores Decimal o string a float de manera segura"""
    if isinstance(value, Decimal):
        return float(value)
    elif isinstance(value, str):
        try:
            return float(value)
        except ValueError:
            return 0.0
    return float(value) if value is not None else 0.0

# Registrar Blueprints
# ======================
app.register_blueprint(recibos_bp)

def generar_tabla_meses(fecha_inicio, total_cuotas, precio_mensual, historial_abonos):
    """Genera una tabla de meses mostrando estado de pagos"""
    meses = []
    # Convertir fecha_inicio a datetime si es necesario
    if isinstance(fecha_inicio, str):
        fecha_actual = datetime.strptime(fecha_inicio, '%Y-%m-%d')
    else:
        fecha_actual = fecha_inicio

    if total_cuotas == 0:  # contado
        total_cuotas = 1

    # Crear diccionario de abonos por mes-año (ej: "09-2025")
    abonos_por_mes = {}
    for abono in historial_abonos:
        key = f"{str(abono[3]).zfill(2)}-{abono[4]}"
        if key not in abonos_por_mes:
            abonos_por_mes[key] = []
        abonos_por_mes[key].append({
            'monto': abono[1],
            'fecha': abono[2],
            'observaciones': abono[6] if len(abono) > 6 else ''
        })

    # Mostrar todas las cuotas (no limitar a 12)
    meses_a_mostrar = max(1, int(total_cuotas))
    hoy = datetime.today().date()

    for i in range(meses_a_mostrar):
        año = fecha_actual.year
        mes = fecha_actual.month + i

        # Ajustar año si el mes supera 12
        while mes > 12:
            mes -= 12
            año += 1

        mes_key = f"{str(mes).zfill(2)}-{año}"

        estado = 'pendiente'
        abonos_mes = abonos_por_mes.get(mes_key, [])
        total_abonado_mes = sum(abono['monto'] for abono in abonos_mes)

        if total_abonado_mes >= float(precio_mensual):
            estado = 'pagado'
        elif total_abonado_mes > 0:
            estado = 'parcial'

        # Marcar vencido si ya pasó el mes y no está pagado
        fecha_mes = date(año, mes, 1)
        if estado != "pagado" and fecha_mes < hoy.replace(day=1):
            estado = "vencido"

        # Nombre del mes
        mes_nombre = calendar.month_name[mes] + f" {año}"

        meses.append({
            'numero': i + 1,
            'mes_nombre': mes_nombre,
            'mes': mes,
            'año': año,
            'cuota_esperada': float(precio_mensual),
            'total_abonado': total_abonado_mes,
            'estado': estado,
            'abonos': abonos_mes,
            'pendiente': max(0, float(precio_mensual) - total_abonado_mes)
        })

    return meses



@app.route("/About")
@Conexion.login_requerido
def about():
    return render_template("About.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    correo = request.form.get('correo')
    contraseña = request.form.get('contraseña')
    return Conexion.login(correo, contraseña)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        correo = request.form.get('correo')
        contraseña = request.form.get('contraseña')
        id_rango = 2  # por defecto Cliente
        return Conexion.register(nombre, correo, contraseña, id_rango)

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id_rango, nombre FROM rango")
        rangos = cursor.fetchall()
    except Exception as e:
        rangos = []
        flash(f"❌ Error al obtener rangos: {str(e)}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

    return render_template("register.html", rangos=rangos)

@app.route('/register_admin', methods=['GET', 'POST'])
@Conexion.login_requerido
@admin_required
def register_admin():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        nombre = request.form.get('nombre')
        correo = request.form.get('correo')
        contraseña = request.form.get('contraseña')
        id_rango = int(request.form.get('rango'))
        
        # Recopilar datos extra según el rango
        datos_extra = {}
        
        if id_rango == 2:  # Cliente
            datos_extra = {
                "apellido": request.form.get("cliente_apellido"),
                "telefono": request.form.get("cliente_tel"),
                "DUI": request.form.get("cliente_dui"),
                "direccion": request.form.get("cliente_direccion")
            }
        elif id_rango == 3:  # Vendedor
            datos_extra = {
                "apellido": request.form.get("vendedor_apellido"),
                "telefono": request.form.get("vendedor_tel"),
            }
        elif id_rango == 4:  # Cobrador
            datos_extra = {
                "apellido": request.form.get("cobrador_apellido"),
                "telefono": request.form.get("cobrador_tel"),
            }
        
        conn.close()
        return Conexion.register(nombre, correo, contraseña, id_rango, datos_extra)

    try:
        # Obtener todos los usuarios con información de rango
        cursor.execute("""
            SELECT u.*, r.nombre as rango_nombre 
            FROM usuarios u 
            LEFT JOIN rango r ON u.id_rango = r.id_rango 
            ORDER BY u.nombre
        """)
        users = cursor.fetchall()

        cursor.execute("SELECT id_rango, nombre FROM rango")
        rangos = cursor.fetchall()

            
    except Exception as e:
        flash(f"❌ Error al obtener datos: {str(e)}", "danger")
        users, rangos = [], []
    finally:
        cursor.close()
        conn.close()

    return render_template("register_admin.html", users=users, rangos=rangos)

@app.route('/editar_usuario', methods=['POST'])
@Conexion.login_requerido
@admin_required
def editar_usuario():
    user_id = request.form.get('user_id')
    nombre = request.form.get('nombre')
    apellido = request.form.get('apellido')
    correo = request.form.get('correo')
    telefono = request.form.get('telefono')
    DUI = request.form.get('DUI')
    direccion = request.form.get('direccion')
    estado = request.form.get('estado')
    id_rango = request.form.get('rango')

    conn = get_connection()
    try:
        cursor = conn.cursor()
        
        # Actualizar campos base
        cursor.execute("""
            UPDATE usuarios 
            SET nombre=%s, apellido=%s, correo=%s, telefono=%s, DUI=%s, 
                direccion=%s, estado=%s, id_rango=%s 
            WHERE id=%s
        """, (nombre, apellido, correo, telefono, DUI, direccion, estado, id_rango, user_id))
        
        conn.commit()
        flash("✅ Usuario actualizado correctamente", "success")
        
    except Exception as e:
        conn.rollback()
        flash(f"❌ Error al actualizar usuario: {str(e)}", "danger")
    finally:
        cursor.close()
        conn.close()
        
    return redirect('/register_admin')

@app.route('/eliminar_usuario/<int:user_id>', methods=['POST'])
@Conexion.login_requerido
@admin_required
def eliminar_usuario(user_id):
    conn = get_connection()
    try:
        cursor = conn.cursor()

        # Verificar si el usuario está en facturas (como cliente, vendedor o cobrador)
        cursor.execute("""
            SELECT COUNT(*) FROM factura_venta 
            WHERE id_cliente = %s OR id_vendedor = %s OR id_cobrador = %s
        """, (user_id, user_id, user_id))
        facturas_count = cursor.fetchone()[0]

        # Verificar si el usuario está en abonos
        cursor.execute("SELECT COUNT(*) FROM abono_venta WHERE id_usuario = %s", (user_id,))
        abonos_count = cursor.fetchone()[0]

        if facturas_count > 0 or abonos_count > 0:
            # No eliminar, solo desactivar
            cursor.execute("UPDATE usuarios SET estado = 0 WHERE id = %s", (user_id,))
            flash("⚠️ Usuario desactivado (tiene registros asociados)", "warning")
        else:
            # Eliminar completamente
            cursor.execute("DELETE FROM usuarios WHERE id=%s", (user_id,))
            flash("🗑️ Usuario eliminado completamente", "info")

        conn.commit()

    except Exception as e:
        conn.rollback()
        flash(f"❌ Error al eliminar usuario: {str(e)}", "danger")
    finally:
        cursor.close()
        conn.close()

    return redirect('/register_admin')


@app.route('/logout')
@Conexion.login_requerido
def logout():
    Conexion.logout()
    session.pop('user_id', None)
    return redirect('/login')

@app.route('/home')
@Conexion.login_requerido
def home():
    return render_template('index.html')

@app.route('/')
@Conexion.login_requerido
def index():
    return redirect('/home')

# ------------------------
# Ventas
# ------------------------
@app.route('/registrar_venta', methods=['GET', 'POST'])
@Conexion.login_requerido
def registrar_venta():
    conn = get_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        id_cliente = request.form['cliente']
        id_producto = request.form['producto']
        direccion = request.form['direccion']
        tipo_pago = request.form['tipo_pago']
        meses = request.form.get('meses', 0)

        # Obtener vendedor (usuario actual debe ser vendedor)
        if session.get('rango') != 3:  # Si no es vendedor
            flash("❌ Solo los vendedores pueden registrar ventas.", "danger")
            cursor.close()
            conn.close()
            return redirect(url_for('registrar_venta'))
        
        id_vendedor = session['user_id']

        # NO asignar cobrador (dejar como NULL)
        id_cobrador = None

        if not id_producto:
            flash("❌ Debe seleccionar al menos un producto.", "danger")
            cursor.close()
            conn.close()
            return redirect(url_for('registrar_venta'))

        # Obtener información del producto único
        cursor.execute("SELECT id_product, precio, stock FROM producto WHERE id_product = %s", (id_producto,))
        producto = cursor.fetchone()

        if not producto:
            flash("Producto no encontrado.", "danger")
            cursor.close()
            conn.close()
            return redirect(url_for('registrar_venta'))

        precio_base = float(producto[1])
        stock_disponible = int(producto[2])
        cantidad = int(request.form.get('cantidad', 1))

        if cantidad <= 0:
            flash("La cantidad debe ser mayor a 0.", "danger")
            cursor.close()
            conn.close()
            return redirect(url_for('registrar_venta'))
        

        if cantidad > stock_disponible:
            flash(f"Stock insuficiente. Disponible: {stock_disponible}", "danger")
            cursor.close()
            conn.close()
            return redirect(url_for('registrar_venta'))

        fecha = datetime.today().strftime('%Y-%m-%d')
        hora = datetime.today().strftime('%H:%M:%S')

        try:
            # Configurar según tipo de pago
            subtotal = precio_base * cantidad
            es_credito = 0 if tipo_pago == 'contado' else 1
            cuotas = 1
            interes_aplicado = 0.0
            total = subtotal
            precio_mensual = total

            if tipo_pago == 'credito':
                if not meses or meses == '0':
                    flash("Debe seleccionar un plazo para pago a crédito.", "danger")
                    cursor.close()
                    conn.close()
                    return redirect(url_for('registrar_venta'))

                cuotas = int(meses)
                cursor.execute("SELECT porcentaje FROM intereses WHERE meses = %s", (meses,))
                interes_result = cursor.fetchone()
                
                if not interes_result:
                    flash(f"No se encontró configuración de interés para {meses} meses.", "danger")
                    cursor.close()
                    conn.close()
                    return redirect(url_for('registrar_venta'))

                interes_aplicado = float(interes_result[0])
                total = subtotal * (1 + interes_aplicado / 100)
                precio_mensual = total / cuotas

            # Insertar factura
            cursor.execute("""
                INSERT INTO factura_venta
                (id_cliente, id_cobrador, id_vendedor, id_product, interes_aplicado, es_credito,
                 estado_pago, monto_abonado, total, cuotas, precio_mensual, fecha, hora, direccion, cantidad)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                id_cliente, id_cobrador, id_vendedor, id_producto, interes_aplicado, es_credito,
                'pendiente', 0.0, total, cuotas, precio_mensual, fecha, hora, direccion, cantidad
            ))

            # Actualizar stock
            cursor.execute("UPDATE producto SET stock = stock - %s WHERE id_product = %s", (cantidad, id_producto))

            conn.commit()
            flash("Venta registrada exitosamente.", "success")
        except Exception as e:
            conn.rollback()
            flash(f"❌ Error al registrar la venta: {str(e)}", "danger")
            print(f"Error detallado en registrar_venta: {e}")
            
        finally:
            cursor.close()
            conn.close()
            
        return redirect(url_for('registrar_venta'))

    # GET - mostrar formulario
    try:
        cursor.execute("SELECT id, nombre, apellido FROM usuarios WHERE id_rango = 2 AND estado = 1")
        clientes = cursor.fetchall()
        
        cursor.execute("SELECT id_product, nombre, precio, stock FROM producto WHERE stock > 0")
        productos = cursor.fetchall()
        
        cursor.execute("SELECT meses, porcentaje FROM intereses ORDER BY meses")
        opciones_credito = cursor.fetchall()

        return render_template("registrar_venta.html", 
                             clientes=clientes, 
                             productos=productos, 
                             opciones_credito=opciones_credito)
                             
    except Exception as e:
        flash(f"❌ Error al cargar datos: {str(e)}", "danger")
        print(f"Error al cargar datos: {e}")
        return redirect(url_for('home'))
    finally:
        cursor.close()
        conn.close()
# ===============================

# ------------------------
# Productos 
# ------------------------
@app.route('/productos', methods=['GET', 'POST'])
@Conexion.login_requerido
@admin_required
def productos():
    categorias, productos = [], []
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = float(request.form['precio'])
        stock = int(request.form['cantidad'])
        categoria = request.form['categoria']
        imagen_file = request.files['imagen']
        imagen_blob = imagen_file.read() if imagen_file and imagen_file.filename != '' else None

        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id_categoria FROM categoria WHERE nombre = %s", (categoria,))
            result = cursor.fetchone()
            if not result:
                flash("❌ Categoría no válida")
                return redirect(url_for('productos'))

            id_catego = result[0]
            cursor.execute("""
    INSERT INTO producto (nombre, descripcion, precio, imagen, stock, id_catego, imagen_blob)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
""", (nombre, descripcion, precio, 1 if imagen_blob else 0, stock, id_catego, imagen_blob))


            conn.commit()
            flash("✅ Producto creado exitosamente")
        except Exception as e:
            flash(f"❌ Error al insertar producto: {str(e)}")
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT nombre FROM categoria ORDER BY nombre")
        categorias = [row[0] for row in cursor.fetchall()]
        cursor.execute("SELECT id_product, nombre, descripcion, precio, stock FROM producto")
        productos = cursor.fetchall()
    except Exception as e:
        flash(f"❌ Error al obtener datos: {str(e)}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

    return render_template('productos_blob.html', productos=productos, categorias=categorias)

@app.route('/mostrar_productos')
@Conexion.login_requerido
def mostrar_productos():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id_product, nombre, descripcion, precio, stock FROM producto")
        productos = cursor.fetchall()
    except Exception as e:
        flash(f"❌ Error al obtener productos: {str(e)}")
        productos = []
    finally:
        if cursor: cursor.close()
        if conn: conn.close()
    return render_template("mostrar_productos.html", productos=productos)

@app.route('/imagen/<int:producto_id>')
def obtener_imagen(producto_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT imagen_blob FROM producto WHERE id_product = %s", (producto_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    if result and result[0]:
        return send_file(io.BytesIO(result[0]), mimetype='image/jpeg')
    else:
        return '', 204  # No Content

@app.route('/agregar_categoria', methods=['POST'])
def agregar_categoria():
    nombre = request.form.get('nombre_categoria')
    descripcion = request.form.get('descripcion_categoria')

    cursor = None
    conn = None
    
    if not nombre:
        flash("❌ El nombre de la categoría es obligatorio.")
        return redirect(url_for('productos'))

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO categoria (nombre, descripcion) VALUES (%s, %s)", (nombre, descripcion))
        conn.commit()
        flash("✅ Categoría agregada exitosamente.")
    except Exception as e:
        flash(f"❌ Error al agregar categoría: {str(e)}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

    return redirect(url_for('productos'))

@app.route('/ventas_admin', methods=['GET', 'POST'])
@Conexion.login_requerido
def ventas_admin():
    if session.get('rango') != 1:  # Solo admin
        flash("❌ No tienes permisos para acceder a esta página.", "danger")
        return redirect('/home')

    # Obtener lista de cobradores (usuarios rango=4)
    conn = Conexion.get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT id, nombre, apellido 
        FROM usuarios 
        WHERE id_rango = 4 AND estado = 1
    """)
    cobradores = cursor.fetchall()
    cursor.close()
    conn.close()

    # 📌 Capturar filtros desde GET
    id_cobrador = request.args.get("id_cobrador")
    fecha_inicio = request.args.get("fecha_inicio")
    fecha_fin = request.args.get("fecha_fin")

    # 📌 Usar filtros si existen
    if id_cobrador or (fecha_inicio and fecha_fin):
        ventas = Conexion.obtener_ventas_filtradas(id_cobrador, fecha_inicio, fecha_fin)
    else:
        ventas = Conexion.obtener_todas_las_ventas()

    # 📌 POST = asignar cobrador
    if request.method == 'POST':
        id_factura = request.form['id_factura']
        id_cobrador_asignado = request.form['id_cobrador']
        Conexion.asignar_cobrador(id_factura, id_cobrador_asignado)
        flash("✅ Cobrador asignado correctamente.", "success")
        return redirect('/ventas_admin')

    return render_template(
        "ventas_admin.html",
        ventas=ventas,
        cobradores=cobradores
    )

##Cobros
@app.route('/cobros')
@Conexion.login_requerido
def cobros():
    """Página principal de cobros - muestra las ventas asignadas al cobrador logueado"""
    if session.get('rango') != 4:  # Solo cobradores
        flash("❌ Acceso denegado. Solo cobradores pueden acceder.", "danger")
        return redirect('/home')
    
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        # El usuario logueado ES el cobrador (estructura simplificada)
        id_cobrador = session['user_id']
        
        # Obtener ventas asignadas a este cobrador
        cursor.execute("""
            SELECT 
                fv.id_factura_venta,
                fv.fecha AS fecha_venta,
                fv.total,
                fv.cantidad,
                CASE WHEN fv.es_credito = 1 THEN 'Crédito' ELSE 'Contado' END AS tipo_pago,
                fv.precio_mensual,
                fv.estado_pago,
                COALESCE(fv.monto_abonado, 0) AS monto_abonado,
                (fv.total - COALESCE(fv.monto_abonado, 0)) AS saldo_pendiente,
                cli.nombre AS cliente_nombre,
                cli.apellido AS cliente_apellido,
                cli.telefono AS cliente_telefono,
                cli.direccion AS cliente_direccion,
                p.nombre AS producto_nombre,
                fv.cuotas
            FROM factura_venta fv
            JOIN usuarios cli ON fv.id_cliente = cli.id
            JOIN producto p ON fv.id_product = p.id_product
            WHERE fv.id_cobrador = %s
            ORDER BY fv.estado_pago ASC, fv.fecha DESC
        """, (id_cobrador,))
        
        ventas = cursor.fetchall()
        print(f"DEBUG - Ventas encontradas para cobrador {id_cobrador}: {len(ventas)}")
        
        # Si no hay ventas asignadas, mostrar mensaje informativo
        if not ventas:
            flash("ℹ️ No tienes ventas asignadas para cobro.", "info")
        
    except Exception as e:
        print(f"ERROR en cobros(): {str(e)}")
        flash(f"❌ Error al obtener ventas: {str(e)}", "danger")
        ventas = []
    finally:
        cursor.close()
        conn.close()
    
    return render_template("cobros.html", ventas=ventas)


@app.route('/detalle_cobro/<int:factura_id>')
@Conexion.login_requerido
def detalle_cobro(factura_id):
    """Muestra el detalle de una factura específica con historial de pagos"""
    if session.get('rango') != 4:
        flash("❌ Acceso denegado.", "danger")
        return redirect('/home')
    
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        id_cobrador = session['user_id']
        
        # Verificar que esta factura pertenezca al cobrador logueado
        cursor.execute("""
            SELECT COUNT(*) AS cnt
            FROM factura_venta fv
            WHERE fv.id_factura_venta = %s AND fv.id_cobrador = %s
        """, (factura_id, id_cobrador))
        
        if cursor.fetchone()["cnt"] == 0:
            flash("❌ No tienes acceso a esta factura.", "danger")
            return redirect('/cobros')
        
        # Obtener información completa de la factura
        cursor.execute("""
            SELECT 
                fv.id_factura_venta,
                fv.fecha AS fecha_venta,
                fv.total,
                fv.cuotas,
                fv.precio_mensual,
                fv.estado_pago,
                fv.es_credito,
                fv.interes_aplicado,
                fv.cantidad,
                COALESCE(fv.monto_abonado, 0) AS monto_abonado,
                (fv.total - COALESCE(fv.monto_abonado, 0)) AS saldo_pendiente,
                cli.id AS cliente_id,
                cli.nombre AS cliente_nombre,
                cli.apellido AS cliente_apellido,
                cli.telefono AS cliente_telefono,
                cli.direccion AS cliente_direccion,
                cli.DUI AS cliente_dui,
                p.nombre AS producto_nombre,
                p.descripcion AS producto_descripcion,
                p.precio AS precio_producto
            FROM factura_venta fv
            JOIN usuarios cli ON fv.id_cliente = cli.id
            JOIN producto p ON fv.id_product = p.id_product
            WHERE fv.id_factura_venta = %s
        """, (factura_id,))
        
        factura = cursor.fetchone()
        
        if not factura:
            flash("❌ Factura no encontrada.", "danger")
            return redirect('/cobros')
        
        # ✅ Convertir a float lo que venga como Decimal
        for campo in ["total", "precio_mensual", "monto_abonado", "saldo_pendiente"]:
            if isinstance(factura[campo], Decimal):
                factura[campo] = float(factura[campo])

        # Obtener historial de abonos
        cursor.execute("""
            SELECT 
                av.id_abono,
                av.monto_abonado,
                av.fecha,
                av.mes_correspondiente,
                av.año_correspondiente,
                av.saldo_pendiente,
                av.observaciones,
                u.nombre as usuario_registro
            FROM abono_venta av
            LEFT JOIN usuarios u ON av.id_usuario = u.id
            WHERE av.id_factura_venta = %s
            ORDER BY av.año_correspondiente DESC, av.mes_correspondiente DESC, av.fecha DESC
        """, (factura_id,))
        
        historial_abonos = cursor.fetchall()
        
        # Convertir historial a formato esperado por generar_tabla_meses
        historial_tuplas = []
        for abono in historial_abonos:
            historial_tuplas.append((
                abono['id_abono'],
                float(abono['monto_abonado']),  # ✅ convertir
                abono['fecha'],
                abono['mes_correspondiente'],
                abono['año_correspondiente'],
                float(abono['saldo_pendiente']),  # ✅ convertir
                abono['observaciones'] or ''
            ))
        
        # Generar tabla de meses
        fecha_inicio = factura["fecha_venta"]
        cuotas_reales = factura["cuotas"]

        meses_pago = generar_tabla_meses(
            fecha_inicio, 
            cuotas_reales, 
            factura["precio_mensual"],  # ya es float
            historial_tuplas
        )
        
    except Exception as e:
        print(f"ERROR en detalle_cobro(): {str(e)}")
        flash(f"❌ Error al obtener detalles: {str(e)}", "danger")
        return redirect('/cobros')
    finally:
        cursor.close()
        conn.close()
    
    return render_template(
        "detalle_cobro.html", 
        factura=factura, 
        historial=historial_abonos,
        meses_pago=meses_pago
    )



@app.route('/registrar_abono/<int:factura_id>', methods=['GET', 'POST'])
@Conexion.login_requerido
def registrar_abono(factura_id):
    """Registra un nuevo abono a una factura"""
    if session.get('rango') != 4:
        flash("❌ Acceso denegado.", "danger")
        return redirect('/home')
    
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        try:
            monto_abono = float(request.form['monto_abono'])
            mes_correspondiente = int(request.form['mes_correspondiente'])
            año_correspondiente = int(request.form['año_correspondiente'])
            observaciones = request.form.get('observaciones', '').strip()
            
            if monto_abono <= 0:
                flash("❌ El monto debe ser mayor a cero.", "danger")
                return redirect(url_for('detalle_cobro', factura_id=factura_id))
            
            # Verificar que la factura existe y pertenece al cobrador
            cursor.execute("""
                SELECT fv.*, (fv.total - COALESCE(fv.monto_abonado, 0)) as saldo_actual
                FROM factura_venta fv
                WHERE fv.id_factura_venta = %s AND fv.id_cobrador = %s
            """, (factura_id, session['user_id']))
            
            factura = cursor.fetchone()
            if not factura:
                flash("❌ Factura no encontrada o no autorizada.", "danger")
                return redirect('/cobros')
            
            saldo_actual = float(factura['saldo_actual'])
            precio_mensual = float(factura['precio_mensual'])
            
            if monto_abono > saldo_actual:
                flash(f"❌ El abono no puede ser mayor al saldo pendiente (${saldo_actual:.2f}).", "danger")
                return redirect(url_for('detalle_cobro', factura_id=factura_id))
            
            # VALIDAR: Verificar cuánto se ha abonado ya en este mes
            cursor.execute("""
                SELECT COALESCE(SUM(monto_abonado), 0) as total_mes
                FROM abono_venta 
                WHERE id_factura_venta = %s 
                AND mes_correspondiente = %s 
                AND año_correspondiente = %s
            """, (factura_id, mes_correspondiente, año_correspondiente))
            
            resultado_mes = cursor.fetchone()
            total_abonado_mes = float(resultado_mes['total_mes'])
            disponible_mes = precio_mensual - total_abonado_mes
            
            if disponible_mes <= 0:
                flash(f"❌ El mes {mes_correspondiente}/{año_correspondiente} ya está completamente pagado.", "warning")
                return redirect(url_for('detalle_cobro', factura_id=factura_id))
            
            if monto_abono > disponible_mes:
                flash(f"❌ Solo puedes abonar ${disponible_mes:.2f} más para el mes {mes_correspondiente}/{año_correspondiente}. Ya se han abonado ${total_abonado_mes:.2f} de ${precio_mensual:.2f}.", "warning")
                return redirect(url_for('detalle_cobro', factura_id=factura_id))
            
            # Calcular nuevo saldo
            nuevo_saldo = saldo_actual - monto_abono
            nuevo_monto_abonado = float(factura['monto_abonado'] or 0) + monto_abono
            
            # Determinar nuevo estado
            if nuevo_saldo <= 0.01:  # Considerar pagado si queda menos de 1 centavo
                nuevo_estado = 'pagado'
                nuevo_saldo = 0
            elif nuevo_monto_abonado > 0:
                nuevo_estado = 'parcial'
            else:
                nuevo_estado = 'pendiente'
            
            # Registrar el abono
            fecha_abono = datetime.today().strftime('%Y-%m-%d')
            cursor.execute("""
                INSERT INTO abono_venta 
                (id_factura_venta, id_usuario, monto_abonado, mes_correspondiente, 
                 año_correspondiente, saldo_pendiente, observaciones, fecha)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                factura_id, session['user_id'], monto_abono, mes_correspondiente,
                año_correspondiente, nuevo_saldo, observaciones, fecha_abono
            ))
            
            # Actualizar la factura
            cursor.execute("""
                UPDATE factura_venta 
                SET monto_abonado = %s, estado_pago = %s
                WHERE id_factura_venta = %s
            """, (nuevo_monto_abonado, nuevo_estado, factura_id))
            
            conn.commit()
            flash(f"✅ Abono de ${monto_abono:.2f} registrado correctamente.", "success")
            
        except ValueError:
            flash("❌ Valores numéricos inválidos.", "danger")
        except Exception as e:
            conn.rollback()
            flash(f"❌ Error al registrar abono: {str(e)}", "danger")
            print(f"Error en registrar_abono: {e}")
        finally:
            cursor.close()
            conn.close()
        
        return redirect(url_for('detalle_cobro', factura_id=factura_id))
    
    # GET - Mostrar formulario
    try:
        cursor.execute("""
            SELECT fv.*, (fv.total - COALESCE(fv.monto_abonado, 0)) as saldo_pendiente,
                   cli.nombre as cliente_nombre, cli.apellido as cliente_apellido,
                   p.nombre as producto_nombre
            FROM factura_venta fv
            JOIN usuarios cli ON fv.id_cliente = cli.id
            JOIN producto p ON fv.id_product = p.id_product
            WHERE fv.id_factura_venta = %s AND fv.id_cobrador = %s
        """, (factura_id, session['user_id']))
        
        factura = cursor.fetchone()
        if not factura:
            flash("❌ Factura no encontrada.", "danger")
            return redirect('/cobros')
        
    except Exception as e:
        flash(f"❌ Error: {str(e)}", "danger")
        return redirect('/cobros')
    finally:
        cursor.close()
        conn.close()
    
    return render_template("registrar_abono.html", factura=factura)



@app.route('/debug_cobros')
@Conexion.login_requerido  
def debug_cobros():
    """Debug para verificar datos del sistema de cobros"""
    conn = get_connection()
    cursor = conn.cursor()
    
    resultado = []
    resultado.append("=== DEBUG SISTEMA DE COBROS ===")
    resultado.append("")
    
    # Información de sesión
    resultado.append(f"Session user_id: {session.get('user_id')}")
    resultado.append(f"Session rango: {session.get('rango')}")
    resultado.append(f"Session nombre: {session.get('nombre')} {session.get('apellido')}")
    resultado.append("")
    
    # Verificar usuario en tabla usuarios
    cursor.execute("SELECT * FROM usuarios WHERE id = %s", (session.get('user_id'),))
    usuario = cursor.fetchone()
    resultado.append(f"Usuario en BD: {usuario}")
    resultado.append("")
    
    # Verificar cobrador correspondiente usando la lógica mejorada
    cursor.execute("""
        SELECT cb.id_cobrador, cb.nombre, cb.apellido, cb.tel, cb.id_zona
        FROM cobrador cb
        JOIN usuarios u ON TRIM(LOWER(cb.nombre)) = TRIM(LOWER(u.nombre))
        AND COALESCE(TRIM(LOWER(cb.apellido)), '') = COALESCE(TRIM(LOWER(u.apellido)), '')
        WHERE u.id = %s AND u.id_rango = 4
    """, (session.get('user_id'),))
    cobrador = cursor.fetchone()
    
    if cobrador:
        resultado.append(f"✓ Cobrador encontrado: ID={cobrador[0]}, Nombre={cobrador[1]} {cobrador[2]}")
        cobrador_id = cobrador[0]
        
        # Verificar ventas asignadas
        cursor.execute("""
            SELECT fv.id_factura_venta, fv.id_cobrador, fv.es_credito, fv.total, 
                fv.estado_pago, c.nombre as cliente
            FROM factura_venta fv 
            JOIN cliente c ON fv.id_cliente = c.id_cliente
            WHERE fv.id_cobrador = %s
        """, (cobrador_id,))
        ventas_cobrador = cursor.fetchall()
        
        resultado.append(f"Ventas asignadas al cobrador: {len(ventas_cobrador)}")
        for venta in ventas_cobrador:
            resultado.append(f"  - Factura #{venta[0]}, Crédito: {venta[2]}, Total: ${venta[3]}, Cliente: {venta[5]}")
            
        # Verificar ventas a crédito específicamente
        cursor.execute("""
            SELECT COUNT(*) as total
            FROM factura_venta 
            WHERE id_cobrador = %s AND es_credito = 1
        """, (cobrador_id,))
        ventas_credito = cursor.fetchone()[0]
        resultado.append(f"Ventas a crédito: {ventas_credito}")
        
    else:
        resultado.append("✗ NO se encontró cobrador asociado al usuario")
        
        # Mostrar comparación detallada
        cursor.execute("SELECT nombre, apellido FROM usuarios WHERE id = %s", (session.get('user_id'),))
        usuario_data = cursor.fetchone()
        cursor.execute("SELECT nombre, apellido FROM cobrador")
        cobradores_data = cursor.fetchall()
        
        resultado.append(f"Usuario buscado: nombre='{usuario_data[0]}', apellido='{usuario_data[1]}'")
        resultado.append("Cobradores disponibles:")
        for cb in cobradores_data:
            resultado.append(f"  - nombre='{cb[0]}', apellido='{cb[1]}'")
            
        resultado.append("")
        resultado.append("SOLUCION SUGERIDA:")
        resultado.append(f"UPDATE usuarios SET apellido = 'CASTILLO' WHERE id = {session.get('user_id')};")
    cursor.close()
    conn.close()
    return f"<pre>{'<br>'.join(resultado)}</pre>"

@app.route('/mis_compras')
@Conexion.login_requerido
def mis_compras():
    """Panel principal del cliente - vista general de sus compras"""
    if session.get('rango') != 2:  # Solo clientes
        flash("Acceso denegado. Solo clientes pueden acceder.", "danger")
        return redirect('/home')
    
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Obtener todas las compras del cliente
        cursor.execute("""
            SELECT 
                fv.id_factura_venta,
                fv.fecha AS fecha_compra,
                fv.total,
                fv.es_credito,
                fv.estado_pago,
                fv.cuotas,
                fv.precio_mensual,
                fv.cantidad
                COALESCE(fv.monto_abonado, 0) AS monto_abonado,
                (fv.total - COALESCE(fv.monto_abonado, 0)) AS saldo_pendiente,
                p.nombre AS producto_nombre,
                p.descripcion AS producto_descripcion,
                p.precio AS precio_original,
                ven.nombre AS vendedor_nombre,
                ven.apellido AS vendedor_apellido
            FROM factura_venta fv
            JOIN producto p ON fv.id_product = p.id_product
            JOIN usuarios ven ON fv.id_vendedor = ven.id
            WHERE fv.id_cliente = %s
            ORDER BY fv.fecha DESC, fv.id_factura_venta DESC
        """, (session['user_id'],))
        
        compras = cursor.fetchall()
        
        # Calcular estadísticas
        total_compras = len(compras)
        compras_pagadas = len([c for c in compras if c['estado_pago'] == 'pagado'])
        compras_pendientes = len([c for c in compras if c['estado_pago'] in ['pendiente', 'parcial']])
        total_gastado = sum(float(c['total']) for c in compras)
        total_pendiente = sum(float(c['saldo_pendiente']) for c in compras if c['estado_pago'] != 'pagado')
        
        estadisticas = {
            'total_compras': total_compras,
            'compras_pagadas': compras_pagadas,
            'compras_pendientes': compras_pendientes,
            'total_gastado': total_gastado,
            'total_pendiente': total_pendiente
        }
        
    except Exception as e:
        print(f"ERROR en mis_compras(): {str(e)}")
        flash(f"Error al obtener tus compras: {str(e)}", "danger")
        compras = []
        estadisticas = {}
    finally:
        cursor.close()
        conn.close()
    
    return render_template("mis_compras.html", compras=compras, estadisticas=estadisticas)


@app.route('/detalle_compra/<int:factura_id>')
@Conexion.login_requerido
def detalle_compra(factura_id):
    """Detalle específico de una compra del cliente"""
    if session.get('rango') != 2:
        flash("Acceso denegado.", "danger")
        return redirect('/home')
    
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Verificar que la compra pertenece al cliente logueado
        cursor.execute("""
            SELECT 
                fv.id_factura_venta,
                fv.fecha AS fecha_compra,
                fv.hora,
                fv.total,
                fv.es_credito,
                fv.estado_pago,
                fv.cuotas,
                fv.precio_mensual,
                fv.interes_aplicado,
                fv.cantidad,
                fv.direccion,
                CAST(COALESCE(fv.monto_abonado, 0) AS DECIMAL(10,2)) AS monto_abonado,
                CAST((fv.total - COALESCE(fv.monto_abonado, 0)) AS DECIMAL(10,2)) AS saldo_pendiente,
                p.nombre AS producto_nombre,
                p.descripcion AS producto_descripcion,
                p.precio AS precio_original,
                ven.nombre AS vendedor_nombre,
                ven.apellido AS vendedor_apellido,
                cob.nombre AS cobrador_nombre,
                cob.apellido AS cobrador_apellido,
                cob.telefono AS cobrador_telefono
            FROM factura_venta fv
            JOIN producto p ON fv.id_product = p.id_product
            JOIN usuarios ven ON fv.id_vendedor = ven.id
            LEFT JOIN usuarios cob ON fv.id_cobrador = cob.id
            WHERE fv.id_factura_venta = %s AND fv.id_cliente = %s
        """, (factura_id, session['user_id']))
        
        compra = cursor.fetchone()
        
        if not compra:
            flash("Compra no encontrada.", "danger")
            return redirect('/mis_compras')
        
        # Obtener historial de abonos
        cursor.execute("""
            SELECT 
                av.id_abono,
                av.monto_abonado,
                av.fecha,
                av.mes_correspondiente,
                av.año_correspondiente,
                av.saldo_pendiente,
                av.observaciones,
                u.nombre as cobrador_registro,
                u.apellido as cobrador_apellido_registro
            FROM abono_venta av
            LEFT JOIN usuarios u ON av.id_usuario = u.id
            WHERE av.id_factura_venta = %s
            ORDER BY av.año_correspondiente DESC, av.mes_correspondiente DESC, av.fecha DESC
        """, (factura_id,))
        
        historial_abonos = cursor.fetchall()
        
        # Solo generar tabla de meses si es a crédito
        meses_pago = []
        if compra['es_credito']:
            # Convertir historial a formato para generar_tabla_meses
            historial_tuplas = []
            for abono in historial_abonos:
                historial_tuplas.append((
                    abono['id_abono'],
                    float(abono['monto_abonado']), 
                    abono['fecha'],
                    abono['mes_correspondiente'],
                    abono['año_correspondiente'],
                    float(abono['saldo_pendiente']),
                    abono['observaciones'] or ''
                ))
            
            meses_pago = generar_tabla_meses(
                compra["fecha_compra"], 
                compra["cuotas"], 
                float(compra["precio_mensual"]), 
                historial_tuplas
            )
        
    except Exception as e:
        print(f"ERROR en detalle_compra(): {str(e)}")
        flash(f"Error al obtener detalles: {str(e)}", "danger")
        return redirect('/mis_compras')
    finally:
        cursor.close()
        conn.close()
    
    return render_template(
        "detalle_compra.html", 
        compra=compra, 
        historial=historial_abonos,
        meses_pago=meses_pago
    )


@app.route('/verificar_mes_abono', methods=['POST'])
@Conexion.login_requerido
def verificar_mes_abono():
    """API endpoint para verificar cuánto se puede abonar en un mes específico"""
    if session.get('rango') not in [2, 4]:  # Clientes y cobradores
        return {'error': 'No autorizado'}, 403
    
    data = request.get_json()
    factura_id = data.get('factura_id')
    mes = data.get('mes')
    año = data.get('año')
    
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Verificar permisos según el rol
        if session.get('rango') == 2:  # Cliente
            cursor.execute("""
                SELECT precio_mensual 
                FROM factura_venta 
                WHERE id_factura_venta = %s AND id_cliente = %s
            """, (factura_id, session['user_id']))
        else:  # Cobrador
            cursor.execute("""
                SELECT precio_mensual 
                FROM factura_venta 
                WHERE id_factura_venta = %s AND id_cobrador = %s
            """, (factura_id, session['user_id']))
        
        factura = cursor.fetchone()
        if not factura:
            return {'error': 'Factura no encontrada'}, 404
        
        precio_mensual = float(factura['precio_mensual'])
        
        # Calcular lo ya abonado en este mes
        cursor.execute("""
            SELECT COALESCE(SUM(monto_abonado), 0) as total_abonado
            FROM abono_venta 
            WHERE id_factura_venta = %s 
            AND mes_correspondiente = %s 
            AND año_correspondiente = %s
        """, (factura_id, mes, año))
        
        resultado = cursor.fetchone()
        total_abonado = float(resultado['total_abonado'])
        disponible = precio_mensual - total_abonado
        
        return {
            'precio_mensual': precio_mensual,
            'total_abonado': total_abonado,
            'disponible': max(0, disponible)
        }
        
    except Exception as e:
        return {'error': str(e)}, 500
    finally:
        cursor.close()
        conn.close()







# ------------------------
# Run
# ------------------------
if __name__ == "__main__":
    print("Flask está listo para correr")
    app.run(debug=True)