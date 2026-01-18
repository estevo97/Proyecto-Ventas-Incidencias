# Resumen de correlación e impacto. 

## Resumen ejecutivo
Este .md analiza la relación estadística entre las incidencias operacionales y los ingresos de ventas.

## Objetivo
- Calcular correlación entre número de incidencias e ingresos por día
- Comparar ingresos en días CON vs SIN incidencias
- Analizar impacto por tipo y severidad de incidencia
- Cuantificar el efecto económico de las incidencias

## Análisis de correlación

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

Ejecutar los tests en el notebook y añadir los resultados numéricos (estadísticos, p‑values) y la conclusión aquí.

---

Queremos determinar si hay diferencia significativa entre la media de ingresos en días con incidencias respecto a días sin incidencias. Si calculamos la media, obtenemos un resultado sorprendente puesto que se obtienen en promedio unos ingresos un 1.63 % superiores en los días en los  que hay incidencias. 

Aún con todo, queremos ver si existen estas diferencias significativas. Como tenemos dos muestras contínuas con media y varianza similar e independientes, usaremos el estadítico T para muestras independientes. Como referencia, también aplicaremos Mann-Whitney.

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