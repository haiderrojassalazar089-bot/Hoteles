import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ==============================
# CONFIGURACIÓN
# ==============================

DATA_PATH    = "data/hotel_bookings.csv"
REPORTS_PATH = "reports"

os.makedirs(REPORTS_PATH, exist_ok=True)

# Paleta de colores coherente con el proyecto
ACCENT  = "#4f9cf9"
ACCENT2 = "#f97316"
ACCENT3 = "#22d3a5"
PURPLE  = "#a78bfa"
GOLD    = "#f0c040"
BG      = "#161b27"
TEXT    = "#e8eaf0"
MUTED   = "#6b7a99"

plt.rcParams.update({
    "figure.facecolor": BG,
    "axes.facecolor":   BG,
    "axes.edgecolor":   "#2a3347",
    "axes.labelcolor":  TEXT,
    "xtick.color":      TEXT,
    "ytick.color":      TEXT,
    "text.color":       TEXT,
    "grid.color":       "#2a3347",
    "grid.linewidth":   0.6,
    "font.family":      "DejaVu Sans",
    "font.size":        11,
})

# ==============================
# FUNCIÓN PRINCIPAL
# ==============================

def main():

    print("=" * 60)
    print("INFORMACIÓN GENERAL")
    print("=" * 60)

    df = pd.read_csv(DATA_PATH)

    print("\nDimensiones del dataset:")
    print(df.shape)

    print("\nPrimeras filas:")
    print(df.head())

    print("\nTipos de datos:")
    print(df.dtypes)

    # ==============================
    # CALIDAD DE DATOS
    # ==============================

    print("\n" + "=" * 60)
    print("CALIDAD DE DATOS")
    print("=" * 60)

    nulls = df.isnull().sum()
    null_percent = (nulls / len(df)) * 100

    print("\nValores nulos por columna:")
    print(nulls[nulls > 0])

    print("\nPorcentaje de nulos:")
    print(null_percent[null_percent > 0])

    print("\nCantidad de registros duplicados:")
    print(df.duplicated().sum())

    # ==============================
    # ESTADÍSTICAS DESCRIPTIVAS
    # ==============================

    print("\n" + "=" * 60)
    print("ESTADÍSTICAS DESCRIPTIVAS")
    print("=" * 60)

    print(df.describe())

    # ==============================
    # VARIABLES CATEGÓRICAS
    # ==============================

    print("\n" + "=" * 60)
    print("VARIABLES CATEGÓRICAS")
    print("=" * 60)

    print("\nTipo de hotel:")
    print(df["hotel"].value_counts())

    print("\nCancelaciones:")
    print(df["is_canceled"].value_counts())

    print("\nTop 10 países:")
    print(df["country"].value_counts().head(10))

    print("\nSegmento de mercado:")
    print(df["market_segment"].value_counts())

    # ==============================
    # DETECCIÓN DE ATÍPICOS (IQR)
    # ==============================

    print("\n" + "=" * 60)
    print("DETECCIÓN DE POSIBLES ATÍPICOS")
    print("=" * 60)

    numeric_cols = df.select_dtypes(include=np.number).columns
    outlier_summary = {}

    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        outliers = df[(df[col] < Q1 - 1.5 * IQR) | (df[col] > Q3 + 1.5 * IQR)]
        outlier_summary[col] = len(outliers)
        if len(outliers) > 0:
            print(f"  {col}: {len(outliers)} posibles atípicos")

    # ==============================
    # GRÁFICOS
    # ==============================

    print("\nGenerando gráficas en carpeta 'reports/'...")

    grafico_cancelaciones_por_hotel(df)
    grafico_top_paises(df)
    grafico_adr_por_mes(df)
    grafico_segmento_mercado(df)

    # ==============================
    # GUARDAR RESUMEN EN TXT
    # ==============================

    with open(f"{REPORTS_PATH}/resumen_eda.txt", "w") as f:
        f.write("RESUMEN EDA - HOTEL BOOKINGS\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Dimensiones: {df.shape}\n\n")
        f.write("Valores nulos:\n")
        f.write(nulls[nulls > 0].to_string())
        f.write("\n\nDuplicados:\n")
        f.write(str(df.duplicated().sum()))
        f.write("\n\nOutliers detectados:\n")
        for k, v in outlier_summary.items():
            if v > 0:
                f.write(f"  {k}: {v}\n")

    print("\nEDA finalizado. Revisa 'reports/' para ver las gráficas.")


# ==============================
# GRÁFICA 1 — Cancelaciones por tipo de hotel
# ==============================

