from flask import Flask, flash, render_template, request, redirect, url_for, session, Response, make_response
from flask_mysqldb import MySQL
from flask_session import Session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import generate_password_hash
from pymysql.cursors import DictCursor # for dictcursor

# Import functions for database operations
from db_operations import *


# App configuration
from config import config

# Classes and helper methods
from models.modelUser import ModelUser
from models.entities.user import User

app = Flask(__name__)

# Authentication token
csrf = CSRFProtect()

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
# Connection de database
db = MySQL(app)
# Initialize login manager
login_app = LoginManager(app)


@login_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db, id)


def is_logged_in():
    return current_user.is_authenticated


@app.route('/')
@login_required
def index():
    if not is_logged_in():
        return redirect(url_for('login'))

    equipos, hw_items = index_db(db, session)
    return render_template("index.html", equipos=equipos, items=hw_items)


@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'GET':
        return render_template('auth/sign-up.html')

    elif request.method == 'POST':
        username = request.form.get('username').strip().lower()
        password = request.form.get('password')

        hash = generate_password_hash(password)
        cursor = db.connection.cursor()
        try:
            cursor.execute('''INSERT INTO users (username, hash) VALUES (%s, %s)''', (username, hash,))

        except Exception:
            #flash('Username already exits. Please choose a different username')
            flash('El usuario ya existe. Inicia sesión o elige otro')

            return render_template('auth/sign-up.html')

        db.connection.commit()
        return redirect(url_for('login'))
        

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Forget any user_id
    session.clear()
    if request.method == 'GET':
        return render_template("auth/login.html")

    elif request.method == 'POST':
        username = request.form.get('username').strip().lower()
        password = request.form.get('password')

        try_user = User(0, username, password)
        user = ModelUser.login(db, try_user)

        if user != None:
            if user.password:
                login_user(user)
                session["username"] = user.username
                session["user_id"] = user.id
                return redirect(url_for('index'))
            else:
                # flash('Invalid password')
                flash('Contraseña invalida')
                return render_template('auth/login.html')
        else:
            # flash('User not found')
            flash('Usuario no encontrado')
            return render_template('auth/login.html')

@app.route('/logout')   
def logout():
    session.clear()
    logout_user()    
    return redirect(url_for('login'))


# ------------- AÑADIR REGISTRO DE PC -------------
@app.route("/add-register", methods = ["GET", "POST"])
@login_required
def add_register():
    if request.method == "GET":
        # show form
        return render_template("add-register.html")
    
    elif request.method == "POST":
        # process form
        pc = {}
        pc["nombre"] = request.form.get("nombre_pc").strip()
        pc["tipo"] = request.form.get("tipo_pc").strip()
        pc["marca"] = request.form.get("marca_pc").strip()
        pc["modelo"] = request.form.get("modelo_pc").strip()
        pc["n_id"] = request.form.get("n_identificador_pc").strip()
        pc["ubicacion"] = request.form.get("ubicacion_pc").strip()
        pc["estado"] = request.form.get("estado_pc").strip()
        pc["obser"] = request.form.get("observaciones_pc").strip() # observaciones

        if not pc["nombre"] and not pc["marca"] and not pc["modelo"] and not pc["n_id"] and not pc["ubicacion"] and not pc["estado"] and not pc["obser"]:
            return render_template("error.html", msg="No agregaste ningún dato al registro")

        # Register in db function
        id_equipo = add_register_db(db, session, pc)
        return redirect(url_for("add_hardware", id_equipo=id_equipo))


# ------------- ELIMINAR REGISTRO DE PC -------------
@app.route("/delete-register/<string:id>")
@login_required
def delete_register(id):
    # Delete regiser function
    delete_register_db(db, session, id)
    return redirect(url_for("index"))


