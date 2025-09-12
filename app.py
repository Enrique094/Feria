
from flask import Flask, render_template, redirect, request, session, url_for, flash, send_file
from Funciones import Conexion
from datetime import datetime
import mysql.connector
from functools import wraps
import io
import calendar

app = Flask(__name__)
app.secret_key = 'Quemen el ina'

def get_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='GestorPlus'
    )

def admin_required(f):
    @wraps(f)
    def decorada(*args, **kwargs):
        if 'rango' not in session or session['rango'] != 1:
            flash("❌ Acceso denegado. Solo administradores pueden acceder a esta página.")
            return redirect('/home')
        return f(*args, **kwargs)
    return decorada

def generar_tabla_meses(fecha_inicio, total_cuotas, precio_mensual, historial_abonos):
    """Genera una tabla de meses mostrando estado de pagos"""
    meses = []
    # Convertir fecha_inicio a datetime si es necesario
    if isinstance(fecha_inicio, str):
        fecha_actual = datetime.strptime(fecha_inicio, '%Y-%m-%d')
    else:
        fecha_actual = fecha_inicio
    
    # Para productos a contado, solo mostrar 1 mes
    if total_cuotas == 0:
        total_cuotas = 1
    
    # Crear diccionario de abonos por mes/año
    abonos_por_mes = {}
    for abono in historial_abonos:
        key = f"{abono[3]}-{abono[4]}"  # mes-año
        if key not in abonos_por_mes:
            abonos_por_mes[key] = []
        abonos_por_mes[key].append({
            'monto': abono[1],
            'fecha': abono[2],
            'observaciones': abono[6] if len(abono) > 6 else ''
        })
    
    # Determinar cuántos meses mostrar
    meses_a_mostrar = 1 if total_cuotas == 1 else min(12, int(total_cuotas))

    for i in range(meses_a_mostrar):
        # Calcular fecha del mes
        año = fecha_actual.year
        mes = fecha_actual.month + i
        
        # Ajustar año si el mes supera 12
        while mes > 12:
            mes -= 12
            año += 1
            
        mes_key = f"{mes}-{año}"
        
        estado = 'pendiente'
        abonos_mes = abonos_por_mes.get(mes_key, [])
        total_abonado_mes = sum(abono['monto'] for abono in abonos_mes)
        
        if total_abonado_mes >= float(precio_mensual):
            estado = 'pagado'
        elif total_abonado_mes > 0:
            estado = 'parcial'
        
        # Obtener nombre del mes
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


