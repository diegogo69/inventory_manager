# Flask utilities
from flask import Flask, flash, render_template, request, redirect, url_for, session, Response, make_response
# Database connector. Dict cursor for key acces intead of index
from flask_mysqldb import MySQL
from pymysql.cursors import DictCursor 
# Handling Session, login, and authentication
from flask_session import Session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import generate_password_hash
# Export to CSV files
from io import StringIO
import csv as csvv
# SYS for aborting the programs
import sys

# Import functions for database operations
from db_operations import *

# App configuration
from config import config

# Classes and helper methods
from models.modelUser import ModelUser
from models.entities.user import User

# Initialize Flask app object
app = Flask(__name__)
# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Authentication token
csrf = CSRFProtect()

# Connection de database
db = MySQL(app)

# Initialize login manager
login_app = LoginManager(app)
# Logged in manager function
def is_logged_in():
    return current_user.is_authenticated

@login_app.user_loader
def load_user(id):
    # Error handling for database connection
    try:
        return ModelUser.get_by_id(db, id)
    except Exception:
        print("Ha ocurrido un error al conectar con la base de datos")
        sys.exit()


# ----- MAIN PAGE -----
@app.route('/')
@login_required
def index():
    if not is_logged_in():
        return redirect(url_for('login'))
    equipos, hw_items = index_db(db, session)
    return render_template("index.html", equipos=equipos, items=hw_items, theme=session['theme'])


# ----- SIGN UP ----- 
@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'GET':
        return render_template('auth/sign-up.html')

    elif request.method == 'POST':
        # User's data
        username = request.form.get('username').strip().lower()
        password = request.form.get('password')
        hash = generate_password_hash(password)
        theme = "light"

        # Except inserting duplicates in the database
        cursor = db.connection.cursor()
        try:
            cursor.execute('''INSERT INTO users (username, hash, theme) VALUES (%s, %s, %s)''', (username, hash, theme,))

        except Exception:
            flash('El usuario ya existe. Inicia sesión o elige otro')
            return render_template('auth/sign-up.html')
        
        db.connection.commit()
        return redirect(url_for('login'))
        

# ----- LOGIN -----
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Forget any user_id
    session.clear()
    if request.method == 'GET':
        return render_template("auth/login.html")

    elif request.method == 'POST':
        username = request.form.get('username').strip().lower()
        password = request.form.get('password')

        # Create user object with built in methods and properties
        user_ = User(0, username, password)
        user = ModelUser.login(db, user_)

        # If there's a return user object
        if user != None:
            # If true. The password match
            if user.password:
                login_user(user)
                session["username"] = user.username
                session["user_id"] = user.id
                session['theme'] = user.theme
                return redirect(url_for('index'))
            # If false. The password is invalid
            else:
                flash('Contraseña invalida')
                return render_template('auth/login.html')
            
        else:
            # flash('User not found')
            flash('Usuario no encontrado')
            return render_template('auth/login.html')


# ----- LOG OUT -----
@app.route('/logout')   
def logout():
    # Save user's color theme
    cursor = db.connection.cursor()
    cursor.execute("UPDATE users SET theme = %s WHERE id_user = %s", (session['theme'], session['user_id'],))
    db.connection.commit()

    session.clear()
    logout_user()    
    return redirect(url_for('login'))


# ------- REGISTER PC ----------
@app.route("/add-register", methods = ["GET", "POST"])
@login_required
def add_register():
    if request.method == "GET":
        # Return form
        return render_template("add-register.html")
    
    elif request.method == "POST":
        # Process form data
        pc = {}
        pc["nombre"] = request.form.get("nombre_pc").strip()
        pc["tipo"] = request.form.get("tipo_pc").strip()
        pc["marca"] = request.form.get("marca_pc").strip()
        pc["modelo"] = request.form.get("modelo_pc").strip()
        pc["n_id"] = request.form.get("n_identificador_pc").strip()
        pc["ubicacion"] = request.form.get("ubicacion_pc").strip()
        pc["estado"] = request.form.get("estado_pc").strip()
        pc["obser"] = request.form.get("observaciones_pc").strip()

        # If the user does not enter any data. Return an error message
        if not pc["nombre"] and not pc["marca"] and not pc["modelo"] and not pc["n_id"] and not pc["ubicacion"] and not pc["estado"] and not pc["obser"]:
            return render_template("error.html", msg="No agregaste ningún dato al registro")

        # Register in db function
        id_equipo = add_register_db(db, session, pc)
        return redirect(url_for("add_hardware", id_equipo=id_equipo))


