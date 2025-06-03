from flask import Flask, render_template, redirect,request, session
from Funciones import Conexion

from flask import url_for, flash, send_file
import mysql.connector
import io

app = Flask(__name__)
app.secret_key = 'Quemen el ina'  # Necesario para usar sesiones

def get_connection():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='Gestor'
    )
    return conn

@app.route("/About")
@Conexion.login_requerido
def pene():
    return render_template("About.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    correo = request.form.get('correo')
    contraseña = request.form.get('contraseña')
    return Conexion.login(correo, contraseña)

@app.route('/register', methods=['GET', 'POST'])
def register():
    nombre = request.form.get('nombre')
    correo = request.form.get('correo')
    contraseña = request.form.get('contraseña')
    id_rango = request.form.get('id_rango')
    return Conexion.register(nombre, correo, contraseña, id_rango)

@app.route('/logout')
@Conexion.login_requerido
def logout():
    Conexion.logout()
    session.pop('user_id', None)
    return redirect('/login')

@app.route('/home')
@Conexion.login_requerido
def home():
    nombre_usuario = session.get('nombre')  # Asegúrate de que 'nombre' esté guardado en la sesión
    return render_template('index.html', nombre_usuario=nombre_usuario)

@app.route('/')
@Conexion.login_requerido
def index():  # Corregido de inedx a index
    if 'user_id' in session:
        return redirect('/home')
    return redirect('/login')


@app.route('/productos', methods=['GET', 'POST'])
def productos():
    conn = None
    cursor = None
    categorias = []
    productos = []

    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = int(request.form['precio'])  # es INT en tu tabla
        stock = int(request.form['cantidad'])  # aquí lo llamas stock
        categoria = request.form['categoria']

        imagen_file = request.files['imagen']
        imagen_blob = imagen_file.read() if imagen_file and imagen_file.filename != '' else None

        try:
            conn = get_connection()
            cursor = conn.cursor()

            # Buscar el id_categoria desde el nombre recibido
            cursor.execute("SELECT id_categoria FROM categoria WHERE nombre = %s", (categoria,))
            result = cursor.fetchone()
            if not result:
                flash("❌ Categoría no válida")
                return redirect(url_for('productos'))
            id_catego = result[0]

            # Insertar producto, incluyendo imagen_blob en la columna nueva
            cursor.execute("""
                INSERT INTO producto (nombre, descripcion, precio, imagen, stock, id_catego, imagen_blob)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (nombre, descripcion, precio, 1 if imagen_blob else 0, stock, id_catego, imagen_blob))

            conn.commit()
            flash("✅ Producto creado exitosamente")
        except Exception as e:
            flash(f"❌ Error al insertar producto: {str(e)}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT nombre FROM categoria ORDER BY nombre")
        categorias = [row[0] for row in cursor.fetchall()]

        cursor.execute("""
            SELECT id_product, nombre, descripcion, precio, stock FROM producto WHERE 1
        """)
        productos = cursor.fetchall()

    except Exception as e:
        flash(f"❌ Error al obtener datos: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return render_template('productos_blob.html', productos=productos, categorias=categorias)


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
        # Imagen no disponible
        return '', 204  # No Content





if __name__ == "__main__":
    app.run(debug=True)