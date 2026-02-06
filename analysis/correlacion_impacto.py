"""
=====================================================
ANÁLISIS IMPACTO INCIDENCIAS → INGRESOS
=====================================================
Script reproducible (sin notebook) que:
- Carga CSV procesados
- Calcula métricas y tests estadísticos
- Genera figuras
- Escribe insights.md

Uso:
    python correlacion_impacto.py
"""

from __future__ import annotations

import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pointbiserialr, spearmanr, ttest_ind, mannwhitneyu
import scipy.stats as stats

warnings.filterwarnings("ignore")

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR.parent / "data" / "processed"
IMAGES_DIR = BASE_DIR.parent / "images"
INSIGHTS_PATH = BASE_DIR / "insights.md"

VENTAS_PATH = DATA_DIR / "ventas400_proc2.csv"
INCIDENCIAS_PATH = DATA_DIR / "incidencias_proc2.csv"

sns.set_style("whitegrid")
plt.rcParams["figure.figsize"] = (12, 6)

# porcentaje de diferencia segura, evitando division por cero
def safe_pct(diff: float, base: float) -> float:
    if base == 0 or np.isnan(base):
        return 0.0
    return (diff / base) * 100


def format_eur(value: float) -> str:
    return f"€{value:,.2f}"

# crea la carpeta de imagenes si no existe
def ensure_dirs() -> None:
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)

# elimina espacios en blanco al principio y al final de los nombres de las columnas
def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = [c.strip() for c in df.columns]
    return df


# cambia el nombre de algunas columnas si vienen en minusculas y cambia el formato de fecha a datatime
def load_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    ventas = normalize_columns(pd.read_csv(VENTAS_PATH))
    incidencias = normalize_columns(pd.read_csv(INCIDENCIAS_PATH))

    # Normalizar columnas (soporta CSV con nombres en minúsculas desde PostgreSQL)
    ventas_rename = {
        "fecha": "Fecha",
        "ticketid": "TicketID",
        "ingresos_total": "Suma de IngresosFila",
    }
    incidencias_rename = {
        "fecha": "Fecha",
        "incidenciaid": "IncidenciaID",
        "duracionmin": "Suma de DuracionMin",
        "tipoincidencia": "TipoIncidencia",
        "severidad": "Severidad",
    }

    ventas = ventas.rename(columns={k: v for k, v in ventas_rename.items() if k in ventas.columns})
    incidencias = incidencias.rename(columns={k: v for k, v in incidencias_rename.items() if k in incidencias.columns})

    ventas["Fecha"] = pd.to_datetime(ventas["Fecha"])
    incidencias["Fecha"] = pd.to_datetime(incidencias["Fecha"])

    return ventas, incidencias

# creacion de la tabla df_diario que recopila el total de ingresos por dia y mergea la nueva data reciente con la anterior.
def build_daily_table(ventas: pd.DataFrame, incidencias: pd.DataFrame) -> pd.DataFrame:
    ventas_diarias = (
        ventas.groupby("Fecha")
        .agg({"Suma de IngresosFila": "sum", "TicketID": pd.Series.nunique})
        .rename(columns={"Suma de IngresosFila": "Ingresos", "TicketID": "Tickets"})
        .reset_index()
    )

    incidencias_diarias = (
        incidencias.groupby("Fecha")
        .agg({"IncidenciaID": "count", "Suma de DuracionMin": "sum"})
        .rename(columns={"IncidenciaID": "NumIncidencias"})
        .reset_index()
    )

    df_diario = ventas_diarias.merge(incidencias_diarias, on="Fecha", how="left")
    df_diario["NumIncidencias"] = df_diario["NumIncidencias"].fillna(0)
    df_diario["Suma de DuracionMin"] = df_diario["Suma de DuracionMin"].fillna(0)
    df_diario["TieneIncidencia"] = (df_diario["NumIncidencias"] > 0).astype(int)

    return df_diario

