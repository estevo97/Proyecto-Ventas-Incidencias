# Modelo de datos

```mermaid
erDiagram
    Calendario_DIM ||--o{ FactVentas : "Fecha"
    Producto_DIM ||--o{ FactVentas : "Producto"
    Ruta_DIM ||--o{ FactVentas : "Ruta"
    Calendario_DIM ||--o{ FactIncidencias : "Fecha"
    Ruta_DIM ||--o{ FactIncidencias : "Ruta"
```

- **Grano de FactVentas**: día-ruta-producto. Usa `Fecha-Ruta` como clave técnica para evitar ambigüedades si hay rutas repetidas por día.
- **Grano de FactIncidencias**: día-ruta. Se vincula a DimCalendario y DimRuta, y se puede relacionar a FactVentas por `Fecha-Ruta` para analizar impacto en ventas.
- **Claves recomendadas**:
  - DimCalendario: `Fecha` (derivada de columnas Año/Día).
  - DimRuta: `Ruta`.
  - DimProducto: `ProductoID` (y atributo `Producto` para la relación con el hecho si no hay ID en el hecho).
- **Relaciones sugeridas**: uno-a-muchos desde las dimensiones hacia los hechos, dirección de filtro bidireccional solo cuando sea necesario para analizar incidencias→ventas.
