
from flask import Flask, render_template, redirect, request, session, url_for, flash, send_file
from Funciones import Conexion
from datetime import datetime
import mysql.connector
from functools import wraps
import io


app = Flask(__name__)
app.secret_key = 'Quemen el ina'

def get_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='Gestor3'
    )

def admin_required(f):
    @wraps(f)
    def decorada(*args, **kwargs):
        if 'rango' not in session or session['rango'] != 1:
            flash("❌ Acceso denegado. Solo administradores pueden acceder a esta página.")
            return redirect('/home')
        return f(*args, **kwargs)
    return decorada

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
        precio_producto = cursor.fetchone()[0]
        
        # Configurar valores según tipo de pago
        if tipo_pago == 'contado':
            es_credito = 0
            cuotas = 1
            interes_aplicado = 0.00
            total = precio_producto
            precio_mensual = precio_producto
        else:  # crédito
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
            
            interes_aplicado = interes_result[0]
            total = precio_producto * (1 + interes_aplicado / 100)
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
            
        except Exception as e:
            conn.rollback()
            flash(f"❌ Error al registrar la venta: {str(e)}", "danger")
        
        cursor.close()
        conn.close()
        return redirect(url_for('registrar_venta'))

    # GET request - mostrar formulario
    cursor.execute("SELECT id_cliente, nombre FROM cliente")
    clientes = cursor.fetchall()

    cursor.execute("SELECT id_product, nombre, precio FROM producto")
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


# ------------------------
# Cobros 
# ------------------------
@app.route('/gestionar_cobros', methods=['GET'])
@Conexion.login_requerido
def gestionar_cobros():
    id_cobrador = session['user_id']
    clientes = Conexion.obtener_clientes_de_cobrador(id_cobrador)

    datos_cobros = []
    for cliente in clientes:
        pagos = Conexion.obtener_pagos_cliente(cliente['id'])
        total_pagado = sum(p['monto'] for p in pagos)
        productos = Conexion.obtener_productos_cliente(cliente['id'])
        total_deuda = sum(p['precio'] for p in productos)

        datos_cobros.append({
            'cliente': cliente,
            'productos': productos,
            'total_deuda': total_deuda,
            'total_pagado': total_pagado,
            'restante': total_deuda - total_pagado
        })

    mostrar_productos = any(len(c['productos']) > 0 for c in datos_cobros)

    return render_template(
        'gestionar_cobros.html',
        cobros=datos_cobros,
        mostrar_productos=mostrar_productos
    )


@app.route('/abonar', methods=['POST'])
@Conexion.login_requerido
def abonar():
    id_cliente = request.form['id_cliente']
    monto = float(request.form['monto'])
    id_cobrador = session['user_id']
    Conexion.registrar_abono(id_cliente, id_cobrador, monto)
    flash("✅ Abono registrado correctamente.")
    return redirect('/gestionar_cobros')


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

# ------------------------
# Run
# ------------------------
if __name__ == "__main__":
    print("Flask está listo para correr")
    app.run(debug=True)