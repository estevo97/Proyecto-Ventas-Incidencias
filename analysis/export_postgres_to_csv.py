"""
=====================================================
EXPORTADOR PostgreSQL → CSV
=====================================================
Script que exporta datos desde PostgreSQL (Railway)
hacia archivos CSV locales en data/processed/

Uso:
    python export_postgres_to_csv.py

Autor: ETL System
Fecha: 2026-02-05
=====================================================
"""

import psycopg2
import pandas as pd
import os
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv(Path(__file__).parent.parent / '.env')

# =====================================================
# CONFIGURACIÓN
# =====================================================

DB_CONFIG = {
    'host': 'hopper.proxy.rlwy.net',
    'port': 57761,
    'database': 'central_data',
    'user': 'postgres',
    'password': os.getenv('POSTGRES_PASSWORD', 'TU_PASSWORD_AQUI')  # ⚠️ Usar variable de entorno
}

# Directorio de salida
OUTPUT_DIR = Path(__file__).parent.parent / 'data' / 'processed'

# Queries para exportar
QUERIES = {
    'ventas400_proc2.csv': """
        SELECT * FROM analytics.vw_ventas
        ORDER BY fecha
    """,
    'incidencias_proc2.csv': """
        SELECT * FROM public.incidencias_raw
        ORDER BY fecha, incidenciaid
    """
}

# =====================================================
# FUNCIONES
# =====================================================

def export_to_csv():
    """Exporta datos de PostgreSQL a CSV"""
    
    print("=" * 60)
    print("🚀 EXPORTANDO PostgreSQL → CSV")
    print("=" * 60)
    
    # Crear directorio si no existe
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Conectar a PostgreSQL
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        print(f"✅ Conexión establecida a {DB_CONFIG['host']}")
    except Exception as e:
        print(f"❌ Error conectando a PostgreSQL: {e}")
        print("\n💡 Asegúrate de configurar la variable de entorno:")
        print("   set POSTGRES_PASSWORD=tu_password")
        return
    
    # Exportar cada query
    total_exported = 0
    try:
        for filename, query in QUERIES.items():
            print(f"\n📥 Exportando: {filename}")
            
            # Ejecutar query y cargar en DataFrame
            df = pd.read_sql_query(query, conn)
            
            # Guardar CSV
            output_path = OUTPUT_DIR / filename
            df.to_csv(output_path, index=False, encoding='utf-8')
            
            print(f"   ✅ {len(df):,} registros exportados")
            print(f"   📁 {output_path}")
            total_exported += len(df)
        
        print("\n" + "=" * 60)
        print(f"✅ EXPORTACIÓN COMPLETADA")
        print(f"📊 Total registros: {total_exported:,}")
        print(f"📂 Ubicación: {OUTPUT_DIR}")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error durante exportación: {e}")
    finally:
        conn.close()

# =====================================================
# EJECUCIÓN
# =====================================================

if __name__ == '__main__':
    export_to_csv()
