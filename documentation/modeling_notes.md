# Notas de modelado

## Decisiones clave

### Claves y grano

- **FactVentas**:
  - **PK física actual**: `TicketID` (simplificada para este sample).
  - **⚠️ En datos reales**: La PK debería ser `TicketID + Producto`, ya que un ticket puede contener múltiples productos/líneas de venta.
  - **Grano actual**: cada fila representa una línea de venta (ticket-producto), pero TicketID no se repite en este dataset.
  - **Nivel de agregación**: La tabla ventas400PROC.csv está agregada a nivel `Fecha-Ruta-Producto` (suma de cantidades, tickets, ingresos por esa combinación).
  - Nota: Si se incorporasen datos sin agregar (grano fino), se debería usar `TicketID + Producto` como PK compuesta.
  
- **FactIncidencias**:
  - **PK física**: `IncidenciaID` (robusta ante cambios futuros).
  - **Grano actual**: Cada fila es una incidencia individual (sin agregación previa).
  - **Nivel de detalle**: día-ruta, pero pueden existir múltiples incidencias para la misma fecha-ruta (cosa que TicketID simple no permite en Ventas).

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

## Asunciones y limitaciones (sample de ChatGPT)
- **TicketID no se repite**: El dataset actual asume que cada ticket contiene un solo producto. En datos reales, un ticket puede tener múltiples productos/líneas, requiriendo PK compuesta `TicketID + Producto`.
- **Datos pre-agregados**: FactVentas está agregada a nivel `Fecha-Ruta-Producto` (no es grano fino TicketID individual).
- **Simplificación para demostración**: El modelo es válido para análisis BI pero no refleja la complejidad de un sistema real de POS (punto de venta).
- **Escalabilidad**: Si se incorporasen datos granulares reales (cada línea del ticket), habría que ajustar PKs y recalcular agregaciones.

## Exportar imagen del modelo
- El diagrama mermaid en `documentation/data_model.md` puede exportarse a PNG/SVG con `mmdc` (Mermaid CLI) o desde VS Code con la extensión Mermaid Markdown Preview.
