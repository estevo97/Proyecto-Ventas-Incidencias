"""
=====================================================
ETL PIPELINE: RAW → ANALYTICS
=====================================================
Script que extrae datos de schema 'public' (raw),
transforma y enriquece los datos, y los carga en
el schema 'analytics' optimizado para Power BI.

Autor: Sistema ETL Automatizado
Fecha: 2026-01-24
=====================================================
"""

import psycopg2
from psycopg2.extras import execute_batch
import pandas as pd
from datetime import datetime
import logging
from typing import Dict, Tuple
import sys

# =====================================================
# CONFIGURACIÓN
# =====================================================

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('etl_pipeline.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Credenciales de Railway PostgreSQL
DB_CONFIG = {
    'host': 'hopper.proxy.rlwy.net',
    'port': 57761,
    'database': 'central_data',
    'user': 'postgres',
    'password': 'TU_PASSWORD_AQUI'  # ⚠️ CAMBIAR ESTO
}

# =====================================================
# FUNCIONES AUXILIARES
# =====================================================

def get_connection():
    """Crea conexión a PostgreSQL"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        logger.info("✅ Conexión a PostgreSQL establecida")
        return conn
    except Exception as e:
        logger.error(f"❌ Error conectando a BD: {e}")
        raise

def extract_raw_data(conn) -> Dict[str, pd.DataFrame]:
    """Extrae datos de las tablas raw"""
    logger.info("📥 Extrayendo datos de schema 'public' (raw)...")
    
    queries = {
        'calendario': "SELECT * FROM public.calendario_raw",
        'productos': "SELECT * FROM public.productos_raw",
        'rutas': "SELECT * FROM public.rutas_raw",
        'ventas': "SELECT * FROM public.ventas_raw",
        'incidencias': "SELECT * FROM public.incidencias_raw"
    }
    
    data = {}
    for name, query in queries.items():
        try:
            df = pd.read_sql(query, conn)
            data[name] = df
            logger.info(f"  ✅ {name}: {len(df)} filas extraídas")
        except Exception as e:
            logger.error(f"  ❌ Error extrayendo {name}: {e}")
            raise
    
    return data

def transform_calendario(df: pd.DataFrame) -> pd.DataFrame:
    """Transforma y enriquece la dimensión calendario"""
    logger.info("🔄 Transformando dim_calendario...")
    
    df_clean = df.copy()
    df_clean.columns = df_clean.columns.str.lower()
    
    # Asegurar que fecha es tipo date
    df_clean['fecha'] = pd.to_datetime(df_clean['fecha'])
    
    # Calcular trimestre
    df_clean['trimestre'] = df_clean['fecha'].dt.quarter
    
    # Nombre mes-año (ej: "Enero 2024")
    df_clean['nombre_mes_anio'] = df_clean['fecha'].dt.strftime('%B %Y')
    
    # Es fin de semana
    df_clean['es_fin_semana'] = df_clean['diasemana'].isin(['Sábado', 'Domingo'])
    
    logger.info(f"  ✅ Calendario transformado: {len(df_clean)} registros")
    return df_clean

def transform_productos(df: pd.DataFrame) -> pd.DataFrame:
    """Transforma la dimensión productos"""
    logger.info("🔄 Transformando dim_productos...")
    
    df_clean = df.copy()
    df_clean.columns = df_clean.columns.str.lower()
    
    # Inferir categorías basadas en nombre (ejemplo simplificado)
    def categorizar_producto(nombre):
        nombre_lower = str(nombre).lower()
        if any(word in nombre_lower for word in ['agua', 'refresco', 'zumo', 'café', 'bebida']):
            return 'Bebidas'
        elif any(word in nombre_lower for word in ['bocadillo', 'sandwich', 'hamburguesa', 'menú']):
            return 'Comida'
        elif any(word in nombre_lower for word in ['chips', 'galleta', 'chocolate', 'snack']):
            return 'Snacks'
        else:
            return 'Otros'
    
    df_clean['categoria'] = df_clean['nombre_producto'].apply(categorizar_producto)
    df_clean['es_activo'] = True
    
    # Renombrar para coincidir con schema
    df_clean = df_clean.rename(columns={'nombre': 'nombre_producto'})
    
    logger.info(f"  ✅ Productos transformados: {len(df_clean)} registros")
    return df_clean

def transform_rutas(df: pd.DataFrame) -> pd.DataFrame:
    """Transforma y enriquece la dimensión rutas"""
    logger.info("🔄 Transformando dim_rutas...")
    
    df_clean = df.copy()
    df_clean.columns = df_clean.columns.str.lower()
    
    # Extraer origen y destino de nombre_ruta (ej: "MAD-BCN" → origen="MAD", destino="BCN")
    df_clean['origen'] = df_clean['nombre_ruta'].str.split('-').str[0]
    df_clean['destino'] = df_clean['nombre_ruta'].str.split('-').str[1]
    
    # Tipo de transporte (inferir basado en código - simplificado)
    # Asumimos que tienes una columna o lógica para determinarlo
    # Aquí usamos un ejemplo simple
    df_clean['tipo_transporte'] = 'Avión'  # Cambiar según tu lógica
    
    # Distancia aproximada (placeholder - deberías tener datos reales)
    df_clean['distancia_km'] = None
    
    df_clean['es_activa'] = True
    
    logger.info(f"  ✅ Rutas transformadas: {len(df_clean)} registros")
    return df_clean

def transform_ventas(df: pd.DataFrame, incidencias_df: pd.DataFrame) -> pd.DataFrame:
    """Transforma la tabla de hechos de ventas"""
    logger.info("🔄 Transformando fact_ventas...")
    
    df_clean = df.copy()
    df_clean.columns = df_clean.columns.str.lower()
    
    # Calcular métricas derivadas
    df_clean['ingresos_total'] = df_clean['cantidad'] * df_clean['preciounit']
    
    # Calcular porcentaje objetivo (manejar división por cero)
    df_clean['porcentaje_objetivo'] = (
        (df_clean['ingresos_total'] / df_clean['objetivoventas']) * 100
    ).fillna(0)
    
    # Marcar si tuvo incidencia (join con incidencias por fecha + ruta)
    incidencias_keys = incidencias_df[['fecha', 'rutaid']].drop_duplicates()
    incidencias_keys['tiene_incidencia'] = True
    
    df_clean = df_clean.merge(
        incidencias_keys, 
        on=['fecha', 'rutaid'], 
        how='left'
    )
    df_clean['tiene_incidencia'] = df_clean['tiene_incidencia'].fillna(False)
    
    # Seleccionar columnas finales
    columnas_finales = [
        'venta_id', 'ticketid', 'fecha', 'rutaid', 'productoid',
        'fecha_ruta', 'cantidad', 'preciounit', 'ingresos_total',
        'pasajeros', 'objetivoventas', 'porcentaje_objetivo', 'tiene_incidencia'
    ]
    
    df_clean = df_clean[columnas_finales]
    
    logger.info(f"  ✅ Ventas transformadas: {len(df_clean)} registros")
    return df_clean

def transform_incidencias(df: pd.DataFrame) -> pd.DataFrame:
    """Transforma la tabla de hechos de incidencias"""
    logger.info("🔄 Transformando fact_incidencias...")
    
    df_clean = df.copy()
    df_clean.columns = df_clean.columns.str.lower()
    
    # Calcular métricas derivadas
    df_clean['es_critica'] = df_clean['severidad'] == 'Alta'
    df_clean['duracion_horas'] = df_clean['duracionmin'] / 60.0
    
    # Renombrar para coincidir con schema
    df_clean = df_clean.rename(columns={
        'tipoincidencia': 'tipo_incidencia',
        'duracionmin': 'duracion_minutos'
    })
    
    logger.info(f"  ✅ Incidencias transformadas: {len(df_clean)} registros")
    return df_clean

def load_dimension(conn, table_name: str, df: pd.DataFrame, conflict_column: str):
    """Carga datos en una tabla dimensión con UPSERT"""
    logger.info(f"💾 Cargando {table_name}...")
    
    cursor = conn.cursor()
    
    # Limpiar tabla primero (para simplificar - en producción usar UPSERT)
    cursor.execute(f"DELETE FROM analytics.{table_name}")
    
    # Preparar datos
    columns = df.columns.tolist()
    values = [tuple(row) for row in df.values]
    
    # Insertar
    placeholders = ','.join(['%s'] * len(columns))
    query = f"""
        INSERT INTO analytics.{table_name} ({','.join(columns)})
        VALUES ({placeholders})
    """
    
    execute_batch(cursor, query, values)
    conn.commit()
    
    logger.info(f"  ✅ {table_name}: {len(df)} registros cargados")

def load_fact_table(conn, table_name: str, df: pd.DataFrame, unique_columns: list):
    """Carga datos en tabla de hechos con manejo de duplicados"""
    logger.info(f"💾 Cargando {table_name}...")
    
    cursor = conn.cursor()
    
    # Limpiar tabla primero (alternativa: usar UPSERT con ON CONFLICT)
    cursor.execute(f"DELETE FROM analytics.{table_name}")
    
    # Preparar datos
    columns = [col for col in df.columns if col != 'incidencia_id' and col != 'venta_id']
    values = [tuple(row[columns]) for _, row in df.iterrows()]
    
    # Insertar
    placeholders = ','.join(['%s'] * len(columns))
    query = f"""
        INSERT INTO analytics.{table_name} ({','.join(columns)})
        VALUES ({placeholders})
    """
    
    execute_batch(cursor, query, values, page_size=500)
    conn.commit()
    
    logger.info(f"  ✅ {table_name}: {len(df)} registros cargados")

def create_tipo_incidencia_catalog(conn, incidencias_df: pd.DataFrame):
    """Crea catálogo de tipos de incidencia"""
    logger.info("📋 Creando catálogo dim_tipo_incidencia...")
    
    # Extraer tipos únicos
    tipos = incidencias_df['tipo_incidencia'].unique()
    
    # Crear DataFrame con categorías (simplificado)
    catalog = []
    for tipo in tipos:
        categoria = 'Operacional'  # Simplificado - personalizar según necesidad
        criticidad = 'Media'
        catalog.append({
            'tipo_incidencia': tipo,
            'categoria': categoria,
            'nivel_criticidad': criticidad,
            'descripcion': f'Incidencia de tipo {tipo}'
        })
    
    df_catalog = pd.DataFrame(catalog)
    load_dimension(conn, 'dim_tipo_incidencia', df_catalog, 'tipo_incidencia')

# =====================================================
# PROCESO ETL PRINCIPAL
# =====================================================

def run_etl():
    """Ejecuta el proceso ETL completo"""
    start_time = datetime.now()
    logger.info("=" * 60)
    logger.info("🚀 INICIANDO ETL PIPELINE")
    logger.info("=" * 60)
    
    try:
        # 1. CONECTAR
        conn = get_connection()
        
        # 2. EXTRACT
        raw_data = extract_raw_data(conn)
        
        # 3. TRANSFORM
        logger.info("\n🔄 FASE DE TRANSFORMACIÓN")
        logger.info("-" * 60)
        
        dim_calendario = transform_calendario(raw_data['calendario'])
        dim_productos = transform_productos(raw_data['productos'])
        dim_rutas = transform_rutas(raw_data['rutas'])
        
        # Transformar hechos (incidencias primero para usar en ventas)
        fact_incidencias = transform_incidencias(raw_data['incidencias'])
        fact_ventas = transform_ventas(raw_data['ventas'], raw_data['incidencias'])
        
        # 4. LOAD
        logger.info("\n💾 FASE DE CARGA")
        logger.info("-" * 60)
        
        # Cargar dimensiones primero
        load_dimension(conn, 'dim_calendario', dim_calendario, 'fecha')
        load_dimension(conn, 'dim_productos', dim_productos, 'productoid')
        load_dimension(conn, 'dim_rutas', dim_rutas, 'rutaid')
        create_tipo_incidencia_catalog(conn, fact_incidencias)
        
        # Cargar hechos
        load_fact_table(conn, 'fact_incidencias', fact_incidencias, ['incidenciaid'])
        load_fact_table(conn, 'fact_ventas', fact_ventas, ['ticketid', 'fecha_ruta', 'productoid'])
        
        # 5. CERRAR CONEXIÓN
        conn.close()
        
        # 6. RESUMEN
        duration = (datetime.now() - start_time).total_seconds()
        logger.info("\n" + "=" * 60)
        logger.info("✅ ETL COMPLETADO EXITOSAMENTE")
        logger.info(f"⏱️  Duración: {duration:.2f} segundos")
        logger.info("=" * 60)
        logger.info(f"📊 Registros procesados:")
        logger.info(f"   - Calendario: {len(dim_calendario)}")
        logger.info(f"   - Productos: {len(dim_productos)}")
        logger.info(f"   - Rutas: {len(dim_rutas)}")
        logger.info(f"   - Ventas: {len(fact_ventas)}")
        logger.info(f"   - Incidencias: {len(fact_incidencias)}")
        logger.info("=" * 60)
        
        return True
        
    except Exception as e:
        logger.error(f"\n❌ ERROR EN ETL: {e}")
        logger.exception("Detalles del error:")
        return False

# =====================================================
# EJECUTAR
# =====================================================

if __name__ == "__main__":
    success = run_etl()
    sys.exit(0 if success else 1)
