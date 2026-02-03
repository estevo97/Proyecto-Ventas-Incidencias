-- =====================================================
-- SCRIPT: Creación de Schema ANALYTICS
-- Proyecto: Ventas e Incidencias
-- Autor: Sistema ETL
-- Fecha: 2026-01-24
-- =====================================================
-- Este script crea un esquema optimizado para análisis
-- con modelo dimensional (Star Schema) listo para Power BI
-- =====================================================

-- Crear schema analytics si no existe
CREATE SCHEMA IF NOT EXISTS analytics;

-- =====================================================
-- DIMENSIONES (Lookup Tables)
-- =====================================================

-- Dimensión Calendario (limpia y enriquecida)
DROP TABLE IF EXISTS analytics.dim_calendario CASCADE;
CREATE TABLE analytics.dim_calendario (
    fecha DATE PRIMARY KEY,
    anio INTEGER NOT NULL,
    mesnum INTEGER NOT NULL,
    mes VARCHAR(20) NOT NULL,
    dia INTEGER NOT NULL,
    diasemana VARCHAR(20) NOT NULL,
    semanaiso INTEGER NOT NULL,
    eslaborable BOOLEAN NOT NULL,
    trimestre INTEGER NOT NULL,
    nombre_mes_anio VARCHAR(30) NOT NULL, -- Ej: "Enero 2024"
    es_fin_semana BOOLEAN NOT NULL
);

-- Dimensión Productos (limpia)
DROP TABLE IF EXISTS analytics.dim_productos CASCADE;
CREATE TABLE analytics.dim_productos (
    productoid INTEGER PRIMARY KEY,
    nombre_producto VARCHAR(100) NOT NULL,
    categoria VARCHAR(50), -- Ej: "Bebidas", "Snacks", "Comida"
    es_activo BOOLEAN DEFAULT TRUE
);

-- Dimensión Rutas (limpia y enriquecida)
DROP TABLE IF EXISTS analytics.dim_rutas CASCADE;
CREATE TABLE analytics.dim_rutas (
    rutaid INTEGER PRIMARY KEY,
    nombre_ruta VARCHAR(50) NOT NULL UNIQUE,
    origen VARCHAR(10),
    destino VARCHAR(10),
    tipo_transporte VARCHAR(20), -- "Avión" o "Tren"
    distancia_km INTEGER,
    es_activa BOOLEAN DEFAULT TRUE
);

-- Dimensión Tipos de Incidencia (catálogo)
DROP TABLE IF EXISTS analytics.dim_tipo_incidencia CASCADE;
CREATE TABLE analytics.dim_tipo_incidencia (
    tipo_incidencia VARCHAR(50) PRIMARY KEY,
    categoria VARCHAR(30), -- "Operacional", "Técnica", "Externa"
    nivel_criticidad VARCHAR(10), -- "Baja", "Media", "Alta"
    descripcion TEXT
);

-- =====================================================
-- TABLAS DE HECHOS (Fact Tables)
-- =====================================================

-- FACT: Ventas (granularidad: ticket individual)
DROP TABLE IF EXISTS analytics.fact_ventas CASCADE;
CREATE TABLE analytics.fact_ventas (
    venta_id BIGSERIAL PRIMARY KEY,
    ticketid INTEGER NOT NULL,
    
    -- Claves foráneas (dimensiones)
    fecha DATE NOT NULL REFERENCES analytics.dim_calendario(fecha),
    rutaid INTEGER NOT NULL REFERENCES analytics.dim_rutas(rutaid),
    productoid INTEGER NOT NULL REFERENCES analytics.dim_productos(productoid),
    
    -- Atributos degenerados (del ticket)
    fecha_ruta VARCHAR(50) NOT NULL, -- Grano natural: fecha + ruta
    
    -- Métricas de venta
    cantidad INTEGER NOT NULL CHECK (cantidad >= 0),
    precio_unitario NUMERIC(10,2) NOT NULL CHECK (precio_unitario >= 0),
    ingresos_total NUMERIC(12,2) NOT NULL CHECK (ingresos_total >= 0),
    
    -- Contexto operativo
    pasajeros INTEGER,
    objetivo_ventas INTEGER,
    
    -- Indicadores calculados
    porcentaje_objetivo NUMERIC(5,2), -- (ingresos_total / objetivo_ventas) * 100
    tiene_incidencia BOOLEAN DEFAULT FALSE, -- Si ese día-ruta tuvo incidencia
    
    -- Auditoría
    fecha_carga TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Restricción de grano único
    UNIQUE(ticketid, fecha_ruta, productoid)
);