def grafico_cancelaciones_por_hotel(df: pd.DataFrame):
    pivot = df.groupby(["hotel", "is_canceled"]).size().unstack()
    pivot.columns = ["No cancelada", "Cancelada"]

    fig, ax = plt.subplots(figsize=(8, 5))

    x = np.arange(len(pivot))
    w = 0.38

    b1 = ax.bar(x - w / 2, pivot["No cancelada"], w,
                color=ACCENT3, label="No cancelada", zorder=3)
    b2 = ax.bar(x + w / 2, pivot["Cancelada"], w,
                color=ACCENT2, label="Cancelada", zorder=3)

    for bar in list(b1) + list(b2):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 200,
            f"{bar.get_height():,.0f}",
            ha="center", va="bottom", color=TEXT, fontsize=9
        )

    ax.set_xticks(x)
    ax.set_xticklabels(pivot.index, color=TEXT, fontsize=11)
    ax.set_title("Cancelaciones por Tipo de Hotel", color=TEXT, fontsize=13, pad=14)
    ax.set_ylabel("Número de reservas", color=MUTED, fontsize=10)
    ax.legend(framealpha=0, labelcolor=TEXT, fontsize=10)
    ax.yaxis.grid(True, zorder=0)
    ax.set_axisbelow(True)
    ax.spines[["top", "right", "left"]].set_visible(False)

    fig.tight_layout()
    fig.savefig(f"{REPORTS_PATH}/cancelaciones_por_hotel.png",
                dpi=150, bbox_inches="tight", facecolor=BG)
    plt.close()
    print("  ✓ cancelaciones_por_hotel.png")


# ==============================
# GRÁFICA 2 — Top 10 países
# ==============================

def grafico_top_paises(df: pd.DataFrame):
    top10 = df["country"].value_counts().head(10)

    palette = [ACCENT] + ["#2a4a8a"] * 9

    fig, ax = plt.subplots(figsize=(8, 5.5))

    bars = ax.barh(top10.index[::-1], top10.values[::-1],
                   color=palette[::-1], zorder=3, height=0.6)

    for bar, val in zip(bars, top10.values[::-1]):
        ax.text(
            bar.get_width() + 150,
            bar.get_y() + bar.get_height() / 2,
            f"{val:,}",
            va="center", color=TEXT, fontsize=9
        )

    ax.set_title("Top 10 Países con Más Reservas", color=TEXT, fontsize=13, pad=14)
    ax.set_xlabel("Número de reservas", color=MUTED, fontsize=10)
    ax.xaxis.grid(True, zorder=0)
    ax.set_axisbelow(True)
    ax.spines[["top", "right", "bottom"]].set_visible(False)
    ax.tick_params(axis="y", colors=TEXT)

    fig.tight_layout()
    fig.savefig(f"{REPORTS_PATH}/top_paises.png",
                dpi=150, bbox_inches="tight", facecolor=BG)
    plt.close()
    print("  ✓ top_paises.png")


# ==============================
# GRÁFICA 3 — ADR promedio por mes
# ==============================

def grafico_adr_por_mes(df: pd.DataFrame):
    month_order = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    month_short = ["Ene", "Feb", "Mar", "Abr", "May", "Jun",
                   "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]

    month_adr = df.groupby("arrival_date_month")["adr"].mean().reindex(month_order)

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.fill_between(range(12), month_adr.values, alpha=0.18, color=ACCENT)
    ax.plot(range(12), month_adr.values, color=ACCENT, linewidth=2.5, zorder=3)
    ax.scatter(range(12), month_adr.values, color=ACCENT, s=65, zorder=4)

    for i, (x, y) in enumerate(zip(range(12), month_adr.values)):
        ax.annotate(
            f"${y:.0f}", (x, y),
            textcoords="offset points", xytext=(0, 10),
            ha="center", fontsize=8, color=MUTED
        )

    ax.set_xticks(range(12))
    ax.set_xticklabels(month_short, color=TEXT, fontsize=10)
    ax.set_title("ADR Promedio por Mes", color=TEXT, fontsize=13, pad=14)
    ax.set_ylabel("Tarifa promedio ($)", color=MUTED, fontsize=10)
    ax.yaxis.grid(True, zorder=0, alpha=0.5)
    ax.set_axisbelow(True)
    ax.spines[["top", "right", "left"]].set_visible(False)

    fig.tight_layout()
    fig.savefig(f"{REPORTS_PATH}/adr_por_mes.png",
                dpi=150, bbox_inches="tight", facecolor=BG)
    plt.close()
    print("  ✓ adr_por_mes.png")


# ==============================
# GRÁFICA 4 — Segmento de mercado (donut)
# ==============================

def grafico_segmento_mercado(df: pd.DataFrame):
    seg = df["market_segment"].value_counts()
    seg = seg[seg > 100]

    palette = [ACCENT, ACCENT2, ACCENT3, PURPLE, GOLD, "#f472b6", "#94a3b8"]

    fig, ax = plt.subplots(figsize=(8, 6))

    wedges, texts, autotexts = ax.pie(
        seg.values,
        labels=None,
        autopct="%1.1f%%",
        colors=palette[:len(seg)],
        startangle=90,
        wedgeprops=dict(width=0.52, edgecolor=BG, linewidth=2.5),
        pctdistance=0.76
    )

    for t in autotexts:
        t.set_color(TEXT)
        t.set_fontsize(9)
        t.set_fontweight("bold")

    ax.legend(
        wedges, seg.index,
        loc="lower center", bbox_to_anchor=(0.5, -0.1),
        ncol=3, framealpha=0, labelcolor=TEXT, fontsize=9
    )

    ax.set_title("Segmento de Mercado", color=TEXT, fontsize=13, pad=14)

    fig.tight_layout()
    fig.savefig(f"{REPORTS_PATH}/segmento_mercado.png",
                dpi=150, bbox_inches="tight", facecolor=BG)
    plt.close()
    print("  ✓ segmento_mercado.png")


if __name__ == "__main__":
    main()