# Tabla de correlaciones entre variables cuantitativas. Se guarda como imagen en carpeta images.
def plot_correlation_heatmap(df_diario: pd.DataFrame) -> None:
    corr = df_diario[["Ingresos", "Tickets", "NumIncidencias", "Suma de DuracionMin", "Fecha"]].corr()
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr, annot=True, cmap="coolwarm", center=0, fmt=".3f", square=True, linewidths=1)
    plt.title("Matriz de Correlaciones", fontsize=16, fontweight="bold")
    plt.tight_layout()
    plt.savefig(IMAGES_DIR / "matriz_correlaciones.jpg", dpi=300, bbox_inches="tight", facecolor=plt.gcf().get_facecolor())
    plt.close()

# Gráfico de dispersión entre número de incidencias e ingresos, con línea de regresión. 
def plot_scatter_incidencias(df_diario: pd.DataFrame) -> None:
    x = df_diario["NumIncidencias"]
    y = df_diario["Ingresos"]
    mask = x.notnull() & y.notnull()

    slope, intercept, r_value, p_value, std_err = stats.linregress(x[mask], y[mask])

    plt.figure(figsize=(10, 5))
    plt.scatter(x, y, alpha=0.6, edgecolor="k")
    xx = np.linspace(x.min(), x.max(), 100)
    plt.plot(xx, intercept + slope * xx, color="red", linewidth=2, label=f"Regresión (r={r_value:.3f})")
    plt.title(f"Correlación Incidencias vs Ingresos (r={r_value:.3f})")
    plt.xlabel("Número de Incidencias por Día")
    plt.ylabel("Ingresos Totales (€)")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(IMAGES_DIR / "correlacion_incidencias_ingresos.jpg", dpi=300, bbox_inches="tight", facecolor=plt.gcf().get_facecolor())
    plt.close()

# Gráfico de barras comparando ingresos medios en días con incidencias vs sin incidencias.
def plot_bar_contra_sin(ingresos_con: pd.Series, ingresos_sin: pd.Series) -> None:
    fig, ax = plt.subplots(figsize=(8, 5))
    data_plot = pd.DataFrame(
        {
            "Tipo": ["Con Incidencias", "Sin Incidencias"],
            "Ingresos Medios": [ingresos_con.mean(), ingresos_sin.mean()],
        }
    )
    sns.barplot(data=data_plot, x="Tipo", y="Ingresos Medios", palette=["#4c72b0", "#dd8452"], ax=ax)
    ax.set_title("Ingresos Medios: Días CON vs SIN Incidencias")
    ax.set_ylabel("Ingresos Medios (€)")
    ax.set_xlabel("")
    plt.savefig(IMAGES_DIR / "BARPLOT_distribucion_ingresos_con_vs_sin_incidencias.jpg", dpi=300, bbox_inches="tight", facecolor=plt.gcf().get_facecolor())
    plt.close()

# Gráfico de boxplot comparando la distribución de ingresos en días con incidencias vs sin incidencias.
def plot_box_contra_sin(df_diario: pd.DataFrame) -> None:
    df_comp = df_diario.copy()
    df_comp["Categoría"] = df_comp["TieneIncidencia"].map({0: "SIN Incidencias", 1: "CON Incidencias"})

    plt.figure(figsize=(8, 6))
    ax = sns.boxplot(x="Categoría", y="Ingresos", data=df_comp, palette=["#4c72b0", "#dd8452"])
    ax.set_title("Distribución de Ingresos: Días CON vs SIN Incidencias")
    ax.set_ylabel("Ingresos Totales (€)")
    ax.set_xlabel("")
    plt.grid(alpha=0.2, axis="y")
    plt.tight_layout()
    plt.savefig(IMAGES_DIR / "distribucion_ingresos_con_vs_sin_incidencias.jpg", dpi=300, bbox_inches="tight", facecolor=plt.gcf().get_facecolor())
    plt.close()

