CREATE TABLE rango (
    id_rango INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(20) -- Ej: 'Junior', 'Senior', 'Admin'
);

CREATE TABLE vendedor (
    id_vende INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(20),
    apellido VARCHAR(20),
    tel VARCHAR(15),
    id_rango INT,
    FOREIGN KEY (id_rango) REFERENCES rango(id_rango)
);


-- Junten User y cliente en una sola tabla, y añadan un campo que indique si es cliente o vendedor.
-- Tabla de usuarios
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    correo VARCHAR(100) UNIQUE,
    contraseña VARCHAR(255),
    rango VARCHAR(50) DEFAULT 'User',
    estado TINYINT(1) DEFAULT 1, 
);

CREATE TABLE cliente (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(20),
    apellido VARCHAR(20),
    tel VARCHAR(15),
    dui VARCHAR(10),
    correo VARCHAR(30),
    direccion VARCHAR(50)
);

CREATE TABLE product (
    id_product INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(30),
    descripcion VARCHAR(50), 
    precio INT -- En centavos
);

CREATE TABLE factura (
    id_factura INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT NOT NULL,
    id_vende INT NOT NULL,
    id_product INT NOT NULL,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    monto INT NOT NULL, -- En centavos

    FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente),
    FOREIGN KEY (id_vende) REFERENCES vendedor(id_vende),
    FOREIGN KEY (id_product) REFERENCES product(id_product)
);
