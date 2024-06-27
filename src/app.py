from flask import Flask, flash, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from flask_session import Session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import generate_password_hash
from pymysql.cursors import DictCursor # for dictcursor

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
    # Code to render the template with logged-in user information (if needed)
    # obtener lista de registros
    cursor = db.connection.cursor()
    cursor.execute("SELECT * FROM equipos WHERE id_user = %s", (session["user_id"],))
    equipos = cursor.fetchall()    
    return render_template("index.html", equipos=equipos)


@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'GET':
        return render_template('auth/sign-up.html')

    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        hash = generate_password_hash(password)
        cursor = db.connection.cursor()
        try:
            cursor.execute('''INSERT INTO users (username, hash) VALUES (%s, %s)''', (username, hash,))

        except Exception:
            flash('Username already exits. Please choose a different username')
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
        username = request.form.get('username')
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
                flash('Invalid password')
                return render_template('auth/login.html')

        else:
            flash('User not found')
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

        # Submit to data base
        cursor = db.connection.cursor()
        cursor.execute("INSERT INTO equipos (nombre, tipo, marca, modelo, n_identificador, ubicacion, estado, observaciones, id_user) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                       (pc["nombre"], pc["tipo"], pc["marca"], pc["modelo"], pc["n_id"], pc["ubicacion"], pc["estado"], pc["obser"], session["user_id"],))
        db.connection.commit()

        # id del equipo recién añadido
        id_equipo = cursor.lastrowid

        return redirect(url_for("add_hardware", id_equipo=id_equipo))


# ------------- ELIMINAR REGISTRO DE PC -------------
@app.route("/delete-register/<string:id>")
@login_required
def delete_register(id):
    cursor = db.connection.cursor()

    cursor.execute("DELETE FROM so WHERE id_equipo = %s AND id_user = %s", (id, session["user_id"],))

    cursor.execute("DELETE FROM programas WHERE id_equipo = %s AND id_user = %s", (id, session["user_id"],))

    cursor.execute("DELETE FROM hardware WHERE id_equipo = %s AND id_user = %s", (id, session["user_id"],))

    cursor.execute("DELETE FROM equipos WHERE id_equipo = %s AND id_user = %s", (id, session["user_id"],))

    db.connection.commit()
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
        print(registro[0]) #        
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
        
        cursor = db.connection.cursor()
        cursor.execute("""
            UPDATE equipos
            SET nombre = %s,
                tipo = %s,
                marca = %s,
                modelo = %s,
                n_identificador = %s,
                ubicacion = %s,
                estado = %s,
                observaciones = %s
            WHERE id_equipo = %s
            AND id_user = %s
            """, (pc["nombre"], pc["tipo"], pc["marca"], pc["modelo"], pc["n_id"], pc["ubicacion"], pc["estado"], pc["obser"], id, session["user_id"]))

        db.connection.commit()

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
        
        # Connectar a MySQL
        cursor = db.connection.cursor()
        registers = 0

        # Insertar datos uno a uno
        for i in range(len(hw["capacidades"])):

            marca = hw["marcas"][i].strip()
            modelo = hw["modelos"][i].strip()
            n_serie = hw["n_series"][i].strip()
            specs = hw["specs"][i].strip()
            capacidad = hw["capacidades"][i].strip()
            tipo = hw["tipos"][i].strip()

            # si no hay ningun dato. no registrar
            if (not marca or marca == "intel") and not modelo and not n_serie and not specs and not capacidad:
                continue

            else:
                registers += 1
            
            # Generar query.
            cursor.execute("""INSERT INTO hardware (marca, modelo, n_serie, especificaciones, capacidad, tipo, id_equipo) 
                                VALUES (%s, %s, %s, %s, %s, %s, %s) WHERE id_user = %s""", 
                            (marca, modelo, n_serie, specs, capacidad, tipo, id_equipo, session["user_id"],))
        
        if registers == 0:
            return render_template("error.html", msg="No agregaste ningún dato al registro")        

        # Registrar queries en la database
        db.connection.commit()

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
        so["nombres"] = request.form.getlist("nombre_so").strip()
        print(len(so["nombres"]), "nombre so")

        so["ediciones"] = request.form.getlist("edicion_so").strip()
        print(len(so["ediciones"]), "edicion so")

        so["arqs"] = request.form.getlist("arq_so").strip()
        print(len(so["arqs"]), "Arquitectura so")


        so["desarrolladore"] = request.form.getlist("desarrollador_so").strip()
        print(len(so["desarrolladores"]), "Desarrollador so")

        so["licencias"] = request.form.getlist("licencia_so").strip()
        print(len(so["licencias"]), "licencia so")


        # Data de los formularios de programas
        sw = {}
        sw["categorias"] = request.form.getlist("categoria_sw").strip()
        print(len(sw["categorias"]), "categorias")

        sw["nombres"] = request.form.getlist("nombre_sw").strip()
        print(len(sw["nombres"]), "nombre")

        sw["versiones"] = request.form.getlist("version_sw").strip()
        print(len(sw["versiones"]), "version")

        sw["desarrolladores"] = request.form.getlist("desarrollador_sw").strip()
        print(len(sw["desarrolladores"]), "desarrollador")

        sw["licencias"] = request.form.getlist("licencia_sw").strip()
        print(len(sw["licencias"]), "licencias")

        # Connectar a MySQL
        cursor = db.connection.cursor()

        # Insertar datos Sistema Operativo
        for i in range(len(so["nombres"])):

            # si no hay ningun dato. no registrar
            if (not so["nombres"] or so["nombres"] == "windows") and not so["ediciones"] and not so["desarrolladores"] and not so["licencias"]:
                continue
            
            # Generar query.
            cursor.execute("""INSERT INTO so (
                                nombre, edicion, 
                                arquitectura, desarrollador, 
                                licencia, id_equipo) 
                                VALUES (
                                    %s, %s,
                                        %s, %s, 
                                    %s, %s
                                ) WHERE id_user = %s
                           """, 
                        (so["nombres"][i], so["ediciones"][i], so["arqs"][i], so["desarrolladores"][i], so["licencias"][i], id_equipo,))
        
        # Insertar datos Programas
        for i in range(len(sw["nombres"])):
            
            # si no hay ningun dato. no registrar
            if not sw["nombres"][i] and not sw["versiones"][i] and not sw["desarrolladores"][i] and not sw["licencias"][i]:
                continue

            # Generar query.
            cursor.execute("""INSERT INTO programas (
                                categoria, nombre, 
                                version, desarrollador, 
                                licencia, id_equipo) 
                                VALUES (
                                    %s, %s, 
                                    %s, %s, 
                                    %s, %s
                                ) WHERE id_user = %s
                            """, 
                            (sw["categorias"][i], sw["nombres"][i], sw["versiones"][i], sw["desarrolladores"][i], 
                             sw["licencias"][i], id_equipo, session["user_id"]))


        # Registrar queries en la database
        db.connection.commit()

        return redirect(url_for("index"))


# ------------- EDITAR HARDWARE DE PC -------------
@app.route("/edit-hardware/<id>", methods = ["GET", "POST"])
@login_required
def edit_hardware(id):

    if request.method == "GET":
        cursor = db.connection.cursor()
        hw = {}

        cursor.execute("SELECT * FROM hardware WHERE id_equipo = %s AND tipo = %s AND id_user = %s", (id, "cpu", session["user_id"],))
        hw["cpu"] = cursor.fetchone()

        cursor.execute("SELECT * FROM hardware WHERE id_equipo = %s AND tipo = %s AND id_user = %s", (id, "ram", session["user_id"],))
        hw["ram"] = cursor.fetchall()

        cursor.execute("SELECT * FROM hardware WHERE id_equipo = %s AND tipo = %s AND id_user = %s", (id, "almacenamiento", session["user_id"],))
        hw["alm"] = cursor.fetchall()

        cursor.execute("SELECT * FROM hardware WHERE id_equipo = %s AND tipo = %s AND id_user = %s", (id, "placa", session["user_id"],))
        hw["placa"] = cursor.fetchone()

        cursor.execute("SELECT * FROM hardware WHERE id_equipo = %s AND tipo = %s AND id_user = %s", (id, "fuente", session["user_id"],))
        hw["fuente"] = cursor.fetchone()

        cursor.execute("SELECT * FROM hardware WHERE id_equipo = %s AND tipo = %s AND id_user = %s", (id, "gpu", session["user_id"],))
        hw["gpu"] = cursor.fetchone()

        cursor.execute("SELECT * FROM hardware WHERE id_equipo = %s AND tipo = %s AND id_user = %s", (id, "monitor", session["user_id"],))
        hw["mon"] = cursor.fetchall()

        cursor.execute("SELECT * FROM hardware WHERE id_equipo = %s AND tipo = %s AND id_user = %s", (id, "teclado", session["user_id"],))
        hw["tec"] = cursor.fetchone()

        cursor.execute("SELECT * FROM hardware WHERE id_equipo = %s AND tipo = %s AND id_user = %s", (id, "mouse", session["user_id"],))
        hw["mou"] = cursor.fetchone()

        cursor.execute("SELECT * FROM hardware WHERE id_equipo = %s AND tipo = %s AND id_user = %s", (id, "impresora", session["user_id"],))
        hw["imp"] = cursor.fetchone()

        cursor.execute("""
                       SELECT * FROM hardware WHERE id_equipo = %s
                       AND id_user = %s
                       AND (
                        tipo = %s OR tipo = %s OR
                        tipo = %s OR tipo = %s OR
                        tipo = %s OR tipo = %s OR
                        tipo = %s)
                       """, 
                       (id, session["user_id"], "red", "bluetooth", "webcam", "escaner", "altavoces", "audifonos", "otro",))
        hw["otros"] = cursor.fetchall()

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

        # Connectar a MySQL
        cursor = db.connection.cursor()

        # Insertar datos uno a uno
        for i in range(len(hw["marcas"])):
            
            # Generar query.
            cursor.execute("""
                           UPDATE hardware 
                           SET marca = %s, 
                               modelo = %s, 
                               n_serie = %s, 
                               especificaciones = %s, 
                               capacidad = %s, 
                               tipo = %s 
                           WHERE id_hw = %s
                           AND id_user = %s
                           """,
                           (hw["marcas"][i], hw["modelos"][i], 
                            hw["n_series"][i], hw["specs"][i], 
                            hw["capacidades"][i], hw["tipos"][i], hw["ids"][i], session["user_id"]))
            
        # Registrar queries en la databasework
        db.connection.commit()

        return redirect(url_for("edit_software", id=id))



# ----------- EDITAR SOFTWARE --------------
@app.route("/edit-software/<id>", methods= ["GET", "POST"])
@login_required
def edit_software(id):
    if request.method == "GET":
        cursor = db.connection.cursor()

        cursor.execute("SELECT * FROM so WHERE id_equipo = %s AND id_user = %s", (id, session["user_id"]))
        sos = cursor.fetchall()

        sw = {}
        cursor.execute("SELECT * FROM programas WHERE id_equipo = %s AND categoria = %s AND id_user = %s", (id, "navegador", session["user_id"],))
        sw["navs"] = cursor.fetchall()

        cursor.execute("SELECT * FROM programas WHERE id_equipo = %s AND categoria = %s AND id_user = %s", (id, "ofimatica", session["user_id"],))
        sw["ofis"] = cursor.fetchall()

        cursor.execute("SELECT * FROM programas WHERE id_equipo = %s AND categoria = %s AND id_user = %s", (id, "seguridad", session["user_id"],))
        sw["segs"] = cursor.fetchall()

        cursor.execute("""
                        SELECT * FROM programas WHERE id_equipo = %s
                        AND id_user = %s
                        AND (
                            categoria = %s OR categoria = %s OR
                            categoria = %s OR categoria = %s OR
                            categoria = %s OR categoria = %s OR
                            categoria = %s OR categoria = %s OR
                            categoria = %s
                        )""", 
                       (id, session["user_id"], "multimedia", "diseño grafico", 
                        "diseño audiovisual", "sistema", 
                        "administrativo", "comunicacion", 
                        "desarrollo", "videojuego",
                        "otro",))
        sw["otros"] = cursor.fetchall()

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

        # Connectar a MySQL
        cursor = db.connection.cursor()


        # Insertar datos SISTEMA OPERATIVO
        for i in range(len(so["nombre"])):

            print(so["ids"][i], f"ID SO [{i}]")
            
            if not so["ids"][i]:

                # Generar query.
                cursor.execute("""
                               INSERT INTO so (
                                    nombre, edicion, 
                                    arquitectura, desarrollador, 
                                    licencia, id_equipo, id_user) 
                                    VALUES (
                                    %s, %s,
                                    %s, %s, 
                                    %s, %s)
                            """, 
                            (so["nombre"][i], so["edicion"][i], 
                            so["arq"][i], so["desarrollador"][i], 
                            so["licencia"][i], id, session["user_id"],))
                
            elif so["ids"][i]:
                # Generar query.
                cursor.execute("""
                            UPDATE so 
                            SET nombre = %s, 
                                edicion = %s, 
                                arquitectura = %s, 
                                desarrollador = %s, 
                                licencia = %s
                            WHERE id_so = %s
                            AND id_user = %s
                            """,
                            (so["nombre"][i], so["edicion"][i], 
                                so["arq"][i], so["desarrollador"][i], 
                                so["licencia"][i], so["ids"][i], session["user_id"]))

        for i in range(len(sw["nombre"])):
            if not sw["ids"][i]:
                # Generar query.
                cursor.execute("""INSERT INTO programas (
                                    categoria, nombre, 
                                    version, desarrollador, 
                                    licencia, id_equipo, id_user) 
                                    VALUES (
                                    %s, %s, 
                                    %s, %s, 
                                    %s, %s, %s)
                                """, 
                                (sw["categoria"][i], sw["nombre"][i], 
                                 sw["version"][i], sw["desarrollador"][i], 
                                 sw["licencia"][i], id, session["user_id"],))

            elif sw["ids"][i]:
                # Generar query.
                cursor.execute("""
                            UPDATE programas 
                            SET categoria = %s, 
                                nombre = %s, 
                                version = %s, 
                                desarrollador = %s, 
                                licencia = %s 
                            WHERE id_sw = %s
                            AND id_user = %s
                            """,
                            (sw["categoria"][i], sw["nombre"][i], 
                                sw["version"][i], sw["desarrollador"][i], 
                                sw["licencia"][i], sw["ids"][i], session["user_id"],))

        # Registrar queries en la database
        db.connection.commit()

        return redirect(url_for("index"))



# VER DATOS DE UN EQUIPOS
@app.route("/ver-registro/<id_equipo>")
@login_required
def ver_registro(id_equipo):
    cursor = db.connection.cursor()

    datos = {}
    
    cursor.execute("SELECT * FROM equipos WHERE id_equipo = %s AND id_user = %s", (id_equipo, session["user_id"],))
    datos["equipos"] = cursor.fetchall()
    print("\n Prueba datos del Equipo\n")
    print(datos["equipos"])

    cursor.execute("SELECT * FROM hardware WHERE id_equipo = %s AND id_user = %s", (id_equipo, session["user_id"],))
    datos["hw"] = cursor.fetchall()
    print("\n Prueba datos del hardware\n")
    print(datos["hw"])

    cursor.execute("SELECT * FROM so WHERE id_equipo = %s AND id_user = %s", (id_equipo, session["user_id"],))
    datos["so"] = cursor.fetchall()
    print("\n Prueba datos del SO\n")
    print(datos["so"])

    cursor.execute("SELECT * FROM programas WHERE id_equipo = %s AND id_user = %s", (id_equipo, session["user_id"],))
    datos["sw"] = cursor.fetchall()
    print("\n Prueba datos de programas\n")
    print(datos["sw"])

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
        
        # Connectar a MySQL
        cursor = db.connection.cursor()
        registers = 0

        # Insertar datos uno a uno
        for i in range(len(hw["capacidades"])):

            marca = hw["marcas"][i].strip()
            modelo = hw["modelos"][i].strip()
            n_serie = hw["n_series"][i].strip()
            specs = hw["specs"][i].strip()
            capacidad = hw["capacidades"][i].strip()
            tipo = hw["tipos"][i].strip()

            # si no hay ningun dato. no registrar
            if (not marca or marca == "intel") and not modelo and not n_serie and not specs and not capacidad:
                continue

            else:
                registers += 1
            
            # Generar query.
            cursor.execute("""INSERT INTO hardware (marca, modelo, n_serie, especificaciones, capacidad, tipo, id_user) 
                                VALUES (%s, %s, %s, %s, %s, %s)""", 
                            (marca, modelo, n_serie, specs, capacidad, tipo, session["user_id"],))
        
        if registers == 0:
            return render_template("error.html", msg="No agregaste ningún dato al registro")        

        # Registrar queries en la database
        db.connection.commit()

        return redirect(url_for("index"))


# ----- VER REGISTROS DE HARDWARES SIN EQUIPO
@app.route("/view-hw-items")
@login_required
def view_hw_items():
    cursor = db.connection.cursor()
    cursor.execute("SELECT * FROM hardware WHERE id_equipo IS NULL AND id_user = %s", (session["user_id"],))
    items = cursor.fetchall()

    return render_template("view-hw-items.html", items=items)


# ----- ELIMINAR REGISTRO DE HARDWARE SIN EQUIPO -------------
@app.route("/delete-hw-item/<string:id>")
@login_required
def delete_hw_item(id):
    cursor = db.connection.cursor()
    cursor.execute("DELETE FROM hardware WHERE id_hw = %s AND id_user = %s", (id, session["user_id"],))
    db.connection.commit()
    return redirect(url_for("view_hw_items"))


@app.route('/home')
@login_required
def home():
    return render_template('home.html')


@app.route('/dash')
def dash():
    return render_template('dashboard.html')


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