# ------- DELETE PC REGISTER ---------
@app.route("/delete-register/<string:id>")
@login_required
def delete_register(id):
    # Check if pc's id exists
    valid = check_valid_registro(db, session, id)
    if not valid:
        return render_template("error.html", msg="El equipo no existe")        

    # Delete register function
    delete_register_db(db, session, id)
    return redirect(url_for("index"))


# ------- EDIT PC REGISTER ---------
@app.route("/edit-register/<string:id>", methods=["GET", "POST"])
@login_required
def edit_register(id):
    # Check if pc's id exists
    valid = check_valid_registro(db, session, id)
    if not valid:
        return render_template("error.html", msg="El equipo no existe")        

    # Load pre-existing form data
    if request.method == "GET":
        cursor = db.connection.cursor()
        cursor.execute("SELECT * FROM equipos WHERE id_equipo = %s AND id_user = %s", (id, session["user_id"],))
        registro = cursor.fetchall()
        return render_template("edit-register.html", registro=registro[0])

    # Process formulario
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
    

# --------- ADD PC HARDWARE --------
@app.route("/add-hardware/<id_equipo>", methods=["GET", "POST"])
@login_required
def add_hardware(id_equipo):
    # Check if pc's id exists
    valid = check_valid_registro(db, session, id_equipo)
    if not valid:
        return render_template("error.html", msg="El equipo no existe")        

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

        # If too many components are entered. Return error
        if len(hw['marcas']) > 23:
            return render_template("error.html", msg="Se superó el límite de registro de datos")        

        # If user did not entered any data. Return an error message
        if not hw["modelos"] and not hw["n_series"] and not hw["specs"] and not hw["capacidades"]:
            return render_template("error.html", msg="No agregaste ningún dato al registro")        
        
        # Submit data registers to database. Returns False if not register was made
        registers = add_hw_db(db, session, hw, id_equipo)

        if not registers:
            return render_template("error.html", msg="No agregaste ningún dato al registro")        

        return redirect(url_for("add_software", id_equipo=id_equipo))

        
# ------- ADD PC SOFTWARE --------
@app.route("/add-software/<id_equipo>", methods=["GET", "POST"])
@login_required
def add_software(id_equipo):
    # Check if pc's id exists
    valid = check_valid_registro(db, session, id_equipo)
    if not valid:
        return render_template("error.html", msg="El equipo no existe")        

    if request.method == "GET":
        return render_template("add-software.html", id_equipo=id_equipo)

    elif request.method == "POST":
        so = {}
        # Operating system data
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

        # Software programs data
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

        # If too many components are entered. Return error
        if len(so['nombres']) > 3:
            return render_template("error.html", msg="Se superó el límite de registro de datos")        
        if len(sw['nombres']) > 20:
            return render_template("error.html", msg="Se superó el límite de registro de datos")        

        add_software_db(db, session, so, sw, id_equipo)
        return redirect(url_for("index"))


# ------- EDIT PC HARDWARE ---------
@app.route("/edit-hardware/<id>", methods = ["GET", "POST"])
@login_required
def edit_hardware(id):
    # Check if pc's id exists
    valid = check_valid_registro(db, session, id)
    if not valid:
        return render_template("error.html", msg="El equipo no existe")        

    # Get pre-existing form data
    if request.method == "GET":
        hw = edit_hw_get(db, session, id)
        print(hw, "HW")

        # Check if there are hw registers for the pc
        registers = False
        for value in hw.values():
            if not value:
                continue
            # If there are not hw registers. It nevers gets to to true
            registers = True
        print(registers)

        # If not registers at all. Render template for add hw
        if not registers:
            return redirect(url_for("add_hardware", id_equipo=id))

        return render_template("edit-hardware.html", id_equipo = id, hw = hw)

    elif request.method == "POST":

        hw = {}
        # Get hw form data
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

        # If too many components are entered. Return error
        if len(hw['marcas']) > 23:
            return render_template("error.html", msg="Se superó el límite de registro de datos")        

        edit_hw_post(db, session, hw)
        return redirect(url_for("edit_software", id=id))