# Gráfico de barras comparando ingresos medios por tipo de incidencia.
def plot_tipo_incidencia(impacto_tipo: pd.DataFrame) -> None:
    impacto_tipo_plot = impacto_tipo.reset_index()
    fig, ax = plt.subplots(figsize=(10, 5))
    colors = ["#4c72b0", "#dd8452", "#55a868", "#c44e52", "#8172b2"]
    bars = ax.bar(
        impacto_tipo_plot["TipoIncidencia"],
        impacto_tipo_plot["Ingreso_Medio"],
        color=colors[: len(impacto_tipo_plot)],
    )

    for rect in bars:
        h = rect.get_height()
        ax.annotate(
            f"€{h:,.0f}",
            xy=(rect.get_x() + rect.get_width() / 2, h),
            xytext=(0, 6),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=9,
        )

    ax.grid(False)
    for spine in ax.spines.values():
        spine.set_visible(False)

    ax.set_title("Ingreso Medio por Tipo de Incidencia")
    ax.set_ylabel("Ingreso Medio (€)")
    ax.set_xlabel("")
    ax.set_ylim(0, 1300)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(IMAGES_DIR / "ingreso_medio_por_tipo_incidencia.jpg", dpi=300, bbox_inches="tight", facecolor=plt.gcf().get_facecolor())
    plt.close()

# Gráfico de barras comparando ingresos medios por severidad de la incidencia.
def plot_severidad(impacto_severidad: pd.DataFrame) -> None:
    impacto_sev_plot = impacto_severidad.reset_index()
    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor("#f0f0f0")
    colors = ["#4c72b0", "#dd8452", "#55a868"]
    bars = ax.bar(
        impacto_sev_plot["Severidad"],
        impacto_sev_plot["Ingreso_Medio"],
        color=colors[: len(impacto_sev_plot)],
    )

    ax.grid(False)
    for spine in ax.spines.values():
        spine.set_visible(False)

    ax.set_title("Ingreso Medio por Severidad de la incidencia")
    ax.set_xlabel("")
    ax.set_ylim(0, 1300)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(IMAGES_DIR / "ingreso_medio_por_severidad_incidencia.jpg", dpi=300, bbox_inches="tight", facecolor=plt.gcf().get_facecolor())
    plt.close()

