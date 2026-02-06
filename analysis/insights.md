# Análisis del impacto de las Incidencias sobre los Ingresos

## Resumen ejecutivo
Este .md analiza la relación estadística entre las incidencias operacionales y los ingresos de ventas.

## Objetivo
- Determinar si existe correlación entre número de incidencias e ingresos por día.
- Determinar si existe diferencia estadística en ingresos en días CON vs SIN incidencias.
- Desglosar las Incidencias por tipo y por grado de severidad y ver si se encuentran diferencias entre las categorías.
- Cuantificar, si es posible, el efecto económico de las incidencias.

Para lograr los objetivos necesitamos centralizar los datos en una única tabla. Creamos una tabla con los datos de ingresos e incidencias agregados por día. La tabla es la siguiente:

| Fecha      |   Ingresos |   Tickets |   NumIncidencias |   Suma de DuracionMin |   TieneIncidencia |
|:-----------|-----------:|----------:|-----------------:|----------------------:|------------------:|
| 2024-01-01 |     705.91 |        34 |                0 |                     0 |                 0 |
| 2024-01-02 |    1201.25 |        50 |                0 |                     0 |                 0 |
| 2024-01-03 |     819.5  |        37 |                1 |                   148 |                 1 |
| 2024-01-04 |     980.48 |        42 |                0 |                     0 |                 0 |
| 2024-01-05 |     998.91 |        44 |                1 |                   106 |                 1 |

## Heatmap de Correlaciones
Antes de empezar con el análisis, hacemos una matriz de correlaciones para las siguientes covariables: Ingresos, Tickets, NumIncidencias, Suma de DuracionMin. De este modo podemos hacernos una idea de qué correlaciones puede ser interesante estudiar.
![Matriz correlaciones](../images/matriz_correlaciones.jpg)

# ANÁLISIS

## 1. INCIDENCIAS VS INGRESOS
### Análisis de correlación
Para determinar si hay correlación entre dos variables cuantitativas, lo primero es hacernos una idea visual enfrentándolas en una nube de puntos.
![Correlación Incidencias vs Ingresos](../images/correlacion_incidencias_ingresos.jpg)

Se observa que la variable Incidencia es binaria, tomando sólo 0 y 1 como valores. No se puede usar el coeficiente de correlación Pearson.

Utilizaremos la prueba Point - biserial correlation y Spearman como referencia.

### Resultados
| Métrica | Valor |
|---:|:---|
| Point biserial correlation (r) | 0.0738 |
| p-value (point biserial) | 4.8709e-01 |
| Spearman (rho) | 0.0860 |
| p-value (Spearman) | 4.1752e-01 |

**📊 Conclusión:** **No significativa** — no hay evidencia de correlación entre incidencias e ingresos (p ≥ 0.05).

La variable incidencias NO influye de manera significativa sobre los ingresos.

---

## 2. Días CON vs SIN Incidencias
Queremos determinar si hay diferencia significativa entre la media de ingresos en días con incidencias respecto a días sin incidencias.

![Barplot ingresos CON vs SIN incidencias](../images/BARPLOT_distribucion_ingresos_con_vs_sin_incidencias.jpg)

### Comparación: Días CON vs SIN Incidencias

- 📈 Días CON incidencias
  - Media: €908.32
  - Desv. Est.: €134.13

- 📉 Días SIN incidencias
  - Media: €886.57
  - Desv. Est.: €162.04

**💰 IMPACTO ECONÓMICO**
- Diferencia media: **€21.75 (+2.45%)**
- Conclusión: ✓ Los días CON incidencias generan MÁS ingresos (posible confusión)

### Prueba de Hipótesis: T-Test
| Test | Estadístico | p‑value |
|---|---:|---:|
| T‑test (paramétrico) | t = 0.6979 | 4.8709e-01 |
| Mann–Whitney U (no param.) | U = 1100.00 | 4.1678e-01 |

**Conclusión:** ✗ No rechazamos H0 (p ≥ 0.05). No hay evidencia de diferencia significativa.

---

### Visualización: Box Plot Comparativo
![Comparación ingresos CON vs SIN incidencias](../images/distribucion_ingresos_con_vs_sin_incidencias.jpg)

## 3. Por TIPO de Incidencia
### Prueba ANOVA
Como tenemos la lista de ingresos para cada tipo de incidencia, aplicamos ANOVA para comparar más de dos clases.

### Promedio de ingresos para cada tipo de incidencia
![Promedio de ingresos para cada tipo de incidencia](../images/ingreso_medio_por_tipo_incidencia.jpg)

## 4. Por SEVERIDAD
### Ingresos promedio en función de la severidad de la incidencia
![Promedio de ingresos por severidad de la incidencia](../images/ingreso_medio_por_severidad_incidencia.jpg)

## RESUMEN Ejecutivo de Hallazgos
No hay evidencia suficiente de impacto.

---

### 📊 Datos generales
| Métrica | Valor |
|---|---:|
| Período analizado | 2024-01-01 — 2024-03-31 |
| Total días | 91 |
| Días con incidencias | 54 (59.3%) |
| Total incidencias | 54 |

### 💰 Impacto económico
| Métrica | Valor (promedio) |
|---|---:|
| Ingresos días CON incidencias | €908.32 |
| Ingresos días SIN incidencias | €886.57 |
| Diferencia media diaria | **€21.75 (+2.45%)** |

### 📈 Correlación y significancia
| Métrica | Valor |
|---|---:|
| Point biserial | 0.0738 (p = 4.8709e-01) |
| Resultado pruebas | No hay evidencia suficiente de impacto. |

### ⚠️ Tipo más problemático
- Avería — Ingreso medio: **€894.68**

### 🎯 Severidad más crítica
- Baja — Ingreso medio: **€874.85**

---

## Recomendaciones
- Acción inmediata (p. ej., priorizar X, recopilar más datos Y, etc).
- Experimentos/validaciones a realizar.

## Próximos pasos
- Lista corta de tareas siguientes (p. ej., probar modelo causal, análisis temporal).

## Anexos
- Código reproducible en `analysis/correlacion_impacto.py`.