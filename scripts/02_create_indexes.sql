-- =====================================================
-- SCRIPT: Optimización con Índices
-- Proyecto: Ventas e Incidencias - Schema Analytics
-- Autor: Sistema ETL
-- Fecha: 2026-01-24
-- =====================================================
-- Este script crea índices optimizados para mejorar
-- el performance de Power BI con DirectQuery
-- =====================================================

\c central_data;

-- =====================================================
-- ÍNDICES EN DIMENSIONES
-- =====================================================

-- dim_calendario: búsquedas por rangos de fecha
CREATE INDEX IF NOT EXISTS idx_calendario_anio ON analytics.dim_calendario(anio);
CREATE INDEX IF NOT EXISTS idx_calendario_mes ON analytics.dim_calendario(mesnum);
CREATE INDEX IF NOT EXISTS idx_calendario_trimestre ON analytics.dim_calendario(trimestre);
CREATE INDEX IF NOT EXISTS idx_calendario_diasemana ON analytics.dim_calendario(diasemana);
CREATE INDEX IF NOT EXISTS idx_calendario_laborable ON analytics.dim_calendario(eslaborable);

-- dim_productos: búsquedas por categoría
CREATE INDEX IF NOT EXISTS idx_productos_categoria ON analytics.dim_productos(categoria);
CREATE INDEX IF NOT EXISTS idx_productos_nombre ON analytics.dim_productos(nombre_producto);

-- dim_rutas: búsquedas frecuentes
CREATE INDEX IF NOT EXISTS idx_rutas_tipo ON analytics.dim_rutas(tipo_transporte);
CREATE INDEX IF NOT EXISTS idx_rutas_origen ON analytics.dim_rutas(origen);
CREATE INDEX IF NOT EXISTS idx_rutas_destino ON analytics.dim_rutas(destino);

-- dim_tipo_incidencia: búsquedas por categoría/criticidad
CREATE INDEX IF NOT EXISTS idx_tipo_inc_categoria ON analytics.dim_tipo_incidencia(categoria);
CREATE INDEX IF NOT EXISTS idx_tipo_inc_criticidad ON analytics.dim_tipo_incidencia(nivel_criticidad);

-- =====================================================
-- ÍNDICES EN FACT_VENTAS (crítico para performance)
-- =====================================================

-- Índice compuesto para filtros más comunes (fecha + ruta)
CREATE INDEX IF NOT EXISTS idx_ventas_fecha_ruta ON analytics.fact_ventas(fecha, rutaid);

-- Índices individuales para joins
CREATE INDEX IF NOT EXISTS idx_ventas_fecha ON analytics.fact_ventas(fecha);
CREATE INDEX IF NOT EXISTS idx_ventas_rutaid ON analytics.fact_ventas(rutaid);
CREATE INDEX IF NOT EXISTS idx_ventas_productoid ON analytics.fact_ventas(productoid);

-- Índice para filtros por incidencia
CREATE INDEX IF NOT EXISTS idx_ventas_tiene_incidencia ON analytics.fact_ventas(tiene_incidencia);

-- Índice para fecha_ruta (grano natural)
CREATE INDEX IF NOT EXISTS idx_ventas_fecha_ruta_key ON analytics.fact_ventas(fecha_ruta);

-- =====================================================
-- ÍNDICES EN FACT_INCIDENCIAS
-- =====================================================

-- Índice compuesto para filtros más comunes
CREATE INDEX IF NOT EXISTS idx_incidencias_fecha_ruta ON analytics.fact_incidencias(fecha, rutaid);

-- Índices individuales para joins
CREATE INDEX IF NOT EXISTS idx_incidencias_fecha ON analytics.fact_incidencias(fecha);
CREATE INDEX IF NOT EXISTS idx_incidencias_rutaid ON analytics.fact_incidencias(rutaid);
CREATE INDEX IF NOT EXISTS idx_incidencias_tipo ON analytics.fact_incidencias(tipo_incidencia);

-- Índice para filtros por severidad
CREATE INDEX IF NOT EXISTS idx_incidencias_severidad ON analytics.fact_incidencias(severidad);
CREATE INDEX IF NOT EXISTS idx_incidencias_critica ON analytics.fact_incidencias(es_critica);

-- =====================================================
-- CLUSTER (Reorganización física)
-- =====================================================
-- Reorganiza los datos físicamente según el índice
-- para mejorar velocidad de lectura secuencial

-- Cluster fact_ventas por fecha (queries suelen filtrar por rango de fechas)
CLUSTER analytics.fact_ventas USING idx_ventas_fecha_ruta;

-- Cluster fact_incidencias por fecha
CLUSTER analytics.fact_incidencias USING idx_incidencias_fecha_ruta;

-- =====================================================
-- VACUUM Y ANALYZE (Optimización de estadísticas)
-- =====================================================
-- Actualiza estadísticas para que el query planner
-- tome mejores decisiones

VACUUM ANALYZE analytics.dim_calendario;
VACUUM ANALYZE analytics.dim_productos;
VACUUM ANALYZE analytics.dim_rutas;
VACUUM ANALYZE analytics.dim_tipo_incidencia;
VACUUM ANALYZE analytics.fact_ventas;
VACUUM ANALYZE analytics.fact_incidencias;

-- =====================================================
-- ESTADÍSTICAS EXTENDIDAS (PostgreSQL 10+)
-- =====================================================
-- Ayuda al query planner con columnas correlacionadas

-- Estadísticas para ventas (fecha + ruta están correlacionadas)
DROP STATISTICS IF EXISTS analytics.stats_ventas_fecha_ruta;
CREATE STATISTICS analytics.stats_ventas_fecha_ruta (dependencies)
ON fecha, rutaid FROM analytics.fact_ventas;

-- Estadísticas para incidencias
DROP STATISTICS IF EXISTS analytics.stats_incidencias_fecha_ruta;
CREATE STATISTICS analytics.stats_incidencias_fecha_ruta (dependencies)
ON fecha, rutaid FROM analytics.fact_incidencias;

ANALYZE analytics.fact_ventas;
ANALYZE analytics.fact_incidencias;

-- =====================================================
-- VERIFICACIÓN DE ÍNDICES
-- =====================================================
-- Query para ver todos los índices creados

SELECT 
    schemaname,
    tablename,
    indexname,
    indexdef
FROM pg_indexes
WHERE schemaname = 'analytics'
ORDER BY tablename, indexname;

-- =====================================================
-- MÉTRICAS DE TAMAÑO
-- =====================================================
-- Ver tamaño de tablas e índices

SELECT 
    tablename,
    pg_size_pretty(pg_total_relation_size('analytics.' || tablename)) as total_size,
    pg_size_pretty(pg_relation_size('analytics.' || tablename)) as table_size,
    pg_size_pretty(pg_total_relation_size('analytics.' || tablename) - pg_relation_size('analytics.' || tablename)) as indexes_size
FROM pg_tables
WHERE schemaname = 'analytics'
ORDER BY pg_total_relation_size('analytics.' || tablename) DESC;

-- =====================================================
-- FIN DEL SCRIPT
-- =====================================================
-- Los índices mejorarán significativamente el performance
-- de Power BI en modo DirectQuery.
-- 
-- IMPORTANTE:
-- - Ejecutar este script DESPUÉS de cargar datos con ETL
-- - Re-ejecutar VACUUM ANALYZE después de cada carga grande
-- - Monitorear uso de índices con pg_stat_user_indexes
-- =====================================================
