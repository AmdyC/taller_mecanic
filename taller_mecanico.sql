CREATE DATABASE IF NOT EXISTS taller_mecanico;
USE taller_mecanico;

CREATE TABLE IF NOT EXISTS clientes (
    dni VARCHAR(255) PRIMARY KEY,
    nombre VARCHAR(255),
    apellido VARCHAR(255),
    direccion VARCHAR(255),
    telefono VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS mecanicos (
    legajo VARCHAR(255) PRIMARY KEY,
    nombre VARCHAR(255),
    apellido VARCHAR(255),
    rol VARCHAR(255),
    estado VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS productos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(255),
    precio INT,
    fabricante VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS proveedores (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(255),
    cuit VARCHAR(255),
    telefono VARCHAR(255),
    direccion VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(255),
    apellido VARCHAR(255),
    usuario VARCHAR(255) UNIQUE,
    contrasena VARCHAR(255),
    rol VARCHAR(255)
);