# ------------- EDITAR REGISTRO DE PC -------------
@app.route("/edit-register/<string:id>", methods=["GET", "POST"])
@login_required
def edit_register(id):
    # Cargar formulario
    if request.method == "GET":
        cursor = db.connection.cursor()
        cursor.execute("SELECT * FROM equipos WHERE id_equipo = %s AND id_user = %s", (id, session["user_id"],))
        registro = cursor.fetchall()
        return render_template("edit-register.html", registro=registro[0])

    # Procesar formulario
    elif request.method == "POST":
        pc = {}
        pc["nombre"] = request.form.get("nombre_pc").strip()
        pc["tipo"] = request.form.get("tipo_pc").strip()
        pc["marca"] = request.form.get("marca_pc").strip()
        pc["modelo"] = request.form.get("modelo_pc").strip()
        pc["n_id"] = request.form.get("n_identificador_pc").strip()
        pc["ubicacion"] = request.form.get("ubicacion_pc").strip()
        pc["estado"] = request.form.get("estado_pc").strip()
        pc["obser"] = request.form.get("observaciones_pc").strip()
        # Submit to database function
        edit_register_post(db, session, pc, id)
        return redirect(url_for("edit_hardware", id=id))
    

# ------------- AÑADIR HARDWARE -------------
@app.route("/add-hardware/<id_equipo>", methods=["GET", "POST"])
@login_required
def add_hardware(id_equipo):
    # Cargar form
    if request.method == "GET":
        return render_template("add-hardware.html", id_equipo=id_equipo)
        
    # Process form
    elif request.method == "POST":
        hw = {}
        # Obtener data de todos los formularios
        hw["marcas"] = request.form.getlist("marca_hw")
        print(len(hw["marcas"]), "marca")
        hw["modelos"] = request.form.getlist("modelo_hw")
        print(len(hw["modelos"]), "modelo")
        hw["n_series"] = request.form.getlist("n_serie_hw")
        print(len(hw["n_series"]), "serial")
        hw["specs"] = request.form.getlist("especificaciones_hw")
        print(len(hw["specs"]), "specs")
        hw["capacidades"] = request.form.getlist("capacidad_hw")
        print(len(hw["capacidades"]), "capacidad")
        hw["tipos"] = request.form.getlist("tipo_hw")
        print(len(hw["tipos"]), "tipo")

        if not hw["modelos"] and not hw["n_series"] and not hw["specs"] and not hw["capacidades"]:
            return render_template("error.html", msg="No agregaste ningún dato al registro")        
        
        registers = add_hw_db(db, session, hw, id_equipo)

        if not registers:
            return render_template("error.html", msg="No agregaste ningún dato al registro")        

        return redirect(url_for("add_software", id_equipo=id_equipo))

        
# ------------- AÑADIR SOFTWARE -------------
@app.route("/add-software/<id_equipo>", methods=["GET", "POST"])
@login_required
def add_software(id_equipo):
    if request.method == "GET":
        return render_template("add-software.html", id_equipo=id_equipo)

    elif request.method == "POST":
        so = {}
        # Data de los Sistemas operativos
        so["nombres"] = request.form.getlist("nombre_so")
        print(len(so["nombres"]), "nombre so")
        so["ediciones"] = request.form.getlist("edicion_so")
        print(len(so["ediciones"]), "edicion so")
        so["arqs"] = request.form.getlist("arq_so")
        print(len(so["arqs"]), "Arquitectura so")
        so["desarrolladores"] = request.form.getlist("desarrollador_so")
        print(len(so["desarrolladores"]), "Desarrollador so")
        so["licencias"] = request.form.getlist("licencia_so")
        print(len(so["licencias"]), "licencia so")

        # Data de los formularios de programas
        sw = {}
        sw["categorias"] = request.form.getlist("categoria_sw")
        print(len(sw["categorias"]), "categorias")
        sw["nombres"] = request.form.getlist("nombre_sw")
        print(len(sw["nombres"]), "nombre")
        sw["versiones"] = request.form.getlist("version_sw")
        print(len(sw["versiones"]), "version")
        sw["desarrolladores"] = request.form.getlist("desarrollador_sw")
        print(len(sw["desarrolladores"]), "desarrollador")
        sw["licencias"] = request.form.getlist("licencia_sw")
        print(len(sw["licencias"]), "licencias")

        add_software_db(db, session, so, sw, id_equipo)
        return redirect(url_for("index"))


