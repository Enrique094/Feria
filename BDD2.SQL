CREATE DATABASE Gestor;
USE Gestor;

-- 1. Rango
CREATE TABLE rango (
    id_rango INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(20) NOT NULL
);

-- 2. Zona
CREATE TABLE zona (
    id_zona INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(20) NOT NULL 
);

-- 3. Categoria
CREATE TABLE categoria (
    id_categoria INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(20),
    descripcion VARCHAR(50)
);

-- 4. Usuarios
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    apellido VARCHAR(100),
    correo VARCHAR(100) UNIQUE,
    contraseña VARCHAR(255),
    estado TINYINT(1) DEFAULT 1,
    id_rango INT,
    FOREIGN KEY (id_rango) REFERENCES rango(id_rango)
);

-- 5. Cliente
CREATE TABLE cliente (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(20),
    apellido VARCHAR(20),
    id_rango INT,
    tel VARCHAR(15) UNIQUE,
    dui VARCHAR(10) UNIQUE ,
    correo VARCHAR(30) UNIQUE,
    direccion VARCHAR(50),
    FOREIGN KEY (id_rango) REFERENCES rango(id_rango)
);

-- 6. Vendedor
CREATE TABLE vendedor (
    id_vende INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(20),
    apellido VARCHAR(20),
    tel VARCHAR(15) UNIQUE,
    id_rango INT,
    id_zona INT,
    FOREIGN KEY (id_rango) REFERENCES rango(id_rango),
    FOREIGN KEY (id_zona) REFERENCES zona(id_zona)
);

-- 7. Cobrador
CREATE TABLE cobrador (
    id_cobrador INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(20),
    apellido VARCHAR(20),
    tel VARCHAR(15) UNIQUE,
    id_rango INT,
    id_zona INT,
    FOREIGN KEY (id_rango) REFERENCES rango(id_rango),
    FOREIGN KEY (id_zona) REFERENCES zona(id_zona)
);

-- 8. Relación Cobrador-Cliente (muchos a muchos)
CREATE TABLE cobrador_cliente (
    id_cobrador INT,
    id_cliente INT,
    PRIMARY KEY (id_cobrador, id_cliente),
    FOREIGN KEY (id_cobrador) REFERENCES cobrador(id_cobrador),
    FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente)
);

-- 9. Producto
CREATE TABLE producto (
    id_product INT AUTO_INCREMENT PRIMARY KEY,
    id_catego INT NOT NULL,
    nombre VARCHAR(30),
    descripcion VARCHAR(200), 
    precio INT NOT NULL,
    imagen BOOLEAN DEFAULT 0, 
    imagen_blob MEDIUMBLOB,
    stock INT DEFAULT 0, 
    FOREIGN KEY (id_catego) REFERENCES categoria(id_categoria)
);

CREATE TABLE intereses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    meses INT NOT NULL,
    porcentaje DECIMAL(5,2) NOT NULL
);


CREATE TABLE factura_venta (
    id_factura_venta INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT NOT NULL,
    id_vende INT NOT NULL,
    id_product INT NOT NULL,
    interes_aplicado DECIMAL(5,2) NOT NULL,
    es_credito DECIMAL NOT NULL DEFAULT 0,
    total DECIMAL(10,2) NOT NULL,
    cuotas INT NOT NULL,
    precio_mensual DECIMAL(10,2) NOT NULL,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    direccion VARCHAR(100) NOT NULL,
    FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente),
    FOREIGN KEY (id_vende) REFERENCES vendedor(id_vende),
    FOREIGN KEY (id_product) REFERENCES producto(id_product)
);


CREATE TABLE factura_cobro (
    id_factura_cobro INT AUTO_INCREMENT PRIMARY KEY,
    id_cobrador INT NOT NULL,
    id_zona INT NOT NULL,
    id_cliente INT NOT NULL,
    fecha DATE NOT NULL,
    FOREIGN KEY (id_cobrador) REFERENCES cobrador(id_cobrador),
    FOREIGN KEY (id_zona) REFERENCES zona(id_zona),
    FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente)
);

-- 12. Contrato
CREATE TABLE contrato (
    id_contrato INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT NOT NULL,
    id_vende INT NOT NULL,
    id_cobrador INT NOT NULL,
    fecha DATE NOT NULL,
    FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente),
    FOREIGN KEY (id_vende) REFERENCES vendedor(id_vende),
    FOREIGN KEY (id_cobrador) REFERENCES cobrador(id_cobrador)
);

-- 13. Abono sobre factura de venta
CREATE TABLE abono_venta (
    id_abono INT AUTO_INCREMENT PRIMARY KEY,
    id_factura_venta INT NOT NULL,
    id_cliente INT NOT NULL,
    id_cobrador INT NOT NULL,
    monto_abonado DECIMAL(10,2) NOT NULL,
    fecha DATE NOT NULL,
    FOREIGN KEY (id_factura_venta) REFERENCES factura_venta(id_factura_venta),
    FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente),
    FOREIGN KEY (id_cobrador) REFERENCES cobrador(id_cobrador)
);