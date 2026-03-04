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

 Implementación de la API (FastAPI)

Como extensión natural del proceso de análisis, limpieza y validación de datos, el proyecto incorpora una API desarrollada con FastAPI, cuyo objetivo es automatizar y exponer el pipeline de EDA y limpieza de datos de manera estructurada y reutilizable.

Esta API está diseñada como base para una futura etapa de inferencia y despliegue de modelos predictivos, asegurando desde el inicio contratos de datos claros y validaciones estrictas.

 Objetivo de la API

La API permite:

* Ejecutar de forma automática el análisis exploratorio de datos (EDA)

* Aplicar el proceso completo de limpieza avanzada

* Generar y persistir un dataset limpio

* Consultar el estado del proceso de limpieza

* Servir como capa intermedia entre datos crudos y modelos predictivos

 Construcción de la API

La API fue construida siguiendo principios de diseño limpio y modular:

* FastAPI como framework principal

* Pydantic para contratos de datos y validación estructural

* Pandas para procesamiento de datos

* Reutilización directa de las funciones de eda.py y limpieza.py

Separación clara entre:

* lógica de negocio

* validación

* orquestación

El archivo main.py actúa como orquestador, conectando los distintos módulos del proyecto sin duplicar lógica.

 Landing Page (Presentación)

La API incluye una landing page personalizada accesible desde la ruta raíz (/), diseñada para:

* Presentar el proyecto de forma visual y profesional

* Identificar al equipo de desarrollo

* Explicar brevemente el propósito de la API

* Redirigir a la documentación técnica interactiva

Esta página está implementada usando HTML + CSS embebido, sin dependencias externas.

 Endpoints Disponibles
GET /

* Landing page de presentación

* Página HTML informativa del proyecto

* No forma parte del esquema OpenAPI

POST /limpieza

* Ejecutar pipeline de limpieza de datos

* Ejecuta de forma secuencial:

* Análisis exploratorio de datos (EDA)

* Carga del dataset original

* Limpieza avanzada

* Exportación del dataset limpio a disco

GET /limpieza

Consultar resultado de la limpieza

Verifica si el archivo limpio ya fue generado

Evita ejecuciones innecesarias del pipeline

Si el archivo no existe, retorna un error controlado (404).

 Documentación Automática

FastAPI genera automáticamente documentación interactiva:

* Swagger UI:
/docs

* ReDoc:
/redoc

Estas interfaces permiten:

* Probar endpoints

* Visualizar esquemas de entrada y salida

* Validar contratos de datos

 Validación y Robustez

La API se apoya en los esquemas definidos en schemas.py, lo que garantiza:

* Tipado estricto

* Reglas de negocio explícitas

* Prevención de datos inconsistentes

* Preparación directa para consumo por modelos de ML

 Preparación para Fases Futuras

Esta API deja preparado el proyecto para:

* Integración de modelos predictivos

* Endpoints de inferencia

* Despliegue en servicios cloud

* Consumo por aplicaciones externas

Si quieres, en el próximo mensaje puedo ay
