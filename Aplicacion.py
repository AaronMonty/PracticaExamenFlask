from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'clave_secreta'

# Configuración de la base de datos
db = mysql.connector.connect(
    host="localhost",
    user="aaron",
    password="1234",
    database="mydatabase"
)

cursor = db.cursor()

# Rutas públicas
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about_me')
def about_me():
    return render_template('about_me.html')

# Rutas privadas
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Verificar las credenciales en la base de datos
        query = "SELECT * FROM alumnos WHERE nombre = %s AND contraseña = %s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()

        if user:
            session['user_id'] = user[0]  # Almacenar la id del usuario en la sesión
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

# Otras funcionalidades, como el segundo formulario

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True)