# ------- EDIT SOFTWARE ---------
@app.route("/edit-software/<id>", methods= ["GET", "POST"])
@login_required
def edit_software(id):
    # Check if pc's id exists
    valid = check_valid_registro(db, session, id)
    if not valid:
        return render_template("error.html", msg="El equipo no existe")        

    # Load pre-existing form data
    if request.method == "GET":
        sos, sw = edit_software_get(db, session, id)
        print(sos, "SO")
        print(sw, "SW")

        # Check if there are so registers for the pc
        registers = False
        for value in sos[0].values():
            if not value:
                continue
            # If there are no hw registers. It nevers gets to to true
            registers = True
        print(registers)

        # If not registers at all. Render template for add hw
        if not registers:
            return redirect(url_for("add_software", id_equipo=id))

        return render_template("edit-software.html", id_equipo=id, sos=sos, sw=sw)
    
    # Submit data to database
    elif request.method == "POST":
        so = {}
        # Get Operating Systems data
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
        # Get software programs data
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

        # Submit OS data to db
        edit_software_so(db, session, so, id)
        # Submit SW Programs data to db
        edit_software_sw(db, session, sw, id)
        # Connectar a MySQL
        return redirect(url_for("index"))


# ------ VIEW PC COMPLETE DATA -------
@app.route("/ver-registro/<id_equipo>")
@login_required
def ver_registro(id_equipo):
    # Check if pc's id exists
    valid = check_valid_registro(db, session, id_equipo)
    if not valid:
        return render_template("error.html", msg="El equipo no existe")        

    # Get data from db function
    datos = ver_registro_db(db, session, id_equipo)
    return render_template("ver-registro.html", datos = datos)

# --- ADD A NON PC HARDWARE COMPONENT OR PERIPHERAL ---
@app.route("/add-hw-item", methods = ["GET", "POST"])
@login_required
def add_hw_item():
    if request.method == "GET":
        # show form
        return render_template("add-hw-item.html")
    
    elif request.method == "POST":
        hw = {}
        # Obtener data de todos los formularios
        hw["tipos"] = request.form.getlist("tipo_hw")
        print(len(hw["tipos"]), "tipo")
        hw["estados"] = request.form.getlist("estado_hw")
        print(len(hw["estados"]), "estado")
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

        # If too many components are entered. Return error
        if len(hw['marcas']) > 3:
            return render_template("error.html", msg="Se superó el límite de registro de datos")        

        # Submit to data base. It returns false if no data was registered       
        registers = add_hw_item_db(db, session, hw)
        
        if not registers:
            return render_template("error.html", msg="No agregaste ningún dato al registro")        

        return redirect(url_for("index"))


# -- VIEW NON PC HARDWARE ITEMS OR PERIPHERALS --
@app.route("/dashboard-hardware")
@login_required
def dashboard_hardware():
    cursor = db.connection.cursor()
    cursor.execute("SELECT * FROM hardware WHERE id_equipo IS NULL AND id_user = %s", (session["user_id"],))
    items = cursor.fetchall()

    return render_template("dashboard-hardware.html", items=items)


# ----- DELETE NON PC HARDWARE COMPONENT -------------
@app.route("/delete-hw-item/<string:id>")
@login_required
def delete_hw_item(id):
    cursor = db.connection.cursor()
    cursor.execute("DELETE FROM hardware WHERE id_hw = %s AND id_user = %s", (id, session["user_id"],))
    db.connection.commit()
    return redirect(url_for("dashboard_hardware"))


# HIDDEN HOME ROUTE TO TEST IF LOGIN WORKS
@app.route('/home')
@login_required
def home():
    return render_template('home.html')


# -- DASHBOARD FOR PC REGISTERS --
@app.route('/dashboard-equipos')
@login_required
def dashboard_equipos():
    # obtener lista de registros
    cursor = db.connection.cursor()
    cursor.execute("SELECT * FROM equipos WHERE id_user = %s", (session["user_id"],))
    equipos = cursor.fetchall()    
    return render_template('dashboard-equipos.html', equipos=equipos)


