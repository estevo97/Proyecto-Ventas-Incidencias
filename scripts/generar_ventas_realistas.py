"""
Script para generar datos de ventas realistas con:
- Múltiples tickets por Fecha-Ruta
- Cada ticket con varios productos
- PK: TicketID + Producto (línea de venta)
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Configuración
FECHA_INICIO = datetime(2024, 1, 1)
FECHA_FIN = datetime(2024, 3, 31)
RUTAS = ["MAD-BCN", "BCN-MAD", "MAD-PMI", "PMI-MAD", "MAD-AGP", "AGP-MAD", "BCN-PMI", "PMI-BCN"]
PRODUCTOS = ["Agua", "Cerveza", "Refresco", "Café", "Bocadillo", "Snack"]
CATEGORIAS = {
    "Agua": "Bebidas",
    "Cerveza": "Bebidas",
    "Refresco": "Bebidas",
    "Café": "Bebidas",
    "Bocadillo": "Comidas",
    "Snack": "Snacks"
}
PRECIOS = {
    "Agua": 2.5,
    "Cerveza": 8.0,
    "Refresco": 3.5,
    "Café": 4.0,
    "Bocadillo": 10.0,
    "Snack": 6.0
}

# Rango de pasajeros por ruta (aproximado)
PASAJEROS_MIN = 50
PASAJEROS_MAX = 250

datos = []
ticket_id = 1

# Iterar por fechas
fecha_actual = FECHA_INICIO
while fecha_actual <= FECHA_FIN:
    dia_semana = fecha_actual.strftime("%A")
    
    # Por cada ruta
    for ruta in RUTAS:
        # Tickets aleatorios por ruta-día (2-8 tickets)
        num_tickets_ruta = random.randint(2, 8)
        
        # Pasajeros en esa ruta-día (1 valor para toda la ruta)
        pasajeros_ruta = random.randint(PASAJEROS_MIN, PASAJEROS_MAX)
        
        for _ in range(num_tickets_ruta):
            # Cada ticket tiene 1-3 productos
            num_productos = random.randint(1, 3)
            productos_ticket = random.sample(PRODUCTOS, num_productos)
            
            for producto in productos_ticket:
                cantidad = random.randint(1, 3)
                precio_unitario = PRECIOS[producto] + random.uniform(-0.5, 0.5)  # Variación
                precio_unitario = round(precio_unitario, 2)
                
                # Objetivo de ventas (aproximado por ruta)
                objetivo_ventas = random.randint(600, 2000)
                
                # Crear fila
                fila = {
                    "TicketID": ticket_id,
                    "Fecha": fecha_actual.strftime("%Y-%m-%d"),
                    "Ruta": ruta,
                    "Fecha-Ruta": f"{fecha_actual.strftime('%Y-%m-%d')}_{ruta}",
                    "Producto": producto,
                    "Cantidad": cantidad,
                    "PrecioUnit": precio_unitario,
                    "Pasajeros": pasajeros_ruta,
                    "ObjetivoVentas": objetivo_ventas,
                    "DiaSemana": dia_semana
                }
                datos.append(fila)
            
            ticket_id += 1
    
    fecha_actual += timedelta(days=1)

# Crear DataFrame
df = pd.DataFrame(datos)

# Guardar CSV
ruta_salida = r"D:\OneDrive\Documentos\GitHub\Proyecto-Ventas-Incidencias\data\raw\Ventas_Realistas.csv"
df.to_csv(ruta_salida, index=False)

print(f"✅ Datos realistas generados: {ruta_salida}")
print(f"📊 Total de filas: {len(df)}")
print(f"🎫 Total de tickets únicos: {df['TicketID'].max()}")
print(f"📅 Período: {df['Fecha'].min()} a {df['Fecha'].max()}")
print(f"\n📋 Vista previa:")
print(df.head(15))
print(f"\n📈 Resumen por ruta:")
print(df.groupby("Ruta")["TicketID"].nunique().sort_values(ascending=False))
