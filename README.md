# 📊 Proyecto: Análisis de Ventas e Incidencias Operacionales

- EDA con datos de ingresos por venta de alimentos en sistemas de transporte (aviación y ferrocarril). 
- Análisis estadístico del impacto de las incidencias operacionales sobre tales ingresos. 
- Proyecto end-to-end que incluye generación de datos sintéticos realistas, dashboard interactivo en Power BI y análisis estadístico avanzado.

---

## 🎯 Objetivos del Proyecto

1. **Analizar el impacto** de las incidencias operacionales en los ingresos de ventas
2. **Identificar patrones** de tipos y severidades de incidencias más problemáticas
3. **Cuantificar económicamente** el efecto de días con vs sin incidencias
4. **Proveer insights accionables** para mejorar la operación y reducir pérdidas

---

## 📁 Estructura del Proyecto

```
Proyecto-Ventas-Incidencias/
│
├── data/
│   └── raw/
│       ├── Ventas_Realistas.csv        # Datos de ventas generados
│       └── Incidencias.csv             # Datos de incidencias generadas
│
├── scripts/
│   ├── generar_ventas_realistas.py     # Script generador de datos de ventas
│   └── generar_incidencias.py          # Script generador de incidencias
│
├── dashboard/
│   ├── dashboard_ventas_incidencias.pbix   # Dashboard Power BI (3 páginas)
│   └── dashboard_preview.pdf               # Vista previa en PDF
│
├── analysis/
│   ├── correlacion_impacto.ipynb       # Análisis estadístico completo
│   └── insights.md                      # Resumen de hallazgos clave
│
├── requirements.txt                     # Dependencias Python
├── .gitignore                          
└── README.md                           
```

---

## 📊 Datasets

#### ver Documentation

---

## 📈 Dashboard Power BI

El dashboard consta de **3 páginas principales:**

### Página 1: Resumen Ejecutivo
- **KPIs principales:**
- **Gráfico:** Evolución mensual Ingresos vs Objetivo
- **Hallazgos clave:**

Enlace al dashboard en hugging face: https://huggingface.co/spaces/estevoag/Proyecto-Ventas-Incidencias2

### Página 2: Análisis de Ventas


### Página 3: Análisis de Incidencias

**Segmentadores disponibles:**
- Mes
- Ruta
- Producto
- Tipo de Incidencia
- Tipo de Transporte (Aviación/Ferrocarril)

---

## 🔬 Análisis Estadístico

El notebook [`correlacion_impacto.ipynb`](analysis/correlacion_impacto.ipynb) incluye:

### 1. Análisis de Correlación
- **Pearson Correlation** entre incidencias e ingresos
- **Spearman Correlation** (no paramétrica)
- Scatter plot con regresión lineal
- Interpretación de significancia estadística

### 2. Comparación Días CON vs SIN Incidencias
- Pruebas de hipótesis:
  - **T-Test** (paramétrico)
  - **Mann-Whitney U** (no paramétrico)
- Box plots comparativos
- Cuantificación del impacto económico

### 3. Análisis por Tipo y Severidad
- Identificación de tipos más problemáticos
- Ingresos medios por severidad
- Duración promedio de incidencias

### 4. Visualizaciones Avanzadas
- Heatmap de correlaciones
- Gráficos interactivos con Plotly
- Resumen ejecutivo automatizado

---

## 📊 Principales Hallazgos

### 💰 Impacto Económico
- **Días SIN incidencias:** €30,000 de ingresos
- **Días CON incidencias:** €44,000 de ingresos
- **Diferencia:** +47% más ingresos en días CON incidencias*

> *Nota: Esto puede parecer contraintuitivo, pero se debe a que los días con más tráfico (y por tanto más ventas) también tienen mayor probabilidad de incidencias.

### ⚠️ Incidencias Críticas
1. **Más frecuente:** Problema TPV (31%)
2. **Mayor duración:** Terminal de pago (26%)
3. **Ruta más afectada:** BCN-PMI (14.32% de incidencias)

### 📈 Tendencias
- **14.75%** de los días tienen incidencias
- Las incidencias en aviación son más frecuentes que en ferrocarril
- Los ingresos por pasajero son mayores en aviación (€0.07 vs €0.06)

---


## 👤 Autor

**Estevo Arias García**
- GitHub: [@estevo97](https://github.com/estevo97)
- LinkedIn: [Estevo Arias García](https://https://www.linkedin.com/in/estevoariasgarcia/)

---

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la [MIT License](LICENSE).



