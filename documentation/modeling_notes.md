# Notas de modelado

## Decisiones clave
- Usar `Fecha-Ruta` como clave compuesta en los hechos para mantener el grano día-ruta; evita duplicidades cuando las rutas se repiten en distintas fechas.
- Limpiar nombres con prefijos tipo "Suma de" o "Recuento de" solo para métricas calculadas; los atributos deben quedar sin agregación (ej.: `Cantidad`, `Ingresos`, `Objetivo`, `Pasajeros`).
- `ProductoID` debe ser la clave de la dimensión Producto; en el hecho de ventas conviene añadirla (o un `ProductoKey`) para evitar depender de texto.
- En DimCalendario, derivar una columna `Fecha` (tipo Date) a partir de Año, MesNum y Día; mantener `EsLaborable` como indicador (0/1).

## Relaciones sugeridas
- DimCalendario (1) → FactVentas (∗) por `Fecha`.
- DimCalendario (1) → FactIncidencias (∗) por `Fecha`.
- DimRuta (1) → FactVentas (∗) por `Ruta`.
- DimRuta (1) → FactIncidencias (∗) por `Ruta`.
- FactIncidencias (∗) → FactVentas (∗) mediante tabla puente lógica usando `Fecha-Ruta` (activar solo en modelos que requieran analizar impacto de incidencias sobre ventas; preferible relación inactiva y medidas con `USERELATIONSHIP`).

## Medidas propuestas (DAX)
- Ventas: `SUM(FactVentas[IngresosTotales])`.
- Objetivo: `SUM(FactVentas[ObjetivoTotal])`.
- % Cumplimiento: `DIVIDE([Ventas], [Objetivo])`.
- Cantidad vendida: `SUM(FactVentas[Cantidad])`.
- Tickets: `COUNT(FactVentas[TicketID])`.
- Pasajeros: `SUM(FactVentas[Pasajeros])`.
- Ingreso por pasajero: `DIVIDE([Ventas], [Pasajeros])`.
- Ingreso promedio por ticket: `DIVIDE([Ventas], [Tickets])`.
- Incidencias: `SUM(FactIncidencias[RecuentoIncidenciaID])`.
- Minutos de incidencia: `SUM(FactIncidencias[DuracionMin])`.
- % días con incidencias: `DIVIDE(DISTINCTCOUNT(FactIncidencias[Fecha]), DISTINCTCOUNT(FactVentas[Fecha]))`.

## Calidad de datos / limpieza pendiente
- Confirmar que en FactVentas el campo `PorcentajeCumplimiento` es calculado en origen; recalcularlo en el modelo para consistencia.
- Verificar separadores decimales (coma vs punto) para evitar textos en lugar de números.
- Normalizar nombres de productos y rutas para evitar duplicados por mayúsculas o tildes.

## Exportar imagen del modelo
- El diagrama mermaid en `documentation/data_model.md` puede exportarse a PNG/SVG con `mmdc` (Mermaid CLI) o desde VS Code con la extensión Mermaid Markdown Preview.
