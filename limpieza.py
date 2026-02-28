import pandas as pd
import numpy as np


def limpieza_avanzada(df: pd.DataFrame) -> pd.DataFrame:

    df = df.copy()

    print("1️⃣ Eliminando duplicados...")
    df = df.drop_duplicates()

    print("2️⃣ Eliminando registros sin huéspedes...")
    df = df[(df['adults'] + df['children'].fillna(0) + df['babies']) > 0]

    print("3️⃣ Imputación de nulos...")

    # children
    df['children'] = df['children'].fillna(df['children'].median())

    # country
    df['country'] = df['country'].fillna("Unknown")

    # variables binarias antes de imputar
    df['has_agent'] = df['agent'].notna().astype(int)
    df['has_company'] = df['company'].notna().astype(int)

    # ya no necesitamos IDs
    df = df.drop(columns=['agent', 'company'])

    print("4️⃣ Feature engineering...")

    df['total_guests'] = df['adults'] + df['children'] + df['babies']
    df['total_nights'] = df['stays_in_weekend_nights'] + df['stays_in_week_nights']
    df['is_family'] = ((df['children'] + df['babies']) > 0).astype(int)

    # Temporada alta (jun-ago)
    df['high_season'] = df['arrival_date_month'].isin(
        ['June', 'July', 'August']
    ).astype(int)

    print("5️⃣ Tratamiento de outliers (IQR)...")

    columnas_outliers = [
        'adr',
        'lead_time',
        'stays_in_weekend_nights',
        'stays_in_week_nights'
    ]

    for col in columnas_outliers:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1

        lim_inf = Q1 - 1.5 * IQR
        lim_sup = Q3 + 1.5 * IQR

        df[col] = df[col].clip(lim_inf, lim_sup)

    print("6️⃣ Eliminando columnas con data leakage...")

    if 'reservation_status_date' in df.columns:
        df = df.drop(columns=['reservation_status_date'])

    print("7️⃣ Optimización de tipos...")

    categoricas = [
        'hotel',
        'arrival_date_month',
        'meal',
        'market_segment',
        'distribution_channel',
        'reserved_room_type',
        'assigned_room_type',
        'deposit_type',
        'customer_type'
    ]

    for col in categoricas:
        if col in df.columns:
            df[col] = df[col].astype('category')

    print("✅ Limpieza avanzada completada")
    print(f"Dimensión final: {df.shape}")

    return df