from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
import os

# ==============================
# CONFIGURACIÓN GENERAL DE LA API
# ==============================

app = FastAPI(
    title="Hotel Bookings API",
    description="API para la limpieza y procesamiento de datos de reservas hoteleras",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "Pipeline",
            "description": "Procesos automáticos de EDA y limpieza de datos"
        }
    ]
)

# ==============================
# LANDING PAGE (PRESENTACIÓN)
# ==============================

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def landing_page():
    return """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Hotel Bookings API</title>
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                background-color: #f3f4f6;
                color: #111827;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            .container {
                max-width: 720px;
                background: white;
                padding: 3.5rem;
                border-radius: 14px;
                box-shadow: 0 15px 30px rgba(0,0,0,0.08);
                text-align: center;
            }
            h1 {
                font-size: 2.4rem;
                margin-bottom: 0.5rem;
            }
            h2 {
                font-size: 1.1rem;
                font-weight: 400;
                color: #6b7280;
                margin-bottom: 2rem;
            }
            ul {
                list-style: none;
                padding: 0;
                margin: 1rem 0;
            }
            li {
                margin: 0.4rem 0;
            }
            p {
                line-height: 1.6;
                margin-top: 1.5rem;
            }
            .btn {
                display: inline-block;
                margin-top: 2.5rem;
                padding: 0.8rem 1.8rem;
                background-color: #2563eb;
                color: white;
                text-decoration: none;
                border-radius: 10px;
                font-weight: 500;
            }
            .btn:hover {
                background-color: #1d4ed8;
            }
            footer {
                margin-top: 2.5rem;
                font-size: 0.85rem;
                color: #9ca3af;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Hotel Bookings API</h1>
            <h2>Limpieza y procesamiento de datos de reservas hoteleras</h2>

            <p><strong>Equipo de desarrollo</strong></p>
            <ul>
                <li>Natalia Gonzalez</li>
                <li>Alejandra Gordillo</li>
                <li>Haider Rojas</li>
            </ul>

            <p>
                API académica que automatiza el análisis exploratorio de datos (EDA)
                y la limpieza avanzada de reservas hoteleras, generando datasets
                listos para modelado predictivo.
            </p>

            <a href="/docs" class="btn">Ver documentación técnica</a>

            <footer>
                Proyecto académico · FastAPI · Pandas · Pydantic
            </footer>
        </div>
    </body>
    </html>
    """

# ==============================
# MODELO DE RESPUESTA
# ==============================

class LimpiezaResponse(BaseModel):
    status: str
    output: str

OUTPUT_PATH = "data/hotel_bookings_limpio.csv"

# ==============================
# POST → EJECUTAR LIMPIEZA
# ==============================

@app.post(
    "/limpieza",
    tags=["Pipeline"],
    summary="Ejecutar pipeline de limpieza de datos",
    response_model=LimpiezaResponse
)
def ejecutar_limpieza():
    """
    Ejecuta el pipeline completo de EDA + limpieza de datos.
    """
    import pandas as pd
    import eda
    from limpieza import limpieza_avanzada

    # Ejecutar EDA
    eda.main()

    # Cargar datos
    df = pd.read_csv("data/hotel_bookings.csv")

    # Limpieza
    df_limpio = limpieza_avanzada(df)

    # Guardar resultado
    df_limpio.to_csv(OUTPUT_PATH, index=False)

    return {
        "status": "ok",
        "output": OUTPUT_PATH
    }

# ==============================
# GET → CONSULTAR RESULTADO
# ==============================

@app.get(
    "/limpieza",
    tags=["Pipeline"],
    summary="Consultar resultado de la limpieza",
    response_model=LimpiezaResponse
)
def obtener_resultado_limpieza():
    """
    Consulta si el archivo limpio ya fue generado.
    """
    if not os.path.exists(OUTPUT_PATH):
        raise HTTPException(
            status_code=404,
            detail="El archivo limpio aún no ha sido generado. Ejecute primero el POST /limpieza."
        )

    return {
        "status": "ok",
        "output": OUTPUT_PATH
    }