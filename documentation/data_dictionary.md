# Diccionario de datos

## Hechos

### ventas400PROC.csv (hechos de ventas)
| Columna | Descripción | Tipo | Ejemplo |
| --- | --- | --- | --- |
| Fecha | Fecha de la venta (agregada por día) | Fecha | 2024-01-05 |
| Fecha-Ruta | Clave compuesta día-ruta para agrupar ventas | Texto | 2024-01-05_BCN-MAD |
| Ruta | Código origen-destino | Texto | BCN-MAD |
| Producto | Nombre del producto vendido | Texto | Cerveza |
| Suma de Cantidad | Unidades vendidas | Numérico | 2 |
| Suma de IngresosPorTicket | Ingreso total del ticket | Numérico | 1472 |
| IngresoPromedioTicket | Promedio por ticket | Numérico | 1472 |
| IngresosTotales | Ingreso total (agregado) | Numérico | 1472 |
| Suma de PrecioUnit | Precio unitario registrado | Numérico | 736 |
| Suma de Pasajeros | Pasajeros en el trayecto | Numérico | 81 |
| IngresosPorPasajero | Ingreso medio por pasajero | Numérico | 18.17 |
| ObjetivoTotal | Objetivo de ingresos para la ruta/día | Numérico | 851 |
| Suma de ObjetivoVentas | Objetivo por ticket | Numérico | 851 |
| PorcentajeCumplimiento | % de cumplimiento vs objetivo | Texto (%) | 172,97 % |
| Recuento de TicketID | Número de tickets | Numérico | 1 |
| Ranking Productos | Ranking interno del producto | Numérico | 1 |
| DiaSemana | Día de la semana derivado | Texto | Friday |

### incidenciasPROC.csv (hechos de incidencias)
| Columna | Descripción | Tipo | Ejemplo |
| --- | --- | --- | --- |
| Fecha | Fecha de la incidencia | Fecha | 2024-01-01 |
| Fecha-Ruta | Clave día-ruta para agrupar incidencias | Texto | 2024-01-01_MAD-AGP |
| Ruta | Código origen-destino | Texto | MAD-AGP |
| Recuento de IncidenciaID | Número de incidencias | Numérico | 1 |
| Suma de DuracionMin | Duración total en minutos | Numérico | 54 |
| TipoIncidencia | Categoría del incidente | Texto | Retraso |
| Severidad | Grado de severidad | Texto | Media |

## Dimensiones

### productosPROC.csv (dim_producto)
| Columna | Descripción | Tipo | Ejemplo |
| --- | --- | --- | --- |
| ProductoID | Identificador de producto | Numérico | 1 |
| Producto | Nombre del producto | Texto | Agua |
| Categoría | Línea de producto | Texto | Bebidas |
| PrecioRecomendado | Precio sugerido | Numérico | 537 |

### rutasPROC.csv (dim_ruta)
| Columna | Descripción | Tipo | Ejemplo |
| --- | --- | --- | --- |
| Ruta | Código origen-destino | Texto | MAD-AGP |
| Origen | Ciudad de origen | Texto | MAD |
| Destino | Ciudad de destino | Texto | AGP |
| TipoTransporte | Modalidad | Texto | Ferrocarril |
| Suma de Distancia_km | Distancia estimada | Numérico | 359 |
| Recuento de RutaID | Conteo de rutas en el set | Numérico | 1 |

### calendarioPROC.csv (dim_calendario)
| Columna | Descripción | Tipo | Ejemplo |
| --- | --- | --- | --- |
| Fecha (derivar de Año/Día) | Fecha completa (día-mes-año) | Fecha | 2024-01-05 |
| Año | Año calendario | Numérico | 2024 |
| Trimestre | Q1–Q4 | Texto | Qtr 1 |
| Mes | Mes en texto (es/en) | Texto | enero / January |
| Día | Día del mes | Numérico | 5 |
| DiaSemana | Día de la semana | Texto | Friday |
| Suma de EsLaborable | Marcador de laborable (1/0) | Numérico | 1 |
| Suma de MesNum | Número de mes | Numérico | 1 |
| Suma de SemanaISO | Semana ISO | Numérico | 1 |

### medidasCRE.csv (resumen de métricas)
| Columna | Descripción | Tipo | Ejemplo |
| --- | --- | --- | --- |
| Ingresos | Ingresos totales del periodo | Numérico | 477327 |
| Objetivo | Objetivo total del periodo | Numérico | 457919 |
| Número incidencias | Conteo total de incidencias | Numérico | 109 |
| Porc Días con Incidencias | % de días con incidencias | Texto (%) | 19,67 % |
| Ventas días con Incidencias | Ventas en días con incidencias | Numérico | 383765 |
| Ventas días sin Incidencias | Ventas en días sin incidencias | Numérico | 93562 |
| Suma de Column | Campo residual del origen (puede omitirse) | Texto |  |