# ------------------------
# Rutas básicas
# ------------------------
@app.route("/About")
@Conexion.login_requerido
def about():
    return render_template("About.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    correo = request.form.get('correo')
    contraseña = request.form.get('contraseña')
    return Conexion.login(correo, contraseña)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        correo = request.form.get('correo')
        contraseña = request.form.get('contraseña')
        id_rango = 2  # por defecto cobrador
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
        id_rango = request.form.get('rango')
        datos_extra = {
            "cliente_apellido": request.form.get("cliente_apellido"),
            "cliente_tel": request.form.get("cliente_tel"),
            "cliente_dui": request.form.get("cliente_dui"),
            "cliente_direccion": request.form.get("cliente_direccion"),
            "vendedor_apellido": request.form.get("vendedor_apellido"),
            "vendedor_tel": request.form.get("vendedor_tel"),
            "vendedor_zona": request.form.get("vendedor_zona"),
            "cobrador_apellido": request.form.get("cobrador_apellido"),
            "cobrador_tel": request.form.get("cobrador_tel"),
            "cobrador_zona": request.form.get("cobrador_zona")
        }
        conn.close()
        return Conexion.register(nombre, correo, contraseña, id_rango, datos_extra)

    try:
        cursor.execute("SELECT * FROM usuarios")
        users = cursor.fetchall()

        cursor.execute("SELECT id_rango, nombre FROM rango")
        rangos = cursor.fetchall()

        cursor.execute("SELECT id_zona, nombre FROM zona")
        zonas = cursor.fetchall()
    except Exception as e:
        flash(f"❌ Error al obtener datos: {str(e)}", "danger")
        users, rangos, zonas = [], [], []
    finally:
        cursor.close()
        conn.close()

    return render_template("register_admin.html", users=users, rangos=rangos, zonas=zonas)

@app.route('/editar_usuario', methods=['GET', 'POST'])
@Conexion.login_requerido
@admin_required
def editar_usuario():
    user_id = request.form.get('user_id')
    nombre = request.form.get('nombre')
    correo = request.form.get('correo')
    estado = request.form.get('estado')
    id_rango = request.form.get('rango')

    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE usuarios 
            SET nombre=%s, correo=%s, estado=%s, id_rango=%s 
            WHERE id=%s
        """, (nombre, correo, estado, id_rango, user_id))
        conn.commit()
        flash("✅ Usuario actualizado", "success")
    except Exception as e:
        flash(f"❌ Error al actualizar: {str(e)}", "danger")
    finally:
        conn.close()
    return redirect('/register_admin')

@app.route('/eliminar_usuario/<int:user_id>', methods=['POST'])
@Conexion.login_requerido
@admin_required
def eliminar_usuario(user_id):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM usuarios WHERE id=%s", (user_id,))
        conn.commit()
        flash("🗑️ Usuario eliminado", "info")
    except Exception as e:
        flash(f"❌ Error al eliminar: {str(e)}", "danger")
    finally:
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
        tipo_pago = request.form['tipo_pago']  # 'contado' o 'credito'
        meses = request.form.get('meses', 0)  # Solo si es crédito
        
        # Obtener el id_vende asociado al usuario logueado
        cursor.execute("""
            SELECT id_vende FROM vendedor
            WHERE nombre = (SELECT nombre FROM usuarios WHERE id = %s)
            LIMIT 1
        """, (session['user_id'],))
        resultado = cursor.fetchone()

        if resultado is None:
            flash("❌ No se encontró un vendedor asociado al usuario actual.", "danger")
            cursor.close()
            conn.close()
            return redirect(url_for('registrar_venta'))

        id_vendedor = resultado[0]
        
        # Obtener precio del producto
        cursor.execute("SELECT precio FROM producto WHERE id_product = %s", (id_producto,))
        precio_result = cursor.fetchone()
        
        if precio_result is None:
            flash("❌ Producto no encontrado.", "danger")
            cursor.close()
            conn.close()
            return redirect(url_for('registrar_venta'))
            
        precio_producto = precio_result[0]
        
        # Configurar valores según tipo de pago
        if tipo_pago == 'contado':
            es_credito = 0
            cuotas = 1
            interes_aplicado = 0.00
            total = float(precio_producto)  # Convertir a float para cálculos
            precio_mensual = total
        else:  # crédito
            if not meses or meses == '0':
                flash("❌ Debe seleccionar un plazo para pago a crédito.", "danger")
                cursor.close()
                conn.close()
                return redirect(url_for('registrar_venta'))
                
            es_credito = 1
            cuotas = int(meses)
            
            # Obtener porcentaje de la tabla intereses según los meses
            cursor.execute("SELECT porcentaje FROM intereses WHERE meses = %s", (meses,))
            interes_result = cursor.fetchone()
            
            if interes_result is None:
                flash(f"❌ No se encontró configuración de interés para {meses} meses.", "danger")
                cursor.close()
                conn.close()
                return redirect(url_for('registrar_venta'))
            
            interes_aplicado = float(interes_result[0])
            total = float(precio_producto) * (1 + interes_aplicado / 100)
            precio_mensual = total / cuotas

        fecha = datetime.today().strftime('%Y-%m-%d')
        hora = datetime.today().strftime('%H:%M:%S')

        try:
            # Insertar la venta en la tabla factura_venta
            cursor.execute("""
                INSERT INTO factura_venta 
                (id_cliente, id_vende, id_product, interes_aplicado, es_credito, 
                 total, cuotas, precio_mensual, fecha, hora, direccion)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (id_cliente, id_vendedor, id_producto, interes_aplicado, es_credito, 
                  total, cuotas, precio_mensual, fecha, hora, direccion))
            
            conn.commit()
            flash("✅ Venta registrada exitosamente.", "success")
            
            # Opcional: Registrar detalles adicionales en log
            print(f"Venta registrada - Cliente: {id_cliente}, Producto: {id_producto}, Total: ${total:.2f}")
            
        except Exception as e:
            conn.rollback()
            flash(f"❌ Error al registrar la venta: {str(e)}", "danger")
            print(f"Error en registrar_venta: {e}")  # Para debugging
        
        cursor.close()
        conn.close()
        return redirect(url_for('registrar_venta'))

    # GET request - mostrar formulario
    try:
        cursor.execute("SELECT id_cliente, nombre FROM cliente")
        clientes = cursor.fetchall()

        cursor.execute("SELECT id_product, nombre, precio FROM producto WHERE stock > 0")  # Solo productos con stock
        productos = cursor.fetchall()
        
        # Obtener opciones de meses disponibles para crédito
        cursor.execute("SELECT meses, porcentaje FROM intereses ORDER BY meses")
        opciones_credito = cursor.fetchall()

        cursor.close()
        conn.close()

        return render_template("registrar_venta.html", 
                            clientes=clientes, 
                            productos=productos,
                            opciones_credito=opciones_credito)
    except Exception as e:
        cursor.close()
        conn.close()
        flash(f"❌ Error al cargar datos: {str(e)}", "danger")
        return redirect(url_for('dashboard'))  # o la página principal


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
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
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

    conn = Conexion.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id_cobrador, nombre, apellido FROM cobrador")
    cobradores = cursor.fetchall()
    cursor.close()
    conn.close()

    if request.method == 'POST':
        id_factura = request.form['id_factura']
        id_cobrador = request.form['id_cobrador']
        Conexion.asignar_cobrador(id_factura, id_cobrador)
        flash("Cobrador asignado correctamente.", "success")
        return redirect('/ventas_admin')

    ventas = Conexion.obtener_ventas()
    return render_template("ventas_admin.html", ventas=ventas, cobradores=cobradores)