# Construcción del markdown con insights, resultados y recomendaciones. Se guarda como insights.md en la carpeta analysis.
def build_insights_markdown(
    df_diario: pd.DataFrame,
    corr_pbis: float,
    pvalue_pbis: float,
    corr_sper: float,
    pvalue_sper: float,
    ingresos_con: pd.Series,
    ingresos_sin: pd.Series,
    t_stat: float,
    t_pvalue: float,
    u_stat: float,
    u_pvalue: float,
    impacto_tipo: pd.DataFrame,
    impacto_severidad: pd.DataFrame,
) -> str:
    diferencia = ingresos_con.mean() - ingresos_sin.mean()
    porcentaje = safe_pct(diferencia, ingresos_sin.mean())

    if pvalue_pbis < 0.05:
        conclusion_corr = "**Significativa** — hay evidencia de correlación entre incidencias e ingresos (p < 0.05)."
        correlacion_txt = "La variable incidencias influye de manera significativa sobre los ingresos."
    else:
        conclusion_corr = "**No significativa** — no hay evidencia de correlación entre incidencias e ingresos (p ≥ 0.05)."
        correlacion_txt = "La variable incidencias NO influye de manera significativa sobre los ingresos."

    if t_pvalue < 0.05:
        conclusion_ttest = "✓ Rechazamos H0 (p < 0.05). Existe diferencia significativa."
        impacto_txt = "Las incidencias SÍ tienen impacto medible en ingresos."
    else:
        conclusion_ttest = "✗ No rechazamos H0 (p ≥ 0.05). No hay evidencia de diferencia significativa."
        impacto_txt = "No hay evidencia suficiente de impacto."

    tipo_peor = impacto_tipo.index[0] if len(impacto_tipo) > 0 else "N/A"
    ingreso_peor = impacto_tipo.iloc[0]["Ingreso_Medio"] if len(impacto_tipo) > 0 else np.nan

    sev_peor = impacto_severidad.index[0] if len(impacto_severidad) > 0 else "N/A"
    ingreso_sev = impacto_severidad.iloc[0]["Ingreso_Medio"] if len(impacto_severidad) > 0 else np.nan

    resumen_table = df_diario.head(5).copy()
    resumen_table["Fecha"] = resumen_table["Fecha"].dt.date

    period_min = df_diario["Fecha"].min().date()
    period_max = df_diario["Fecha"].max().date()
    total_dias = len(df_diario)
    dias_con_inc = df_diario["TieneIncidencia"].sum()
    total_incidencias = df_diario["NumIncidencias"].sum()
    pct_dias_inc = (dias_con_inc / total_dias) * 100 if total_dias else 0

    total_ingresos_con = df_diario[df_diario["TieneIncidencia"] == 1]["Ingresos"].sum()
    total_ingresos_sin = df_diario[df_diario["TieneIncidencia"] == 0]["Ingresos"].sum()

    lines = []
    lines.append("# Análisis del impacto de las Incidencias sobre los Ingresos\n")
    lines.append("## Resumen ejecutivo")
    lines.append("Este .md analiza la relación estadística entre las incidencias operacionales y los ingresos de ventas.\n")

    lines.append("## Objetivo")
    lines.append("- Determinar si existe correlación entre número de incidencias e ingresos por día.")
    lines.append("- Determinar si existe diferencia estadística en ingresos en días CON vs SIN incidencias.")
    lines.append("- Desglosar las Incidencias por tipo y por grado de severidad y ver si se encuentran diferencias entre las categorías.")
    lines.append("- Cuantificar, si es posible, el efecto económico de las incidencias.\n")

    lines.append("Para lograr los objetivos necesitamos centralizar los datos en una única tabla. Creamos una tabla con los datos de ingresos e incidencias agregados por día. La tabla es la siguiente:\n")

    lines.append(resumen_table.to_markdown(index=False))
    lines.append("\n## Heatmap de Correlaciones")
    lines.append("Antes de empezar con el análisis, hacemos una matriz de correlaciones para las siguientes covariables: Ingresos, Tickets, NumIncidencias, Suma de DuracionMin. De este modo podemos hacernos una idea de qué correlaciones puede ser interesante estudiar.")
    lines.append("![Matriz correlaciones](../images/matriz_correlaciones.jpg)")

    lines.append("\n# ANÁLISIS")
    lines.append("\n## 1. INCIDENCIAS VS INGRESOS")
    lines.append("### Análisis de correlación")
    lines.append("Para determinar si hay correlación entre dos variables cuantitativas, lo primero es hacernos una idea visual enfrentándolas en una nube de puntos.")
    lines.append("![Correlación Incidencias vs Ingresos](../images/correlacion_incidencias_ingresos.jpg)")
    lines.append("\nSe observa que la variable Incidencia es binaria, tomando sólo 0 y 1 como valores. No se puede usar el coeficiente de correlación Pearson.")
    lines.append("\nUtilizaremos la prueba Point - biserial correlation y Spearman como referencia.")

    lines.append("\n### Resultados")
    lines.append("| Métrica | Valor |")
    lines.append("|---:|:---|")
    lines.append(f"| Point biserial correlation (r) | {corr_pbis:.4f} |")
    lines.append(f"| p-value (point biserial) | {pvalue_pbis:.4e} |")
    lines.append(f"| Spearman (rho) | {corr_sper:.4f} |")
    lines.append(f"| p-value (Spearman) | {pvalue_sper:.4e} |")
    lines.append("")
    lines.append(f"**📊 Conclusión:** {conclusion_corr}")
    lines.append("")
    lines.append(correlacion_txt)

    lines.append("\n---\n")
    lines.append("## 2. Días CON vs SIN Incidencias")
    lines.append("Queremos determinar si hay diferencia significativa entre la media de ingresos en días con incidencias respecto a días sin incidencias.")
    lines.append("\n![Barplot ingresos CON vs SIN incidencias](../images/BARPLOT_distribucion_ingresos_con_vs_sin_incidencias.jpg)")
    lines.append("\n### Comparación: Días CON vs SIN Incidencias")
    lines.append("")
    lines.append(f"- 📈 Días CON incidencias\n  - Media: {format_eur(ingresos_con.mean())}\n  - Desv. Est.: {format_eur(ingresos_con.std())}")
    lines.append("")
    lines.append(f"- 📉 Días SIN incidencias\n  - Media: {format_eur(ingresos_sin.mean())}\n  - Desv. Est.: {format_eur(ingresos_sin.std())}")
    lines.append("")
    lines.append("**💰 IMPACTO ECONÓMICO**")
    lines.append(f"- Diferencia media: **{format_eur(diferencia)} ({porcentaje:+.2f}%)**")
    lines.append(f"- Conclusión: {'✓ Los días CON incidencias generan MÁS ingresos (posible confusión)' if diferencia >= 0 else '⚠️ Los días CON incidencias generan MENOS ingresos'}")

    lines.append("\n### Prueba de Hipótesis: T-Test")
    lines.append("| Test | Estadístico | p‑value |")
    lines.append("|---|---:|---:|")
    lines.append(f"| T‑test (paramétrico) | t = {t_stat:.4f} | {t_pvalue:.4e} |")
    lines.append(f"| Mann–Whitney U (no param.) | U = {u_stat:.2f} | {u_pvalue:.4e} |")
    lines.append("")
    lines.append(f"**Conclusión:** {conclusion_ttest}")

    lines.append("\n---\n")
    lines.append("### Visualización: Box Plot Comparativo")
    lines.append("![Comparación ingresos CON vs SIN incidencias](../images/distribucion_ingresos_con_vs_sin_incidencias.jpg)")

    lines.append("\n## 3. Por TIPO de Incidencia")
    lines.append("### Prueba ANOVA")
    lines.append("Como tenemos la lista de ingresos para cada tipo de incidencia, aplicamos ANOVA para comparar más de dos clases.")
    lines.append("\n### Promedio de ingresos para cada tipo de incidencia")
    lines.append("![Promedio de ingresos para cada tipo de incidencia](../images/ingreso_medio_por_tipo_incidencia.jpg)")

    lines.append("\n## 4. Por SEVERIDAD")
    lines.append("### Ingresos promedio en función de la severidad de la incidencia")
    lines.append("![Promedio de ingresos por severidad de la incidencia](../images/ingreso_medio_por_severidad_incidencia.jpg)")

    lines.append("\n## RESUMEN Ejecutivo de Hallazgos")
    lines.append(impacto_txt)

    lines.append("\n---\n")
    lines.append("### 📊 Datos generales")
    lines.append("| Métrica | Valor |")
    lines.append("|---|---:|")
    lines.append(f"| Período analizado | {period_min} — {period_max} |")
    lines.append(f"| Total días | {total_dias} |")
    lines.append(f"| Días con incidencias | {dias_con_inc} ({pct_dias_inc:.1f}%) |")
    lines.append(f"| Total incidencias | {total_incidencias:.0f} |")

    lines.append("\n### 💰 Impacto económico")
    lines.append("| Métrica | Valor (promedio) |")
    lines.append("|---|---:|")
    lines.append(f"| Ingresos días CON incidencias | {format_eur(ingresos_con.mean())} |")
    lines.append(f"| Ingresos días SIN incidencias | {format_eur(ingresos_sin.mean())} |")
    lines.append(f"| Diferencia media diaria | **{format_eur(diferencia)} ({porcentaje:+.2f}%)** |")

    lines.append("\n### 📈 Correlación y significancia")
    lines.append("| Métrica | Valor |")
    lines.append("|---|---:|")
    lines.append(f"| Point biserial | {corr_pbis:.4f} (p = {pvalue_pbis:.4e}) |")
    lines.append(f"| Resultado pruebas | {impacto_txt} |")

    lines.append("\n### ⚠️ Tipo más problemático")
    lines.append(f"- {tipo_peor} — Ingreso medio: **{format_eur(ingreso_peor) if not np.isnan(ingreso_peor) else 'N/A'}**")

    lines.append("\n### 🎯 Severidad más crítica")
    lines.append(f"- {sev_peor} — Ingreso medio: **{format_eur(ingreso_sev) if not np.isnan(ingreso_sev) else 'N/A'}**")

    lines.append("\n---\n")
    lines.append("## Recomendaciones")
    lines.append("- Acción inmediata (p. ej., priorizar X, recopilar más datos Y, etc).")
    lines.append("- Experimentos/validaciones a realizar.")

    lines.append("\n## Próximos pasos")
    lines.append("- Lista corta de tareas siguientes (p. ej., probar modelo causal, análisis temporal).")

    lines.append("\n## Anexos")
    lines.append("- Código reproducible en `analysis/correlacion_impacto.py`.")

    return "\n".join(lines)

