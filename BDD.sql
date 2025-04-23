
CREATE TABLE vendedor(
id_vende INT AUTO_INCREMENT PRIMARY KEY,
nombre VARCHAR (20),
apellido VARCHAR (20),
tel INT (8)
); 

CREATE TABLE rango (
    id_rango INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(20) -- Ej: 'Junior', 'Senior', 'Admin'
);

CREATE TABLE cliente(
id_cliente INT AUTO_INCREMENT PRIMARY KEY,
nombre VARCHAR (20),
apellido VARCHAR (20),
tel INT (8),
dui INT (9),
correo VARCHAR (30),
direccion VARCHAR (50)
);
CREATE TABLE vendedor (
    id_vende INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(20),
    apellido VARCHAR(20),
    tel INT(8),
    id_rango INT,
    FOREIGN KEY (id_rango) REFERENCES rango(id_rango)
);

CREATE TABLE product(
id_product INT AUTO_INCREMENT PRIMARY KEY,
nombre VARCHAR (30),
descripcion VARCHAR (50), 
precio INT (10)
);

CREATE TABLE cliente (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(20),
    apellido VARCHAR(20),
    tel INT(8),
    dui INT(9),
    correo VARCHAR(30),
    direccion VARCHAR(50)
);

CREATE TABLE product (
    id_product INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(30),
    descripcion VARCHAR(50), 
    precio INT(10) -- En centavos
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