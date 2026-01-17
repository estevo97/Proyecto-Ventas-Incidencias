# Resumen de correlación e impacto. 

## Resumen ejecutivo
Breve síntesis (2–3 frases) con la conclusión principal.

## Objetivo
Explicar qué se buscó con el análisis de correlación_impacto.

## Metodología
- Datos usados: archivo(s) y fecha.
- Métrica de correlación: Pearson / Spearman / etc.
- Cómo se midió "impacto" (definición).

## Hallazgos principales
- Variable A vs Variable B: correlación X.XX — interpretación (p. ej., fuerte positiva).
- Variable C vs Variable D: correlación Y.YY — interpretación.
(Pegar aquí las top 5 correlaciones relevantes con sus valores y significancia.)

## Impacto/Interpretación
- Qué implican estos hallazgos para el negocio/operación.
- Riesgos/limitaciones (sesgos, tamaño muestral, variables confusoras).

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