# Función principal que ejecuta todo el análisis, genera gráficos y escribe insights.md
def main() -> None:
    ensure_dirs()

    ventas, incidencias = load_data()

    df_diario = build_daily_table(ventas, incidencias)

    plot_correlation_heatmap(df_diario)
    plot_scatter_incidencias(df_diario)

    corr_pbis, pvalue_pbis = pointbiserialr(df_diario["NumIncidencias"], df_diario["Ingresos"])
    corr_sper, pvalue_sper = spearmanr(df_diario["NumIncidencias"], df_diario["Ingresos"])

    ingresos_con = df_diario[df_diario["TieneIncidencia"] == 1]["Ingresos"]
    ingresos_sin = df_diario[df_diario["TieneIncidencia"] == 0]["Ingresos"]

    plot_bar_contra_sin(ingresos_con, ingresos_sin)

    t_stat, t_pvalue = ttest_ind(ingresos_con, ingresos_sin)
    u_stat, u_pvalue = mannwhitneyu(ingresos_con, ingresos_sin, alternative="two-sided")

    plot_box_contra_sin(df_diario)

    df_tipo = incidencias.merge(df_diario[["Fecha", "Ingresos"]], on="Fecha", how="left")

    impacto_tipo = df_tipo.groupby("TipoIncidencia").agg(
        {
            "Ingresos": ["mean", "std", "count"],
            "Suma de DuracionMin": "mean",
        }
    ).round(2)
    impacto_tipo.columns = ["Ingreso_Medio", "Desv_Est", "Num_Casos", "Duracion_Media"]
    impacto_tipo = impacto_tipo.sort_values("Ingreso_Medio")

    if len(impacto_tipo) > 0:
        plot_tipo_incidencia(impacto_tipo)

    impacto_severidad = df_tipo.groupby("Severidad").agg(
        {
            "Ingresos": ["mean", "std", "count"],
            "Suma de DuracionMin": "mean",
        }
    ).round(2)
    impacto_severidad.columns = ["Ingreso_Medio", "Desv_Est", "Num_Casos", "Duracion_Media"]
    impacto_severidad = impacto_severidad.sort_values("Ingreso_Medio")

    if len(impacto_severidad) > 0:
        plot_severidad(impacto_severidad)

    insights_md = build_insights_markdown(
        df_diario=df_diario,
        corr_pbis=corr_pbis,
        pvalue_pbis=pvalue_pbis,
        corr_sper=corr_sper,
        pvalue_sper=pvalue_sper,
        ingresos_con=ingresos_con,
        ingresos_sin=ingresos_sin,
        t_stat=t_stat,
        t_pvalue=t_pvalue,
        u_stat=u_stat,
        u_pvalue=u_pvalue,
        impacto_tipo=impacto_tipo,
        impacto_severidad=impacto_severidad,
    )

    INSIGHTS_PATH.write_text(insights_md, encoding="utf-8")
    print(f"✅ insights.md actualizado en: {INSIGHTS_PATH}")


if __name__ == "__main__":
    main()
