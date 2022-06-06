from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from datetime import datetime
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.secret_key = 'my_secret_key'
mensaje_error= 0

app.config['MYSQL_HOST'] = 'localhost' 
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'J08042005'
app.config['MYSQL_DB'] = 'cuentas' 
mysql = MySQL(app)


@app.route("/")
def info():
    return render_template('Index.html')

@app.route("/login")
def login ():
    global mensaje_error
    return render_template("login.html", mensaje_error = mensaje_error)

@app.route("/login/chofer")
def loginChofer ():
    global mensaje_error
    return render_template("loginChofer.html", mensaje_error = mensaje_error)

@app.route("/register")
def register ():
    global mensaje_error
    return render_template("register.html",mensaje_error = mensaje_error)

@app.route ("/register2")
def register2 ():
    global mensaje_error
    return render_template ("register2.html", mensaje_error = mensaje_error)

@app.route ("/usu", methods= ['POST'])
def loginUsu ():
    global mensaje_error
    try:
        aux = request.form['id'] 
    except:
        aux = 0

    correo = request.form['email']
    contra = request.form['password']
    cur = mysql.connection.cursor()

    try:
        destino = request.form['destino']
        partida= request.form['partida']
        cur.execute('INSERT INTO viajes (partida, destino) VALUES (%s,%s)', (partida, destino ))
        mysql.connection.commit()

    except:
        destino = ''
        partida = ''
    
    try:
        cur.execute("SELECT * FROM viajes")
        viajes = cur.fetchall()
        partida2 = request.form['partida']
        destino2 = request.form ['destino']
        for i in viajes:
            if (i[1] == partida2 and i[2] == destino2):
                iden = i[0]
                print("los dos son iguales")
    except:
        iden = 0

    try:
        auxiliar = request.form['iden']
        sentencia = " DELETE FROM viajes WHERE id LIKE ('{0}')".format(auxiliar)
        cur.execute (sentencia)
        mysql.connection.commit()

    except:
        pass
    
    cur.execute('SELECT * FROM Usuario')
    Usuario = cur.fetchall()
    for x in Usuario:
        if correo == x[3] and contra == x[4]:
            return render_template ("usu.html", nombre = x[1], correo = correo, contra = contra, aux = int(aux), destino = destino, partida= partida, iden = iden)
    
    flash ('El correo o contraseña no coincide, por favor verifique')
    mensaje_error = 1
    return redirect(url_for('login'))

@app.route ("/chofer",methods= ['POST'])
def lgChofer():
    global mensaje_error

    correo = request.form['email']
    contra = request.form['password']
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM Chofer')
    Usuario = cur.fetchall()
    for x in Usuario:
        if correo == x[4] and contra == x[5]:
            cur.execute('SELECT * FROM viajes')
            viajes = cur.fetchall()
            return render_template ("chofer.html", nombre = x[2], contra = contra, correo = correo, viajes = viajes)
    
    flash ('El correo o contraseña no coincide, por favor verifique')
    mensaje_error = 1
    return redirect(url_for('loginChofer'))


@app.route("/add_person", methods=['POST'])
def add_person ():
    global mensaje_error
    #Datos del registro de usuarios
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    email = request.form['email']
    contrasenia = request.form['contraseña']
    telefono = request.form['phoneNumber']


    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM Usuario')
    Usuario = cur.fetchall()
    print(Usuario)
    for x in Usuario:
        if email == x[3]:
            flash('Ya hay una cuenta con ese correo. Por favor use otro')
            mensaje_error = 1
            return redirect(url_for("register"))

    cur.execute("INSERT INTO Usuario (nombre, apellido, email, password, telefono) VALUES (%s,%s,%s,%s,%s)", (nombre, apellido, email, contrasenia, telefono))
    mysql.connection.commit()

    success_message = 'Sr(a). {} se ha registrado exitosamente.'.format(nombre)
    flash(success_message)
    mensaje_error=0
    return redirect(url_for("register"))

@app.route("/add_chofer", methods=['POST'])
def add_chofer ():
    global mensaje_error
    #datos el registro de chofer
    auto = request.form['flexRadioDefault']
    if(auto == "true"):
        auto = "Tiene"
    else:
        auto="No Tiene"
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    email = request.form['email']

    cur = mysql.connection.cursor()
    cur.execute('SELECT *  FROM Chofer')
    Chofer  = cur.fetchall() 
    for x in Chofer:
        if email == x[4]:
            flash('Ya hay una cuenta con ese correo. Por favor use otro')
            mensaje_error = 1
            return redirect(url_for("register2"))

    contrasenia = request.form['Contraseña']
    tel = request.form['phoneNumber']
    nacimiento = request.form['birthday']
    genero = request.form['gen']
    
    
    cur.execute("INSERT INTO Chofer (auto, nombre, apellido, email, password, telefono, nacimiento, genero) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)", (auto, nombre, apellido, email, contrasenia, tel, nacimiento, genero))
    mysql.connection.commit()

    if genero == "Hombre": 
        success_message = 'Sr. {} se ha registrado exitosamente.'.format(nombre)
    elif genero == "Mujer":
        success_message = 'Sra. {} se ha registrado exitosamente.'.format(nombre)
    else:
        success_message = '{} se ha registrado exitosamente.'.format(nombre)
    flash(success_message)
    mensaje_error=0
    return redirect(url_for("register2"))

@app.route("/usu/pedido", methods =['POST'])
def pedir ():
    return redirect(url_for('loginUsu'))

@app.route("/Information")
def Information ():
    return render_template("Information.html")

@app.route("/Information#<name>")
def Information2 ():
    return render_template("Information.html")

if __name__ == '__main__':
    app.run(debug=True)