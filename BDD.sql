USE sql5774043;

CREATE TABLE vendedor(
id_vende INT AUTO_INCREMENT PRIMARY KEY,
nombre VARCHAR (20),
apellido VARCHAR (20),
tel INT (8)
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

CREATE TABLE product(
id_product INT AUTO_INCREMENT PRIMARY KEY,
nombre VARCHAR (30),
descripcion VARCHAR (50), 
precio INT (10)
);
