from flask import Flask, render_template, redirect, request, session, url_for, flash, send_file
from Funciones import Conexion
from datetime import datetime
import mysql.connector
import io
from functools import wraps  # ← IMPORTANTE para corregir el decorador

app = Flask(__name__)
app.secret_key = 'Quemen el ina'  # Necesario para usar sesiones

def get_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='Gestor'
    )

# ✅ Decorador corregido
def admin_required(f):
    @wraps(f)  # ← Corrige el error de duplicidad
    def decorada(*args, **kwargs):
        if 'rango' not in session or session['rango'] != 1:
            flash("❌ Acceso denegado. Solo administradores pueden acceder a esta página.")
            return redirect('/home')
        return f(*args, **kwargs)
    return decorada

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
        id_rango = 2  # Cobrador por defecto
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


# Aquí está la ÚNICA función register_admin que debes mantener
@app.route('/register_admin', methods=['GET', 'POST'])
@Conexion.login_requerido
@admin_required
def register_admin():
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

        return Conexion.register(nombre, correo, contraseña, id_rango, datos_extra)

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id_rango, nombre FROM rango")
        rangos = cursor.fetchall()
    except Exception as e:
        rangos = []
        flash(f"❌ Error al obtener rangos: {str(e)}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()
    
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id_zona, nombre FROM zona")
        zonas = cursor.fetchall()
    except Exception as e:
        zonas = []
        flash(f"❌ Error al obtener rangos: {str(e)}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

    return render_template("register_admin.html", rangos=rangos, zonas=zonas)

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
    return redirect('/home') if 'user_id' in session else redirect('/login')

@app.route('/productos', methods=['GET', 'POST'])
@Conexion.login_requerido
@admin_required
def productos():
    categorias, productos = [], []
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = int(request.form['precio'])
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

@app.route('/registrar_venta', methods=['GET', 'POST'])
@Conexion.login_requerido
def registrar_venta():
    conn = get_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        id_cliente = request.form['cliente']
        id_producto = request.form['producto']
        id_categoria = request.form['categoria']
        monto = request.form['monto']
        id_vendedor = session['user_id']
        fecha = datetime.today().strftime('%Y-%m-%d')
        hora = datetime.today().strftime('%H:%M:%S')

        exito = Conexion.registrar_venta(id_cliente, id_vendedor, id_producto, id_categoria, monto, fecha, hora)
        flash("✅ Venta registrada correctamente." if exito else "❌ Error al registrar la venta.")
        return redirect(url_for('registrar_venta'))

    cursor.execute("SELECT id_cliente, nombre FROM cliente")
    clientes = cursor.fetchall()

    cursor.execute("SELECT id_product, nombre FROM producto")
    productos = cursor.fetchall()

    cursor.execute("SELECT id_categoria, nombre FROM categoria")
    categorias = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template("registrar_venta.html", clientes=clientes, productos=productos, categorias=categorias)

if __name__ == "__main__":
    app.run(debug=True)