# Cobrar

@app.route('/cobros')
@Conexion.login_requerido
def cobros():
    """Página principal de cobros - muestra las ventas asignadas al cobrador logueado"""
    if session.get('rango') != 4:  # Solo cobradores
        flash("Acceso denegado. Solo cobradores pueden acceder.", "danger")
        return redirect('/home')
    
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        # PASO 1: Obtener el id_cobrador real del usuario logueado
        # Usar TRIM y LOWER para comparación más robusta
        cursor.execute("""
            SELECT c.id_cobrador 
            FROM cobrador c
            JOIN usuarios u ON TRIM(LOWER(c.nombre)) = TRIM(LOWER(u.nombre))
            AND COALESCE(TRIM(LOWER(c.apellido)), '') = COALESCE(TRIM(LOWER(u.apellido)), '')
            WHERE u.id = %s AND u.id_rango = 4
            LIMIT 1
        """, (session['user_id'],))
        
        cobrador_result = cursor.fetchone()
        
        if not cobrador_result:
            # Debug detallado para identificar el problema
            cursor.execute("SELECT id, nombre, apellido FROM usuarios WHERE id = %s", (session['user_id'],))
            usuario_info = cursor.fetchone()
            
            cursor.execute("SELECT id_cobrador, nombre, apellido FROM cobrador")
            cobradores_info = cursor.fetchall()
            
            print(f"DEBUG - Usuario buscado: {usuario_info}")
            print(f"DEBUG - Cobradores disponibles: {cobradores_info}")
            
            flash("No se encontró cobrador asociado al usuario actual. Contacte al administrador.", "warning")
            return redirect('/home')
        
        id_cobrador_real = cobrador_result['id_cobrador']
        print(f"DEBUG - Cobrador encontrado: ID = {id_cobrador_real}")
        
        # PASO 2: Obtener ventas asignadas a ese cobrador
        cursor.execute("""
            SELECT 
                fv.id_factura_venta,
                fv.fecha AS fecha_venta,
                fv.total,
                CASE WHEN fv.Cuotas = 1 THEN 'Crédito' ELSE 'Contado' END AS tipo_pago,
                fv.Precio_Mensual AS precio_mensual,
                fv.estado_pago,
                COALESCE(fv.monto_abonado, 0) AS monto_abonado,
                (fv.total - COALESCE(fv.monto_abonado, 0)) AS saldo_pendiente,
                c.nombre AS cliente_nombre,
                c.apellido AS cliente_apellido,
                c.tel AS cliente_telefono,
                c.direccion AS cliente_direccion,
                p.nombre AS producto_nombre
            FROM factura_venta fv
            JOIN cliente c ON fv.id_cliente = c.id_cliente
            JOIN producto p ON fv.id_product = p.id_product
            WHERE fv.id_cobrador = %s AND fv.es_credito = 1
            ORDER BY fv.fecha DESC
        """, (id_cobrador_real,))
        
        ventas = cursor.fetchall()
        print(f"DEBUG - Ventas encontradas: {len(ventas)}")
        
    except Exception as e:
        print(f"ERROR en cobros(): {str(e)}")
        flash("Error al obtener ventas.", "danger")
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
        flash("Acceso denegado.", "danger")
        return redirect('/home')
    
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Obtener el id_cobrador real del usuario logueado
        cursor.execute("""
            SELECT c.id_cobrador 
            FROM cobrador c
            JOIN usuarios u ON TRIM(LOWER(c.nombre)) = TRIM(LOWER(u.nombre))
            AND COALESCE(TRIM(LOWER(c.apellido)), '') = COALESCE(TRIM(LOWER(u.apellido)), '')
            WHERE u.id = %s AND u.id_rango = 4
            LIMIT 1
        """, (session['user_id'],))
        
        cobrador_result = cursor.fetchone()
        if not cobrador_result:
            flash("No se encontró cobrador asociado.", "danger")
            return redirect('/home')
        
        id_cobrador_real = cobrador_result['id_cobrador']
        
        # Verificar que esta factura pertenezca al cobrador logueado
        cursor.execute("""
            SELECT COUNT(*) AS cnt
            FROM factura_venta fv
            WHERE fv.id_factura_venta = %s AND fv.id_cobrador = %s
        """, (factura_id, id_cobrador_real))
        
        if cursor.fetchone()["cnt"] == 0:
            flash("No tienes acceso a esta factura.", "danger")
            return redirect('/cobros')
        
        # Obtener información completa de la factura
        cursor.execute("""
            SELECT 
                fv.id_factura_venta,
                fv.fecha AS fecha_venta,
                fv.total,
                fv.Cuotas AS cuotas,
                fv.Precio_Mensual AS precio_mensual,
                fv.estado_pago,
                COALESCE(fv.monto_abonado, 0) AS monto_abonado,
                (fv.total - COALESCE(fv.monto_abonado, 0)) AS saldo_pendiente,
                c.id_cliente,
                c.nombre AS cliente_nombre,
                c.apellido AS cliente_apellido,
                c.tel AS cliente_telefono,
                c.direccion AS cliente_direccion,
                p.nombre AS producto_nombre,
                p.descripcion AS producto_descripcion
            FROM factura_venta fv
            JOIN cliente c ON fv.id_cliente = c.id_cliente
            JOIN producto p ON fv.id_product = p.id_product
            WHERE fv.id_factura_venta = %s
        """, (factura_id,))
        
        factura = cursor.fetchone()
        
        if not factura:
            flash("Factura no encontrada.", "danger")
            return redirect('/cobros')
        
        # Obtener historial de abonos
        cursor.execute("""
            SELECT 
                av.id_abono,
                av.monto_abonado,
                av.fecha,
                av.mes_correspondiente,
                av.año_correspondiente,
                av.saldo_pendiente,
                av.observaciones
            FROM abono_venta av
            WHERE av.id_factura_venta = %s
            ORDER BY av.año_correspondiente, av.mes_correspondiente
        """, (factura_id,))
        
        historial_abonos = cursor.fetchall()
        
        # Convertir historial a formato esperado por generar_tabla_meses
        historial_tuplas = []
        for abono in historial_abonos:
            historial_tuplas.append((
                abono['id_abono'],
                abono['monto_abonado'], 
                abono['fecha'],
                abono['mes_correspondiente'],
                abono['año_correspondiente'],
                abono['saldo_pendiente'],
                abono['observaciones']
            ))
        
        # Generar tabla de meses
        fecha_inicio = factura["fecha_venta"]
        # Para cuotas: si es crédito (bit=1) usar 12 meses, si contado (bit=0) usar 1
        cuotas_calculadas = 12 if factura["cuotas"] == 1 else 1
        meses_pago = generar_tabla_meses(
            fecha_inicio, 
            cuotas_calculadas, 
            float(factura["precio_mensual"]), 
            historial_tuplas
        )
        
    except Exception as e:
        print(f"ERROR en detalle_cobro(): {str(e)}")
        flash(f"Error al obtener detalles: {str(e)}", "danger")
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

