# Análisis del impacto de las Incidencias sobre los Ingresos


## Resumen ejecutivo
Este .md analiza la relación estadística entre las incidencias operacionales y los ingresos de ventas.

## Objetivo
- Determinar si existe correlación entre número de incidencias e ingresos por día.
- Determinar si existe diferencia estadística en ingresos en días CON vs SIN incidencias.
- Desglosar las Incidencias por tipo y por grado de severidad y ver si se encuentran diferencias entre las categorías.
- Cuantificar, si es posible, el efecto económico de las incidencias.

## Análisis de correlación
![Correlación Incidencias vs Ingresos](../images/correlacion_incidencias_ingresos.jpg)
Para determinar si hay correlación entre dos variables cuantitativas, lo primero es enfrentarlas en una nube de puntos, siendo la Variable 1 el eje X y la Variable 2 el eje Y.

### Scatterplot. Correlación Ingresos e Incidencias

Se observa que la variable Incidencia es binaria, tomando sólo 0 y 1 como valores. No se puede usar el coeficiente de correlación Pearson.

Utilizaremos la prueba Point - biserial correlation, que es una variable de la prueba Pearson que se usa cuando una variable es continua y la otra binaria. También usaremos como referencia el test Spearman.

### Análisis de correlación — Incidencias vs Ingresos

| Métrica | Valor |
|---:|:---|
| Point biserial correlation (r) | 0.0475 |
| p-value (point biserial) | 6.5484e-01 |
| Spearman (rho) | 0.0788 |
| p-value (Spearman) | 4.5791e-01 |

**📊 Conclusión:** **No significativa** — no hay evidencia de correlación entre incidencias e ingresos (p ≥ 0.05).

---

## Comparación: Días CON vs SIN Incidencias

Queremos determinar si hay diferencia significativa entre la media de ingresos en días con incidencias respecto a días sin incidencias. Al calcular las medias observamos que, en promedio, los días con incidencias presentan un incremento del 1.63 %.

- Diseño: dos muestras independientes (Ingresos en días CON vs SIN incidencias).  
- Tests:  
  - T-test independiente (asumiendo medias y varianzas similares).  
  - Mann–Whitney U (prueba no paramétrica como contraste).  
- Hipótesis:  
  - H0: no hay diferencia en la media de ingresos entre ambos grupos.  
  - H1: existe diferencia en la media de ingresos.

---

Aún con todo, queremos ver si existen estas diferencias significativas. Como tenemos dos muestras contínuas con media y varianza similar e independientes, usaremos el estadítico T para muestras independientes. Como referencia, también aplicaremos Mann-Whitney.

### Prueba de Hipótesis: T-Test

| Test | Estadístico | p‑value |
|---|---:|---:|
| T‑test (paramétrico) | t = 0.4486 | 6.5484e-01 |
| Mann–Whitney U (no param.) | U = 1091.50 | 4.5727e-01 |

**Conclusión:** ✗ No rechazamos H0 (p ≥ 0.05). No hay evidencia de diferencia significativa en la media de ingresos entre días CON y SIN incidencias.

Como vemos, ese 1.63% de diferencia no es suficiente para afirmar que haya diferencia significativa entre los días con incidencias y los días en los que no la hay. Podemos decir, pues, que las incidencias no afectan, en el global de los datos, a los ingresos promedio. Podríamos, en un futuro, desglosar en categorías estos datos y aplicar, para cada caso, la prueba T. De este modo podríamos encontrar algún contexto de filtro (por ejemplo, cancelaciones en ferrocarriles en un mes donde haya habido inclemencias climáticas) en donde sí se noten estas diferencias de forma significativa.

---

### Visualización: Box Plot Comparativo

## Análisis por Tipo de Incidencia

### Prueba ANOVA

Como tenemos la lista de ingresos para cada tipo de incidencia, vamos a ver si hay diferencias significativas entre ellas. Para eso, utilizaremos la prueba ANOVA, ya que tenemos que comparar más de dos clases de datos.

Los resultados no son significativos, por lo que no podemos afirmar que haya diferencias significativas en los ingresos obtenidos en cada uno de los casos en los que hay una incidencia.

### Promedio de ingresos para cada tipo de incidencia

Como vemos, los promedios en ingresos para cada tipo de incidencia son muy similares

## Análisis por Severidad

### Análisis ANOVA de ingresos en función de la severidad de la incidencia

Los resultados siguen sin ser significativos, aunque el p-valor es más bajo que cuando no se tiene en cuenta la severidad de las incidencias.

### Ingresos promedio en función de la severidad de la incidencia

Resulta llamativo que los ingresos más bajos se obtengan cuando la severidad es más baja y que los más altos se den con severidad media.

## Heatmap de Correlaciones

## Resumen Ejecutivo de Hallazgos

## Recomendaciones
- Acción inmediata (p. ej., priorizar X, recopilar más datos Y).
- Experimentos/validaciones a realizar.

## Reproducibilidad y visuales
- Las figuras clave están en `analysis/figures/` (p. ej. `fig_corr_matrix.png`, `fig_top_pairs.png`).
- Nota: los prints en notebooks pueden no verse en GitHub si los outputs no se guardan; por eso se recomienda exportar las figuras.

## Próximos pasos
- Lista corta de tareas siguientes (p. ej., probar modelo causal, análisis temporal).

## Anexos
- Código para reproducir (o enlace al notebook `notebooks/correlacion_impacto.ipynb`).