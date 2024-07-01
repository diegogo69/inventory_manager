def index_db(db, session):
    # Lista de registros para la pagina principal
    cursor = db.connection.cursor()
    # Data de equipos
    cursor.execute("SELECT * FROM equipos WHERE id_user = %s", (session["user_id"],))
    equipos = cursor.fetchall()    
    # Data de hardware
    cursor.execute("SELECT * FROM hardware WHERE id_equipo IS NULL AND id_user = %s", (session["user_id"],))
    hw_items = cursor.fetchall()
    return equipos, hw_items

def add_register_db(db, session, pc):
    # Submit to data base
    cursor = db.connection.cursor()
    cursor.execute("INSERT INTO equipos (nombre, tipo, marca, modelo, n_identificador, ubicacion, estado, observaciones, id_user) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                    (pc["nombre"], pc["tipo"], pc["marca"], pc["modelo"], pc["n_id"], pc["ubicacion"], pc["estado"], pc["obser"], session["user_id"],))
    db.connection.commit()

    # id del equipo recién añadido
    id_equipo = cursor.lastrowid
    return id_equipo

def delete_register_db(db, session, id):
    cursor = db.connection.cursor()
    cursor.execute("DELETE FROM so WHERE id_equipo = %s AND id_user = %s", (id, session["user_id"],))
    cursor.execute("DELETE FROM programas WHERE id_equipo = %s AND id_user = %s", (id, session["user_id"],))
    cursor.execute("DELETE FROM hardware WHERE id_equipo = %s AND id_user = %s", (id, session["user_id"],))
    cursor.execute("DELETE FROM equipos WHERE id_equipo = %s AND id_user = %s", (id, session["user_id"],))
    db.connection.commit()
    return

def edit_register_post(db, session, pc, id):
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
    return


def add_hw_db(db, session, hw, id_equipo):
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
        cursor.execute("""INSERT INTO hardware (marca, modelo, n_serie, especificaciones, capacidad, tipo, id_equipo, id_user) 
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""", 
                        (marca, modelo, n_serie, specs, capacidad, tipo, id_equipo, session["user_id"],))
        
        # Si no hay ningun registro.
        if registers == 0:
            return False
        
        # Si hay registros
        db.connection.commit()
    return True


def add_software_db(db, session, so, sw, id_equipo):
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
                            licencia, id_equipo, id_user) 
                            VALUES (
                                %s, %s,
                                    %s, %s, 
                                %s, %s, %s
                            )
                        """, 
                    (so["nombres"][i].strip(), so["ediciones"][i].strip(), 
                        so["arqs"][i].strip(), so["desarrolladores"][i].strip(), 
                        so["licencias"][i].strip(), id_equipo, session["user_id"]))
    
    # Insertar datos Programas
    for i in range(len(sw["nombres"])):
        
        # si no hay ningun dato. no registrar
        if not sw["nombres"][i] and not sw["versiones"][i] and not sw["desarrolladores"][i] and not sw["licencias"][i]:
            continue

        # Generar query.
        cursor.execute("""INSERT INTO programas (
                            categoria, nombre, 
                            version, desarrollador, 
                            licencia, id_equipo, id_user) 
                            VALUES (
                                %s, %s, 
                                %s, %s, 
                                %s, %s, %s
                            )
                        """, 
                        (sw["categorias"][i].strip(), sw["nombres"][i].strip(), 
                            sw["versiones"][i].strip(), sw["desarrolladores"][i].strip(), 
                            sw["licencias"][i].strip(), id_equipo, session["user_id"]))

    # Registrar queries en la database
    db.connection.commit()
    return


def edit_hw_get(db, session, id):
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
    return hw


def edit_hw_post(db, session, hw):
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
                        (hw["marcas"][i].strip(), hw["modelos"][i].strip(), 
                        hw["n_series"][i].strip(), hw["specs"][i].strip(), 
                        hw["capacidades"][i].strip(), hw["tipos"][i].strip(), 
                        hw["ids"][i], session["user_id"]))
    # Registrar queries en la databasework
    db.connection.commit()
    return


def edit_software_get(db, session, id):
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
    return sos, sw


def edit_software_so(db, session, so, id):
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
                        (so["nombre"][i].strip(), so["edicion"][i].strip(), 
                        so["arq"][i].strip(), so["desarrollador"][i].strip(), 
                        so["licencia"][i].strip(), id, session["user_id"],))
            
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
                        (so["nombre"][i].strip(), so["edicion"][i].strip(), 
                            so["arq"][i].strip(), so["desarrollador"][i].strip(), 
                            so["licencia"][i].strip(), so["ids"][i], session["user_id"]))
    db.connection.commit()
    return


def edit_software_sw(db, session, sw, id):
    cursor = db.connection.cursor()

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
                            (sw["categoria"][i].strip(), sw["nombre"][i].strip(), 
                                sw["version"][i].strip(), sw["desarrollador"][i].strip(), 
                                sw["licencia"][i].strip(), id, session["user_id"],))

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
                        (sw["categoria"][i].strip(), sw["nombre"][i].strip(), 
                            sw["version"][i].strip(), sw["desarrollador"][i].strip(), 
                            sw["licencia"][i].strip(), sw["ids"][i], session["user_id"],))
    # Registrar queries en la database
    db.connection.commit()
    return


def ver_registro_db(db, session, id_equipo):
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

    return datos


def add_hw_item_db(db, session, hw):
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
    # Si no hay registros
    if registers == 0:
        return False
    
    # Registrar queries en la database
    db.connection.commit()
    return True
