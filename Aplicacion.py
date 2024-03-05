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

<<<<<<< HEAD
=======
def register_user(username, password):
    query = "INSERT INTO alumnos (nombre, password) VALUES (%s, %s)"
    cursor = db.cursor()
    cursor.execute(query, (username, password))
    db.commit()
    cursor.close()
>>>>>>> e32049ce67efb83a7095064b20fa44dbfcc1771c

# Rutas públicas
@app.route('/')
def index():
    return render_template('index.html')

<<<<<<< HEAD
@app.route('/about')
def about():
    return render_template('ejercicios.html')
=======


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
<<<<<<< HEAD
            cursor.close()
            return render_template('register.html', error='El usuario ya existe')
        else:
            # Insert user data into the database
            insert_query = "INSERT INTO alumnos (nombre, contraseña) VALUES (%s, %s)"
            cursor.execute(insert_query, (username, password))
            db.commit()
            cursor.close()

=======
            return render_template('register.html', error='El usuario ya existe')
        else:
            register_user(username, password)
>>>>>>> e32049ce67efb83a7095064b20fa44dbfcc1771c
            return redirect(url_for('login'))

    return render_template('register.html')

# Rutas privadas
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Verificar las credenciales en la base de datos
<<<<<<< HEAD
        query = "SELECT * FROM alumnos WHERE nombre = %s AND contraseña = %s"
=======
        query = "SELECT * FROM alumnos WHERE nombre = %s AND password = %s"
>>>>>>> e32049ce67efb83a7095064b20fa44dbfcc1771c
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

@app.route('/ejercicio/<int:num>')
def ejercicio(num):
    exercises = [
        {"titulo": "Ejercicio 1", "descripcion": "Programa que calcula el año en que cumplirás 100 años.", "codigo": """nombre = input("Ingresa tu nombre: ")
edad = int(input("Ingresa tu edad: ")

año_actual = 2023  # Asumiendo que estamos en el año 2023
año_cumplir_100 = año_actual + (100 - edad)

print(f"¡Hola {nombre}! Cumplirás 100 años en el año {año_cumplir_100}.")""" },
        {"titulo": "Ejercicio 2", "descripcion": "Programa que verifica si un número es par o impar.", "codigo": """numero = int(input("Ingresa un número: "))

if numero % 2 == 0:
    print("El número es par.")
else:
    print("El número es impar.")""" },
        {"titulo": "Ejercicio 3", "descripcion": "Bucle que imprime los números mayores a 5 de una lista.", "codigo": """numeros = [2, 6, 8, 3, 1, 10, 7, 4, 9, 5]

for num in numeros:
    if num > 5:
        print(num)""" },
        {"titulo": "Ejercicio 4", "descripcion": "Bucle que imprime los números comunes entre dos listas.", "codigo": """lista1 = [1, 2, 3, 4, 5]
lista2 = [3, 4, 5, 6, 7, 8]

for num in lista1:
    if num in lista2:
        print(num)""" },
        {"titulo": "Ejercicio 5", "descripcion": "Calcula las edades a partir de años de nacimiento.", "codigo": """años_nacimiento = [1990, 1985, 2000, 1998, 2005]

año_actual = 2023  # Asumiendo que estamos en el año 2023
edades = [año_actual - año for año in años_nacimiento]

print("Edades de los alumnos:")
print(edades)""" },
        {"titulo": "Ejercicio 6", "descripcion": "Verifica si un texto es un palíndromo.", "codigo": """texto = input("Ingresa un texto: ")

texto = texto.lower() 
texto_sin_espacios = texto.replace(" ", "")  

if texto_sin_espacios == texto_sin_espacios[::-1]:
    print("El texto es un palíndromo.")
else:
    print("El texto no es un palíndromo.")""" },
    ]

    if 1 <= num <= len(exercises):
        exercise = exercises[num - 1]
        return render_template('ejercicio.html', exercise=exercise, num=num)
    else:
        return "Ejercicio no encontrado"

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True)