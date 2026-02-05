import psycopg2
import pandas as pd
import time

# Reemplaza con tus credenciales de Railway
conn = psycopg2.connect(
    host="hopper.proxy.rlwy.net",
    port=57761,
    database="central_data",
    user="postgres",
    password="TU_PASSWORD_AQUI"  # Reemplaza esto
)

df = pd.read_csv(r'D:\OneDrive\Documentos\GitHub\Proyecto-Ventas-Incidencias\data\raw\Calendario.csv')

print(f"Importando {len(df)} filas...")

cursor = conn.cursor()
start = time.time()

for idx, row in df.iterrows():
    try:
        cursor.execute(
            """INSERT INTO public.calendario_raw 
               (fecha, anio, mesnum, mes, dia, diasemana, semanaiso, eslaborable) 
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
            (row['Fecha'], row['Anio'], row['MesNum'], row['Mes'], 
             row['Dia'], row['DiaSemana'], row['SemanaISO'], row['EsLaborable'])
        )
        if idx % 50 == 0:
            print(f"  {idx}/{len(df)} filas...")
    except Exception as e:
        print(f"Error en fila {idx}: {e}")
        conn.rollback()
        break

conn.commit()
cursor.close()
conn.close()

elapsed = time.time() - start
print(f"✓ Importación completada en {elapsed:.2f} segundos")