# -- EXPORT PC REGISTERS DATA --
@app.route("/export-equipos", methods=["POST"])
@login_required
def export_equipos():
  # Connect to MySQL database
    cursor = db.connection.cursor()
    cursor.execute("SELECT * FROM equipos WHERE id_user = %s", (session["user_id"],))
    equipos = cursor.fetchall()    

    # Create a StringIO object to hold the CSV data
    csv_buffer = StringIO()
    fieldnames = [key for key in equipos[0]]

    # csv didn't worked. So named it csvv
    writer = csvv.DictWriter(csv_buffer, fieldnames=fieldnames)
    writer.writeheader()  
    # Write the data to the buffer
    for row in equipos:
        writer.writerow(row)

    # Set response headers
    response = make_response(csv_buffer.getvalue())
    response.headers["Content-Disposition"] = "attachment;filename=registros_equipos.csv"
    response.headers["Content-Type"] = "text/csv"
    return response


# EXPORT NON PC HARDWARE REGISTERS
@app.route("/export-hardware", methods=["POST"])
@login_required
def export_hardware():
  # Connect to MySQL database
    cursor = db.connection.cursor()
    cursor.execute("SELECT * FROM hardware WHERE id_equipo IS NULL AND id_user = %s", (session["user_id"],))
    hardware = cursor.fetchall()

    # Create a StringIO object to hold the CSV data
    csv_buffer = StringIO()
    fieldnames = [key for key in hardware[0]]

    writer = csvv.DictWriter(csv_buffer, fieldnames=fieldnames)
    writer.writeheader()  
    # Write the data to the buffer
    for row in hardware:
        writer.writerow(row)

    # Set response headers
    response = make_response(csv_buffer.getvalue())
    response.headers["Content-Disposition"] = "attachment;filename=registros_hardware.csv"
    response.headers["Content-Type"] = "text/csv"
    return response


# EXPORT A PC REGISTER
@app.route("/export-registro", methods=["POST"])
@login_required
def export_registro():
  # Connect to MySQL database
    id_equipo = request.form.get("id_eq")
    datos = ver_registro_db(db, session, id_equipo)

    # Create a StringIO object to hold the CSV data
    csv_buffer = StringIO()
    fieldnames = [key for key in datos['equipos'][0].keys()]

    writer = csvv.DictWriter(csv_buffer, fieldnames=fieldnames)
    writer.writeheader()  
    # Write the data to the buffer
    for row in datos['equipos']:
        writer.writerow(row)

    # If there is hardware data
    if datos.get('hw'):
        writer.writerow({})
        row_header = [key for key in datos['hw'][0].keys()]
        writer = csvv.DictWriter(csv_buffer, fieldnames=row_header)
        writer.writeheader()  
        # Write the data to the buffer
        for row in datos['hw']:
            writer.writerow(row)

    # If there is os data
    if datos.get('so'):
        writer.writerow({})
        row_header = [key for key in datos['so'][0].keys()]
        writer = csvv.DictWriter(csv_buffer, fieldnames=row_header)
        writer.writeheader()  
        # Write the data to the buffer
        for row in datos['so']:
            writer.writerow(row)
            
    # If there is programs data
    if datos.get('sw'):
        writer.writerow({})
        row_header = [key for key in datos['sw'][0].keys()]
        writer = csvv.DictWriter(csv_buffer, fieldnames=row_header)
        writer.writeheader()  
        # Write the data to the buffer
        for row in datos['sw']:
            writer.writerow(row)

    # Set response headers
    response = make_response(csv_buffer.getvalue())
    # Get name of the pc registered
    pc_name = f"{datos['equipos'][0]['nombre']}"
    response.headers["Content-Disposition"] = f"attachment;filename=registro_{pc_name}.csv"
    response.headers["Content-Type"] = "text/csv"
    return response


# AJUSTES Y CONFIGURACION
@app.route("/ajustes", methods=['GET', 'POST'])
@login_required
def ajustes():
    if request.method == 'GET':
        print(session['theme'], 'GET')
        return render_template("ajustes.html", theme=session['theme'])
    
    elif request.method == 'POST':
        color = request.form.get("color_mode")
        if color:
            session['theme'] = color
        print(session['theme'], 'POST')
        return render_template("ajustes.html", theme=session['theme'])


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