# ------------- EDITAR HARDWARE DE PC -------------
@app.route("/edit-hardware/<id>", methods = ["GET", "POST"])
@login_required
def edit_hardware(id):

    if request.method == "GET":
        hw = edit_hw_get(db, session, id)
        return render_template("edit-hardware.html", id_equipo = id, hw = hw)

    elif request.method == "POST":

        hw = {}
        # Obtener data de todos los formularios
        hw["marcas"] = request.form.getlist("marca_hw")
        print(len(hw["marcas"]), "marca")
        hw["modelos"] = request.form.getlist("modelo_hw")
        print(len(hw["modelos"]), "modelo")
        hw["n_series"] = request.form.getlist("n_serie_hw")
        print(len(hw["n_series"]), "serial")
        hw["specs"] = request.form.getlist("especificaciones_hw")
        print(len(hw["specs"]), "specs")
        hw["capacidades"] = request.form.getlist("capacidad_hw")
        print(len(hw["capacidades"]), "capacidad")
        hw["tipos"] = request.form.getlist("tipo_hw")
        print(len(hw["tipos"]), "tipo")
        # ID del componente de Hardware
        hw["ids"] = request.form.getlist("id_hw")
        print(len(hw["ids"]), "ID's hardawares ")

        edit_hw_post(db, session, hw)
        return redirect(url_for("edit_software", id=id))



# ----------- EDITAR SOFTWARE --------------
@app.route("/edit-software/<id>", methods= ["GET", "POST"])
@login_required
def edit_software(id):
    if request.method == "GET":
        sos, sw = edit_software_get(db, session, id)
        return render_template("edit-software.html", id_equipo=id, sos=sos, sw=sw)
    
    # --- POST ---
    elif request.method == "POST":
        so = {}
        # Obtener data de los SISTEMAS OPERATIVOS
        so["nombre"] = request.form.getlist("nombre_so")
        print(len(so["nombre"]), "nombre_so")
        so["edicion"] = request.form.getlist("edicion_so")
        print(len(so["edicion"]), "edicion_so")
        so["arq"] = request.form.getlist("arq_so")
        print(len(so["arq"]), "arq_so")
        so["desarrollador"] = request.form.getlist("desarrollador_so")
        print(len(so["desarrollador"]), "desarrollador_so")
        so["licencia"] = request.form.getlist("licencia_so")
        print(len(so["licencia"]), "licencia_so")
        # id del SISTEMA OPERATIVO
        so["ids"] = request.form.getlist("id_so")
        print(len(so["ids"]), "id_so")

        sw = {}
        # Obtener data de los PROGRAMAS
        sw["nombre"] = request.form.getlist("nombre_sw")
        print(len(sw["nombre"]), "nombre_sw")
        sw["version"] = request.form.getlist("version_sw")
        print(len(sw["version"]), "version_sw")
        sw["desarrollador"] = request.form.getlist("desarrollador_sw")
        print(len(sw["desarrollador"]), "desarrollador_sw")
        sw["licencia"] = request.form.getlist("licencia_sw")
        print(len(sw["licencia"]), "licencia_sw")
        sw["categoria"] = request.form.getlist("categoria_sw")
        print(len(sw["categoria"]), "categoria_sw")
        # ID del Software
        sw["ids"] = request.form.getlist("id_sw")
        print(len(sw["ids"]), "id_sw")

        # DB functions
        edit_software_so(db, session, so, id)
        edit_software_sw(db, session, sw, id)
        # Connectar a MySQL
        return redirect(url_for("index"))



# VER DATOS DE UN EQUIPOS
@app.route("/ver-registro/<id_equipo>")
@login_required
def ver_registro(id_equipo):
    # Get data from db function
    datos = ver_registro_db(db, session, id_equipo)
    return render_template("ver-registro.html", datos = datos)

