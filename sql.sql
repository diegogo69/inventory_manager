CREATE DATABASE inventario;

CREATE TABLE users (
	id_user INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    hash VARCHAR(255) NOT NULL
    );

CREATE TABLE equipos (
    id_equipo INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(50),
    tipo VARCHAR(50),
    marca VARCHAR(50),
    modelo VARCHAR(50),
    n_identificador VARCHAR(50),
    ubicacion VARCHAR(50),
    estado VARCHAR(50),
    observaciones VARCHAR(255)
    id_user INT,
    FOREIGN KEY(id_user) REFERENCES users(id_user)
    );

CREATE TABLE hardware (
    id_hw INT PRIMARY KEY AUTO_INCREMENT,
    tipo VARCHAR(50),
    marca VARCHAR(50),
    modelo VARCHAR(50),
    n_serie VARCHAR(50),
    especificaciones VARCHAR(255),
    capacidad VARCHAR(50),
    estado VARCHAR(50),
    id_equipo INT,
    id_user INT,
    FOREIGN KEY(id_user) REFERENCES users(id_user),
    FOREIGN KEY(id_equipo) REFERENCES equipos(id_equipo)
);

CREATE TABLE so (
    id_so INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(50),
    edicion VARCHAR(50),
    arquitectura VARCHAR(50),
    desarrollador VARCHAR(50),
    licencia VARCHAR(100),
    id_equipo INT,
    id_user INT,
    FOREIGN KEY(id_user) REFERENCES users(id_user),
    FOREIGN KEY(id_equipo) REFERENCES equipos(id_equipo)
);

CREATE TABLE programas (
    id_sw INT PRIMARY KEY AUTO_INCREMENT,
    categoria VARCHAR(50),
    nombre VARCHAR(50),
    version VARCHAR(50),
    desarrollador VARCHAR(50),
    licencia VARCHAR(100),
    id_equipo INT,
    id_user INT,
    FOREIGN KEY(id_user) REFERENCES users(id_user),
    FOREIGN KEY(id_equipo) REFERENCES equipos(id_equipo)
);
