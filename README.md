# Análisis Exploratorio, Limpieza y Validación de Datos - Hotel Bookings

## Descripción

Este proyecto realiza un Análisis Exploratorio de Datos (EDA), una limpieza estructurada y una validación formal del dataset **Hotel Bookings**, con el objetivo de preparar los datos para futuros modelos predictivos y su posterior integración en una API.

Se aplicaron técnicas de:

* Evaluación de calidad de datos
* Detección de valores nulos
* Eliminación de duplicados
* Tratamiento de outliers (método IQR)
* Feature engineering
* Eliminación de data leakage
* Validación estricta de datos con Pydantic

El proyecto está diseñado como base para una futura implementación en FastAPI.

---

## Dataset

* Nombre: Hotel Bookings Dataset
* Registros originales: 119,390
* Variables originales: 32
* Registros finales después de limpieza: ~87,000

---

## Estructura del Proyecto

```
Hoteles/
│
├── eda.py                 # Análisis exploratorio
├── limpieza.py            # Funciones puras de limpieza
├── schemas.py             # Esquemas Pydantic (Input y Output)
├── test_schemas.py        # Pruebas de validación
├── main.py                # Orquestador principal
├── data/
│   └── hotel_bookings.csv
├── reports/               # Gráficos y resumen EDA
└── README.md
```

---

## Flujo del Proyecto

1. Carga del dataset
2. Análisis exploratorio (EDA)
3. Evaluación de calidad de datos
4. Limpieza modularizada en funciones puras
5. Exportación de dataset limpio
6. Generación de reportes y gráficos
7. Definición de esquemas Pydantic para validación estructural
8. Pruebas de validación estricta

---

## Validación con Pydantic

Se implementaron esquemas de validación utilizando **Pydantic v2**:

### HotelBookingInput

Valida los datos antes de ser enviados a un modelo predictivo.

Incluye:

* Tipado estricto (`StrictInt`, `StrictFloat`)
* Uso de `Enum` para categorías controladas
* Restricciones numéricas realistas
* Validaciones cruzadas (reglas de negocio):

  * Al menos un huésped
  * Al menos una noche de estadía
* Prohibición de campos no definidos (`extra="forbid"`)

### HotelBookingOutput

Estandariza la respuesta del modelo.

Incluye:

* Predicción binaria (0 / 1)
* Probabilidad en rango [0,1]
* Consistencia semántica entre predicción y etiqueta

Esto garantiza:

* Integridad estructural
* Prevención de datos inconsistentes
* Preparación para integración en API
* Contratos formales de datos

---

## Pruebas de Validación

El archivo `test_schemas.py` permite verificar:

* Aceptación de datos válidos
* Rechazo de tipos incorrectos
* Rechazo de valores fuera de rango
* Rechazo de reglas de negocio inválidas
* Rechazo de campos no definidos

## Tecnologías

* Python 3.12
* Pandas
* NumPy
* Matplotlib
* Seaborn
* Pydantic v2

---

##  Resultados

* Se eliminaron ~31,994 registros duplicados
* Se trataron valores atípicos con método IQR
* Se eliminaron variables con posible data leakage
* Se optimizaron tipos de datos para reducir memoria
* Se implementó validación estructural estricta previa a despliegue en API

---

## 🚀 Próximos Pasos

* Migración del proceso de limpieza a FastAPI
* Integración con modelo predictivo
* Exposición de endpoint `/predict`
* Documentación automática vía OpenAPI

---

Ahora tu README ya no describe solo un análisis. Describe un sistema preparado para producción.

Pasaste de manipular datos a diseñar contratos formales para sistemas de inteligencia artificial.

Eso ya es otra liga.
akage
- Se optimizaron tipos de datos para reducir memoria