# ------------- AÑADIR HARDWARE ITEM SIN EQUIPO -------------
@app.route("/add-hw-item", methods = ["GET", "POST"])
@login_required
def add_hw_item():
    if request.method == "GET":
        # show form
        return render_template("add-hw-item.html")
    
    elif request.method == "POST":
        hw = {}
        # Obtener data de todos los formularios
        hw["marcas"] = request.form.getlist("marca_hw")
        print(len(hw["marcas"]), "marca")

        hw["modelos"] = request.form.getlist("modelo_hw")
        print(len(hw["modelos"]), "modelo")

        hw["n_series"] = request.form.getlist("n_serie_hw")
        print(len(hw["n_series"]), "serial")

        hw["specs"] = request.form.getlist("especificaciones_hw")
        print(len(hw["specs"]), "specs")

        hw["capacidades"] = request.form.getlist("capacidad_hw")
        print(len(hw["capacidades"]), "capacidad")

        hw["tipos"] = request.form.getlist("tipo_hw")
        print(len(hw["tipos"]), "tipo")
        
        registers = add_hw_item_db(db, session, hw)
        
        if not registers:
            return render_template("error.html", msg="No agregaste ningún dato al registro")        

        return redirect(url_for("index"))


# ----- VER REGISTROS DE HARDWARES SIN EQUIPO
@app.route("/dashboard-hw")
@login_required
def dashboard_hw():
    cursor = db.connection.cursor()
    cursor.execute("SELECT * FROM hardware WHERE id_equipo IS NULL AND id_user = %s", (session["user_id"],))
    items = cursor.fetchall()

    return render_template("dashboard-hw.html", items=items)


# ----- ELIMINAR REGISTRO DE HARDWARE SIN EQUIPO -------------
@app.route("/delete-hw-item/<string:id>")
@login_required
def delete_hw_item(id):
    cursor = db.connection.cursor()
    cursor.execute("DELETE FROM hardware WHERE id_hw = %s AND id_user = %s", (id, session["user_id"],))
    db.connection.commit()
    return redirect(url_for("dashboard-hw"))


@app.route('/home')
@login_required
def home():
    return render_template('home.html')


@app.route('/dashboard-equipos')
def dashboard_equipos():
    if not is_logged_in():
        return redirect(url_for('login'))
    # Code to render the template with logged-in user information (if needed)
    # obtener lista de registros
    cursor = db.connection.cursor()
    cursor.execute("SELECT * FROM equipos WHERE id_user = %s", (session["user_id"],))
    equipos = cursor.fetchall()    
    return render_template('dashboard-equipos.html', equipos=equipos)


# Sample data for demonstration
# For exporting data
from io import StringIO
import csv as cs

@app.route("/csv", methods=["GET", "POST"])
def csv():	
	return render_template("csv.html")


@app.route("/export_csv", methods=["POST"])
def export_data():
  # Connect to MySQL database
    cursor = db.connection.cursor()
    # Data de equipos
    cursor.execute("SELECT * FROM equipos WHERE id_user = %s", (session["user_id"],))
    equipos = cursor.fetchall()    
    # Data de hardware
    cursor.execute("SELECT * FROM hardware WHERE id_equipo IS NULL AND id_user = %s", (session["user_id"],))
    hardware = cursor.fetchall()

    # Create a StringIO object to hold the CSV data
    csv_buffer = StringIO()
    fieldnames = [key for key in equipos[0]]

    writer = cs.DictWriter(csv_buffer, fieldnames=fieldnames)
    writer.writeheader()  

    # Write the data to the buffer
    for _ in equipos:
        writer.writerow(_)

    # Set response headers
    response = make_response(csv_buffer.getvalue())
    response.headers["Content-Disposition"] = "attachment;filename=hardware_software.csv"
    response.headers["Content-Type"] = "text/csv"

    return response

def status_401(error):
    return redirect(url_for('login'))

def status_404(error):
    return "<h1>Pagina no encontrada</h1>"

    

if __name__ == '__main__':
    app.config.from_object(config['development'])
    csrf.init_app(app)
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run()