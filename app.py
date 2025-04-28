from flask import Flask, render_template, redirect,request, session
from Funciones import Conexion

app = Flask(__name__)
app.secret_key = 'Quemen el ina'  # Necesario para usar sesiones

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
    rango = request.form.get('rango')
    return Conexion.register(nombre, correo, contraseña, rango)

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






if __name__ == "__main__":
    app.run(debug=True)