CREATE DATABASE Gestor;
USE Gestor;

-- 1. Rango
CREATE TABLE rango (
    id_rango INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(20) NOT NULL
);

-- 2. Usuarios
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    correo VARCHAR(100) UNIQUE,
    contraseña VARCHAR(255),
    rango VARCHAR(50) DEFAULT 'User',
    estado TINYINT(1) DEFAULT 1
);

-- 3. Cliente
CREATE TABLE cliente (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(20),
    apellido VARCHAR(20),
    tel VARCHAR(15),
    dui VARCHAR(10),
    correo VARCHAR(30),
    direccion VARCHAR(50)
);

-- 4. Vendedor
CREATE TABLE vendedor (
    id_vende INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(20),
    apellido VARCHAR(20),
    tel VARCHAR(15),
    id_rango INT,
    id_zona INT,
    FOREIGN KEY (id_rango) REFERENCES rango(id_rango),
    FOREIGN KEY (id_zona) REFERENCES Zona(id_zona)
);

-- 5. Cobrador
CREATE TABLE cobrador (
    id_cobrador INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(20),
    apellido VARCHAR(20),
    tel VARCHAR(15),
    id_rango INT,
    id_zona INT,
    cliente INT,
    FOREIGN KEY (id_rango) REFERENCES rango(id_rango),
    FOREIGN KEY (id_zona) REFERENCES Zona(id_zona),
    FOREIGN KEY (cliente) REFERENCES cliente(id_cliente)
);

-- 6. Producto
CREATE TABLE producto (
    id_product INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(30),
    descripcion VARCHAR(50), 
    precio INT NOT NULL,
    imagen BIT(1) DEFAULT 0, 
    stock INT DEFAULT 0, 
    id_catego INT NOT NULL,
    FOREIGN KEY (id_catego) REFERENCES categoria(id_categoria)
);

-- 7. Categoria
CREATE TABLE categoria (
    id_categoria INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(20),
    descripcion VARCHAR(50)
);

-- 8. Zona
CREATE TABLE Zona (
    id_zona INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(20)
);



-- 9. Factura de venta
CREATE TABLE factura_venta (
    id_factura_venta INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT NOT NULL,
    id_vende INT NOT NULL,
    id_product INT NOT NULL,
    id_catego INT NOT NULL,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    monto INT NOT NULL,
    FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente),
    FOREIGN KEY (id_vende) REFERENCES vendedor(id_vende),
    FOREIGN KEY (id_product) REFERENCES producto(id_product),
    FOREIGN KEY (id_catego) REFERENCES categoria(id_categoria)
);

-- 10. Factura de cobro
CREATE TABLE factura_cobro (
    id_factura_cobro INT AUTO_INCREMENT PRIMARY KEY,
    id_cobrador INT NOT NULL,
    id_zona INT NOT NULL,
    id_cliente INT NOT NULL,
    monto INT NOT NULL,
    fecha DATE NOT NULL,
    FOREIGN KEY (id_cobrador) REFERENCES cobrador(id_cobrador),
    FOREIGN KEY (id_zona) REFERENCES Zona(id_zona),
    FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente)
);

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
