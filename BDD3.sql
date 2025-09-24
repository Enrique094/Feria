CREATE DATABASE Gestor;
USE Gestor;

--  Rango
CREATE TABLE rango (
    id_rango INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(20) NOT NULL
);

--  Categoria
CREATE TABLE categoria (
    id_categoria INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(20),
    descripcion VARCHAR(50)
);

--  Usuarios
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    apellido VARCHAR(100),
    correo VARCHAR(100) UNIQUE,
    telefono VARCHAR(15),
    contraseña VARCHAR(255),
    DUI VARCHAR(10) UNIQUE,
    direccion VARCHAR(80),
    estado TINYINT(1) DEFAULT 1,
    id_rango INT,
    FOREIGN KEY (id_rango) REFERENCES rango(id_rango)
);

--  Producto
CREATE TABLE producto (
    id_product INT AUTO_INCREMENT PRIMARY KEY,
    id_catego INT NOT NULL,
    nombre VARCHAR(30),
    descripcion VARCHAR(200), 
    precio decimal(10,2) DEFAULT NULL,
    imagen BOOLEAN DEFAULT 0, 
    imagen_blob MEDIUMBLOB,
    stock INT DEFAULT 0, 
    FOREIGN KEY (id_catego) REFERENCES categoria(id_categoria)
);

--  Intereses
CREATE TABLE intereses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    meses INT NOT NULL,
    porcentaje DECIMAL(5,2) NOT NULL
);

--  Factura de Venta
CREATE TABLE factura_venta (
    id_factura_venta INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT NOT NULL,
    id_cobrador INT NOT NULL,
    id_vendedor INT NOT NULL,
    id_product INT NOT NULL,
    interes_aplicado DECIMAL(5,2) NOT NULL,
    es_credito DECIMAL NOT NULL DEFAULT 0,
    estado_pago ENUM('pendiente', 'parcial', 'pagado') DEFAULT 'pendiente',
    monto_abonado DECIMAL(10,2) DEFAULT 0.00,
    total DECIMAL(10,2) NOT NULL,
    cuotas INT NOT NULL,
    precio_mensual DECIMAL(10,2) NOT NULL,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    direccion VARCHAR(100) NOT NULL,
    FOREIGN KEY (id_cliente) REFERENCES usuarios(id),
    FOREIGN KEY (id_cobrador) REFERENCES usuarios(id),
    FOREIGN KEY (id_vendedor) REFERENCES usuarios(id),
    FOREIGN KEY (id_product) REFERENCES producto(id_product)
);

--  Factura de Cobro
CREATE TABLE factura_cobro (
    id_factura_cobro INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    fecha DATE NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id)
);

--  Abono sobre factura de venta
CREATE TABLE abono_venta (
    id_abono INT AUTO_INCREMENT PRIMARY KEY,
    id_factura_venta INT NOT NULL,
    id_usuario INT NOT NULL,
    monto_abonado DECIMAL(10,2) NOT NULL,
    mes_correspondiente INT NOT NULL DEFAULT 1,
    año_correspondiente INT NOT NULL DEFAULT YEAR(CURDATE()),
    saldo_pendiente DECIMAL(10,2) NOT NULL DEFAULT 0,
    observaciones VARCHAR(200) NULL,
    fecha DATE NOT NULL,
    FOREIGN KEY (id_factura_venta) REFERENCES factura_venta(id_factura_venta),
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id)
);