-- FACT: Incidencias (granularidad: incidencia individual)
DROP TABLE IF EXISTS analytics.fact_incidencias CASCADE;
CREATE TABLE analytics.fact_incidencias (
    incidencia_id SERIAL PRIMARY KEY,
    incidenciaid INTEGER NOT NULL,
    
    -- Claves foráneas (dimensiones)
    fecha DATE NOT NULL REFERENCES analytics.dim_calendario(fecha),
    rutaid INTEGER NOT NULL REFERENCES analytics.dim_rutas(rutaid),
    tipo_incidencia VARCHAR(50) REFERENCES analytics.dim_tipo_incidencia(tipo_incidencia),
    
    -- Atributos degenerados
    fecha_ruta VARCHAR(50) NOT NULL,
    
    -- Métricas de incidencia
    severidad VARCHAR(20) NOT NULL,
    duracion_minutos INTEGER NOT NULL CHECK (duracion_minutos >= 0),
    
    -- Indicadores calculados
    es_critica BOOLEAN, -- Si severidad = 'Alta'
    duracion_horas NUMERIC(5,2), -- duracion_minutos / 60
    
    -- Auditoría
    fecha_carga TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Restricción de grano único
    UNIQUE(incidenciaid)
);

-- =====================================================
-- VISTA AGREGADA: Análisis Ventas vs Incidencias
-- =====================================================
-- Vista pre-calculada para Power BI (performance)
DROP VIEW IF EXISTS analytics.vw_ventas_incidencias_diarias CASCADE;
CREATE VIEW analytics.vw_ventas_incidencias_diarias AS
SELECT 
    v.fecha,
    v.rutaid,
    r.nombre_ruta,
    r.tipo_transporte,
    c.diasemana,
    c.eslaborable,
    
    -- Agregaciones de ventas
    COUNT(DISTINCT v.ticketid) as num_tickets,
    SUM(v.cantidad) as cantidad_total_vendida,
    SUM(v.ingresos_total) as ingresos_totales,
    AVG(v.precio_unitario) as precio_promedio,
    AVG(v.pasajeros) as pasajeros_promedio,
    MAX(v.objetivo_ventas) as objetivo_ventas,
    
    -- Indicadores de incidencias
    COUNT(i.incidencia_id) as num_incidencias,
    COALESCE(SUM(i.duracion_minutos), 0) as duracion_total_incidencias,
    MAX(CASE WHEN i.severidad = 'Alta' THEN 1 ELSE 0 END) as tuvo_incidencia_alta,
    
    -- Métricas calculadas
    CASE 
        WHEN COUNT(i.incidencia_id) > 0 THEN 'Con Incidencia'
        ELSE 'Sin Incidencia'
    END as estado_dia,
    
    -- Impacto estimado (simplificado)
    CASE 
        WHEN COUNT(i.incidencia_id) > 0 
        THEN SUM(v.ingresos_total) * 0.85 -- Asume 15% de pérdida
        ELSE SUM(v.ingresos_total)
    END as ingresos_ajustados

FROM analytics.fact_ventas v
LEFT JOIN analytics.fact_incidencias i 
    ON v.fecha = i.fecha AND v.rutaid = i.rutaid
INNER JOIN analytics.dim_rutas r ON v.rutaid = r.rutaid
INNER JOIN analytics.dim_calendario c ON v.fecha = c.fecha

GROUP BY 
    v.fecha, 
    v.rutaid, 
    r.nombre_ruta, 
    r.tipo_transporte,
    c.diasemana,
    c.eslaborable;

-- =====================================================
-- COMENTARIOS (Documentación en BD)
-- =====================================================
COMMENT ON SCHEMA analytics IS 'Schema optimizado para análisis de ventas e incidencias - listo para Power BI';
COMMENT ON TABLE analytics.fact_ventas IS 'Tabla de hechos con todas las transacciones de venta (granularidad: ticket)';
COMMENT ON TABLE analytics.fact_incidencias IS 'Tabla de hechos con todas las incidencias operacionales';
COMMENT ON VIEW analytics.vw_ventas_incidencias_diarias IS 'Vista agregada día-ruta para dashboard principal';

COMMENT ON COLUMN analytics.fact_ventas.tiene_incidencia IS 'Indica si ese día-ruta tuvo al menos una incidencia';
COMMENT ON COLUMN analytics.fact_ventas.porcentaje_objetivo IS 'Porcentaje de cumplimiento del objetivo de ventas';

-- =====================================================
-- FIN DEL SCRIPT
-- =====================================================
