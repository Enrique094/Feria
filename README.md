# FERIA DE LOGROS
GestorPlus

# Agregar a la BDD
--Asegurar que el id rango esten asignados del 1 al 4

INSERT INTO rango (nombre) VALUES
('Administrador'),
('Cliente'),
('Vendedor'),
('Cobrador');


# Apartador agregados
- Asegurar que el id rango esten asignados del 1 al 4
- Decorador agregado para verificar que el usuario es administrador
# Modificar el registro de administrador
- Agregar un campo de contraseña al formulario de registro de selecionar rango

# Apartados por agregar
- Triggers para la funcion del abono y el total de deuda del cliente
- Triggers para la resta de stock de los productos



AGREAG ESO 


CREATE TABLE abonos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT,
    id_cobrador INT,
    monto DECIMAL(10,2),
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
    id_factura INT,  -- RELACIONADO A factura_venta
    FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente),
    FOREIGN KEY (id_factura) REFERENCES factura_venta(id)
);
