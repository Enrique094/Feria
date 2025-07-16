
# prueba.py
from sqlalchemy import null


Precio_data = 100
meses = 10
interes = 0.05  # 5% de interés
cuotas = 0

if cuotas == 1:
    print( "el precio no cambia")
    Precio_Final = Precio_data
    print(f"El precio final es: {Precio_Final}")
    Precion_cuotas = 0
if cuotas == 0:
    def NuevoPrecio(precio: int, Meses: int):
        precio_nuevo = precio * (1+ interes) ** Meses  # Aplicando un descuento del 15%
        Precio_mensual = precio_nuevo / Meses
        return round(precio_nuevo, 2), round(Precio_mensual, 2)
    
    print(NuevoPrecio(Precio_data, meses)) # Ejemplo de uso)





# Debería imprimir el nuevo precio y el precio mensual





