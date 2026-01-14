# Notas de modelado

## Decisiones clave
    
### Claves y grano
- **FactVentas**:
  - **PK física**: `TicketID` (identifica cada ticket único; robusta ante cambios futuros).
  - **Grano analítico actual**: día-ruta-producto (nivel más granular en el modelo actual).
  - La columna `Fecha-Ruta` es auxiliar para análisis cruzados, no la PK.
  
- **FactIncidencias**:
  - **PK física**: `IncidenciaID` (identifica cada incidencia única; permite múltiples incidencias por día-ruta).
  - **Grano analítico actual**: día-ruta (en análisis agregados, pero pueden existir varias incidencias para la misma fecha-ruta).
  - Si en el futuro se añaden campos como hora o tipo detallado, el grano puede cambiar, pero `IncidenciaID` seguirá siendo la PK.

### Otras decisiones
- Limpiar nombres con prefijos tipo "Suma de" o "Recuento de" solo para métricas calculadas; los atributos deben quedar sin agregación (ej.: `Cantidad`, `Ingresos`, `Objetivo`, `Pasajeros`).
- `ProductoID` debe ser la clave de la dimensión Producto; en el hecho de ventas conviene añadirla (o un `ProductoKey`) para evitar depender de texto.
- En DimCalendario, derivar una columna `Fecha` (tipo Date) a partir de Año, MesNum y Día; mantener `EsLaborable` como indicador (0/1).

## Relaciones sugeridas
- DimCalendario (1) → FactVentas (∗) por `Fecha`.
- DimCalendario (1) → FactIncidencias (∗) por `Fecha`.
- DimRuta (1) → FactVentas (∗) por `Ruta`.
- DimRuta (1) → FactIncidencias (∗) por `Ruta`.
- DimProducto (1) → FactVentas (∗) por `ProductoID` (o `Producto` si no existe ID en el hecho).
- **NO relacionar FactVentas con FactIncidencias directamente** (sería M:M y causaría duplicados). Para analizar impacto de incidencias en ventas, usar medidas DAX que filtren por contexto de Fecha y Ruta desde las dimensiones compartidas.

## Medidas propuestas (DAX)
- Ventas: `SUM(FactVentas[IngresosTotales])`.
- Objetivo: `SUM(FactVentas[ObjetivoTotal])`.
- % Cumplimiento: `DIVIDE([Ventas], [Objetivo])`.
- Cantidad vendida: `SUM(FactVentas[Cantidad])`.
- Tickets: `COUNT(FactVentas[TicketID])`.
- Pasajeros: `SUM(FactVentas[Pasajeros])`.
- Ingreso por pasajero: `DIVIDE([Ventas], [Pasajeros])`.
- Ingreso promedio por ticket: `DIVIDE([Ventas], [Tickets])`.
- Incidencias: `COUNTROWS(FactIncidencias)` o `COUNT(FactIncidencias[IncidenciaID])`.
- Minutos de incidencia: `SUM(FactIncidencias[DuracionMin])`.
- % días con incidencias: `DIVIDE(DISTINCTCOUNT(FactIncidencias[Fecha]), DISTINCTCOUNT(FactVentas[Fecha]))`.

## Calidad de datos / limpieza pendiente
- Confirmar que en FactVentas el campo `PorcentajeCumplimiento` es calculado en origen; recalcularlo en el modelo para consistencia.
- Verificar separadores decimales (coma vs punto) para evitar textos en lugar de números.
- Normalizar nombres de productos y rutas para evitar duplicados por mayúsculas o tildes.

## Exportar imagen del modelo
- El diagrama mermaid en `documentation/data_model.md` puede exportarse a PNG/SVG con `mmdc` (Mermaid CLI) o desde VS Code con la extensión Mermaid Markdown Preview.
