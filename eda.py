import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Para entornos sin interfaz gráfica
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ==============================
# CONFIGURACIÓN
# ==============================

DATA_PATH = "data/hotel_bookings.csv"
REPORTS_PATH = "reports"

os.makedirs(REPORTS_PATH, exist_ok=True)

# ==============================
# FUNCIÓN PRINCIPAL
# ==============================

def main():

    print("="*60)
    print("INFORMACIÓN GENERAL")
    print("="*60)

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

    print("\n" + "="*60)
    print("CALIDAD DE DATOS")
    print("="*60)

    nulls = df.isnull().sum()
    null_percent = (nulls / len(df)) * 100

    print("\nValores nulos por columna:")
    print(nulls)

    print("\nPorcentaje de nulos:")
    print(null_percent)

    print("\nCantidad de registros duplicados:")
    print(df.duplicated().sum())

    # ==============================
    # ESTADÍSTICAS DESCRIPTIVAS
    # ==============================

    print("\n" + "="*60)
    print("ESTADÍSTICAS DESCRIPTIVAS")
    print("="*60)

    print(df.describe())

    # ==============================
    # VARIABLES CATEGÓRICAS
    # ==============================

    print("\n" + "="*60)
    print("VARIABLES CATEGÓRICAS")
    print("="*60)

    print("\nTipo de hotel:")
    print(df['hotel'].value_counts())

    print("\nCancelaciones:")
    print(df['is_canceled'].value_counts())

    print("\nTop 10 países:")
    print(df['country'].value_counts().head(10))

    # ==============================
    # DETECCIÓN DE ATÍPICOS (IQR)
    # ==============================

    print("\n" + "="*60)
    print("DETECCIÓN DE POSIBLES ATÍPICOS")
    print("="*60)

    numeric_cols = df.select_dtypes(include=np.number).columns

    outlier_summary = {}

    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1

        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR

        outliers = df[(df[col] < lower) | (df[col] > upper)]
        outlier_summary[col] = len(outliers)

        print(f"{col}: {len(outliers)} posibles atípicos")

    # ==============================
    # GRÁFICOS (GUARDADOS EN REPORTS)
    # ==============================

    print("\nGenerando gráficos en carpeta 'reports/'...")

    # Cancelaciones
    plt.figure()
    df['is_canceled'].value_counts().plot(kind='bar')
    plt.title("Cancelaciones")
    plt.xlabel("Cancelado (0=No, 1=Sí)")
    plt.ylabel("Cantidad")
    plt.savefig(f"{REPORTS_PATH}/cancelaciones.png")
    plt.close()

    # Distribución ADR
    plt.figure()
    sns.histplot(df['adr'], bins=50)
    plt.title("Distribución ADR")
    plt.savefig(f"{REPORTS_PATH}/distribucion_adr.png")
    plt.close()

    # Lead time
    plt.figure()
    sns.histplot(df['lead_time'], bins=50)
    plt.title("Distribución Lead Time")
    plt.savefig(f"{REPORTS_PATH}/lead_time.png")
    plt.close()

    # Correlación
    plt.figure(figsize=(12, 8))
    sns.heatmap(df[numeric_cols].corr(), cmap="coolwarm")
    plt.title("Mapa de Correlación")
    plt.savefig(f"{REPORTS_PATH}/correlacion.png")
    plt.close()

    # ==============================
    # GUARDAR RESUMEN EN TXT
    # ==============================

    with open(f"{REPORTS_PATH}/resumen_eda.txt", "w") as f:
        f.write("RESUMEN EDA - HOTEL BOOKINGS\n")
        f.write("="*50 + "\n\n")
        f.write(f"Dimensiones: {df.shape}\n\n")
        f.write("Valores nulos:\n")
        f.write(nulls.to_string())
        f.write("\n\nDuplicados:\n")
        f.write(str(df.duplicated().sum()))
        f.write("\n\nOutliers:\n")
        for k, v in outlier_summary.items():
            f.write(f"{k}: {v}\n")

    print("\nEDA finalizado correctamente.")
    print("Revisa la carpeta 'reports/' para ver los gráficos y el resumen.")


if __name__ == "__main__":
    main()


