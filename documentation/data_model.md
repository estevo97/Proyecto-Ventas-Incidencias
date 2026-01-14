# Modelo de datos

```mermaid
erDiagram
    Calendario_DIM ||--o{ Ventas : "Fecha"
    Producto_DIM ||--o{ Ventas : "Producto"
    Ruta_DIM ||--o{ Ventas : "Ruta"
    Calendario_DIM ||--o{ Incidencias : "Fecha"
    Ruta_DIM ||--o{ Incidencias : "Ruta"
    
    classDef ventasStyle fill:#90EE90,stroke:#228B22,stroke-width:2px
    classDef incidenciasStyle fill:#FFB6C1,stroke:#DC143C,stroke-width:2px
    
    class Ventas ventasStyle
    class Incidencias incidenciasStyle
```   

- **Grano de Ventas**: La clave primaria es TicketID. El grano es Fecha - Ruta - Producto
- **Grano de Incidencias**: La clave primaria IncidenciaID. El grano es Fecha - Ruta
- **Claves recomendadas**:
  - Calendario: `Fecha` (derivada de columnas Año/Día).
  - Ruta: `Ruta`.
  - Producto: `ProductoID`.
- **Relaciones sugeridas**: 
  - Todas las relaciones son 1:∗ desde dimensiones hacia hechos (esquema estrella clásico).
  - Ambos hechos se relacionan con Calendario y Ruta, pero **no entre sí** (evita la problemática M:M).
  - Para analizar impacto de incidencias en ventas, usar medidas DAX con contexto compartido de Fecha y Ruta.
