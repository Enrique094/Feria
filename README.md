# FERIA DE LOGROS
GestorPlus

# Agregar a la BDD
Usar la BDD llamada gestor.sql
--Asegurar que el id rango esten asignados del 1 al 4

INSERT INTO rango (nombre) VALUES
('Administrador'),
('Cliente'),
('Vendedor'),
('Cobrador');

INSERT INTO `usuarios` (`id`, `nombre`, `apellido`, `correo`, `telefono`, `contraseña`, `DUI`, `direccion`, `estado`, `id_rango`) VALUES (NULL, 'Admin', NULL, 'admin@gmail.com', NULL, '1234', NULL, NULL, '1', '1');

INSERT INTO `categoria` (`id_categoria`, `nombre`, `descripcion`) VALUES (NULL, 'Ropa', 'Vestidos, uniformes'), (NULL, 'Electrodomesticos', 'Dispositivos electrónicos');


# Apartador agregados
- Asegurar que el id rango esten asignados del 1 al 4
- Decorador agregado para verificar que el usuario es administrador
# Modificar el registro de administrador
- Agregar un campo de contraseña al formulario de registro de selecionar rango


# Apartados por agregar
- Triggers para la funcion del abono y el total de deuda del cliente
- Triggers para la resta de stock de los productos
