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