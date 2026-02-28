#  Análisis Exploratorio y Limpieza de Datos - Hotel Bookings
##  Descripción

Este proyecto realiza un Análisis Exploratorio de Datos (EDA) y una limpieza
estructurada del dataset "Hotel Bookings", con el objetivo de preparar los
datos para futuros modelos predictivos.

Se aplicaron técnicas de:
- Evaluación de calidad de datos
- Detección de valores nulos
- Eliminación de duplicados
- Tratamiento de outliers (IQR)
- Feature engineering
- Eliminación de data leakage

## Dataset

- Nombre: Hotel Bookings Dataset
- Registros originales: 119,390
- Variables originales: 32
- Registros finales después de limpieza: ~87,000

## Estructura del Proyecto

Hoteles/
│
├── eda.py              # Análisis exploratorio
├── limpieza.py         # Funciones puras de limpieza
├── main.py             # Orquestador principal
├── data/
│   └── hotel_bookings.csv
├── reports/            # Gráficos y resumen EDA
└── README.md

## Flujo del Proyecto

1. Carga del dataset
2. Análisis exploratorio (EDA)
3. Evaluación de calidad de datos
4. Limpieza modularizada en funciones puras
5. Exportación de dataset limpio
6. Generación de reportes y gráficos

## Tecnologías

- Python 3
- Pandas
- NumPy
- Matplotlib
- Seaborn

## Resultados

- Se eliminaron ~31,994 registros duplicados
- Se trataron valores atípicos con método IQR
- Se eliminaron variables con posible data leakage
- Se optimizaron tipos de datos para reducir memoria