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

## 🚀 Instalación y Uso

### Requisitos Previos
- Python 3.8+
- Power BI Desktop (para visualizar dashboard)

### 1. Clonar el Repositorio
```bash
git clone https://github.com/tu-usuario/Proyecto-Ventas-Incidencias.git
cd Proyecto-Ventas-Incidencias
```

### 2. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 3. Generar Datos (Opcional)
Si quieres regenerar los datasets:

```bash
# Generar ventas
python scripts/generar_ventas_realistas.py

# Generar incidencias
python scripts/generar_incidencias.py
```

### 4. Ejecutar Análisis
```bash
# Abrir notebook de análisis
jupyter notebook analysis/correlacion_impacto.ipynb
```

### 5. Ver Dashboard
1. Abrir `dashboard/dashboard_ventas_incidencias.pbix` en Power BI Desktop
2. Refrescar datos si es necesario
3. Explorar las 3 páginas interactivas

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

## 🛠️ Tecnologías Utilizadas

| Tecnología | Uso |
|------------|-----|
| Python 3.11 | Generación de datos y análisis |
| Pandas | Manipulación de datos |
| NumPy | Cálculos numéricos |
| Matplotlib/Seaborn | Visualizaciones estáticas |
| Plotly | Visualizaciones interactivas |
| SciPy | Pruebas estadísticas |
| Power BI Desktop | Dashboard interactivo |
| Jupyter Notebook | Análisis exploratorio |

---

## 📝 Próximos Pasos

- [ ] Crear dashboard web interactivo con Streamlit
- [ ] Implementar modelos predictivos de incidencias
- [ ] Automatizar alertas por incidencias críticas
- [ ] Análisis de series temporales (ARIMA/Prophet)
- [ ] Integración con datos reales (APIs)

---

## 👤 Autor

**Tu Nombre**
- GitHub: [@tu-usuario](https://github.com/tu-usuario)
- LinkedIn: [Tu Perfil](https://linkedin.com/in/tu-perfil)

---

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la [MIT License](LICENSE).

---

## 🙏 Agradecimientos

Proyecto desarrollado como parte del portfolio de ciencia de datos y análisis de negocio.

---

**⭐ Si te resultó útil este proyecto, dale una estrella en GitHub!**
