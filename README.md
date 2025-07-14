# FERIA DE LOGROS
GestorPlus

# Agregar a la BDD
--Asegurar que el id rango esten asignados del 1 al 4

INSERT INTO rango (nombre) VALUES
('Administrador'),
('Cliente'),
('Vendedor'),
('Cobrador');

INSERT INTO `usuarios` (`id`, `nombre`, `apellido`, `correo`, `contraseña`, `estado`, `id_rango`) VALUES (NULL, 'Admin', NULL, 'Admin@gmail.com', '1234', '1', '1');

INSERT INTO `zona` (`id_zona`, `nombre`) VALUES (NULL, 'Centro'), (NULL, 'Norte'), (NULL, 'Sur'), (NULL, 'Este'), (NULL, 'Oeste');

INSERT INTO `categoria` (`id_categoria`, `nombre`, `descripcion`) VALUES (NULL, 'Ropa', 'Vestidos, uniformes'), (NULL, 'Electrodomesticos', 'Dispositivos electrónicos');


# Apartador agregados
- Asegurar que el id rango esten asignados del 1 al 4
- Decorador agregado para verificar que el usuario es administrador
# Modificar el registro de administrador
- Agregar un campo de contraseña al formulario de registro de selecionar rango


# Apartados por agregar
- Triggers para la funcion del abono y el total de deuda del cliente
- Triggers para la resta de stock de los productos