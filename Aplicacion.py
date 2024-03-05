from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'clave_secreta'

# Configuración de la base de datos
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="mydatabase"
)


# Rutas públicas
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the user already exists
        query = "SELECT * FROM alumnos WHERE nombre = %s"
        cursor = db.cursor()
        cursor.execute(query, (username,))
        user = cursor.fetchone()

        if user:
            cursor.close()
            return render_template('register.html', error='El usuario ya existe')
        else:
            # Insert user data into the database
            insert_query = "INSERT INTO alumnos (nombre, contraseña) VALUES (%s, %s)"
            cursor.execute(insert_query, (username, password))
            db.commit()
            cursor.close()

            return redirect(url_for('login'))

    return render_template('register.html')

# Rutas privadas
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Verificar las credenciales en la base de datos
        query = "SELECT * FROM alumnos WHERE nombre = %s AND contraseña = %s"
        cursor = db.cursor()  # Crear un nuevo cursor
        cursor.execute(query, (username, password))
        user = cursor.fetchone()

        if user:
            session['user_id'] = user[0]  # Almacenar la id del usuario en la sesión
            cursor.close()  # Cerrar el cursor después de la ejecución de la consulta
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Credenciales incorrectas')

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    # Comprobar si el usuario está autenticado antes de acceder al panel de control
    if 'user_id' in session:
        return render_template('dashboard.html')
    else:
        return redirect(url_for('login'))

# Ruta para el logout
@app.route('/logout')
def logout():
    # Eliminar la información del usuario de la sesión
    session.pop('user_id', None)
    return redirect(url_for('index'))

# Otras funcionalidades, como el segundo formulario

@app.route('/formulario', methods=['GET', 'POST'])
def formulario():
    if request.method == 'POST':
        # Obtener los datos del formulario
        equipo_favorito = request.form['equipo_favorito']
        jugador_favorito = request.form['jugador_favorito']

        # Puedes realizar acciones con los datos si es necesario

        # Redirigir a una página de agradecimiento o simplemente mostrar un mensaje
        return render_template('mensaje.html', equipo=equipo_favorito, jugador=jugador_favorito)

    # Si es una solicitud GET, simplemente renderiza el formulario
    return render_template('formulario.html')

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True)