@app.route('/registrar_abono', methods=['POST'])
@Conexion.login_requerido
def registrar_abono():
    """Registra un nuevo abono de pago"""
    if session.get('rango') != 4:
        flash("Acceso denegado.", "danger")
        return redirect('/home')
    
    factura_id = request.form['factura_id']
    monto_abono = float(request.form['monto_abono'])
    mes_correspondiente = int(request.form['mes_correspondiente'])
    año_correspondiente = int(request.form['año_correspondiente'])
    observaciones = request.form.get('observaciones', '')
    
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Obtener información actual de la factura
        cursor.execute("""
            SELECT total, COALESCE(monto_abonado, 0), id_cliente
            FROM factura_venta 
            WHERE id_factura_venta = %s
        """, (factura_id,))
        
        factura_info = cursor.fetchone()
        if not factura_info:
            flash("Factura no encontrada.", "danger")
            return redirect('/cobros')
        
        total_factura, monto_abonado_actual, id_cliente = factura_info
        nuevo_monto_abonado = monto_abonado_actual + monto_abono
        saldo_pendiente = total_factura - nuevo_monto_abonado
        
        # Obtener ID del cobrador real
        cursor.execute("""
            SELECT c.id_cobrador 
            FROM cobrador c
            JOIN usuarios u ON TRIM(LOWER(c.nombre)) = TRIM(LOWER(u.nombre))
            AND COALESCE(TRIM(LOWER(c.apellido)), '') = COALESCE(TRIM(LOWER(u.apellido)), '')
            WHERE u.id = %s AND u.id_rango = 4
            LIMIT 1
        """, (session['user_id'],))
        
        cobrador_result = cursor.fetchone()
        if not cobrador_result:
            flash("Cobrador no encontrado.", "danger")
            return redirect('/cobros')
        
        id_cobrador = cobrador_result[0]
        
        # Registrar el abono
        cursor.execute("""
            INSERT INTO abono_venta 
            (id_factura_venta, id_cliente, id_cobrador, monto_abonado, fecha, 
            mes_correspondiente, año_correspondiente, saldo_pendiente, observaciones)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (factura_id, id_cliente, id_cobrador, monto_abono, 
            datetime.today().strftime('%Y-%m-%d'),
            mes_correspondiente, año_correspondiente, saldo_pendiente, observaciones))
        
        # Actualizar la factura
        nuevo_estado = 'pagado' if saldo_pendiente <= 0 else 'parcial'
        cursor.execute("""
            UPDATE factura_venta 
            SET monto_abonado = %s, estado_pago = %s
            WHERE id_factura_venta = %s
        """, (nuevo_monto_abonado, nuevo_estado, factura_id))
        
        conn.commit()
        flash(f"Abono de ${monto_abono:.2f} registrado correctamente.", "success")
        
    except Exception as e:
        conn.rollback()
        flash(f"Error al registrar abono: {str(e)}", "danger")
        print(f"ERROR registrar_abono: {e}")
    finally:
        cursor.close()
        conn.close()
    
    return redirect(f'/detalle_cobro/{factura_id}')

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




# ------------------------
# Run
# ------------------------
if __name__ == "__main__":
    print("Flask está listo para correr")
    app.run(debug=True)