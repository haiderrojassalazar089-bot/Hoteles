from pydantic import BaseModel, Field
from typing import Optional, Literal


# ==============================
# INPUT SCHEMA
# ==============================

class HotelBookingInput(BaseModel):
    """
    Esquema de entrada para predicción de cancelación
    """

    # Tipo de hotel (limitado a valores reales del dataset)
    hotel: Literal["Resort Hotel", "City Hotel"]

    # Información temporal
    lead_time: int = Field(..., ge=0, description="Días entre reserva y llegada")
    arrival_date_year: int = Field(..., ge=2015)
    arrival_date_month: Literal[
        "January", "February", "March", "April",
        "May", "June", "July", "August",
        "September", "October", "November", "December"
    ]
    arrival_date_week_number: int = Field(..., ge=1, le=53)
    arrival_date_day_of_month: int = Field(..., ge=1, le=31)

    # Estadía
    stays_in_weekend_nights: int = Field(..., ge=0)
    stays_in_week_nights: int = Field(..., ge=0)

    # Huéspedes
    adults: int = Field(..., ge=0)
    children: Optional[float] = Field(0, ge=0)
    babies: int = Field(..., ge=0)

    # Precio
    adr: float = Field(..., ge=0, description="Average Daily Rate")

    # Segmentación comercial
    meal: str
    market_segment: str
    distribution_channel: str
    reserved_room_type: str
    deposit_type: str
    customer_type: str

    class Config:
        schema_extra = {
            "example": {
                "hotel": "Resort Hotel",
                "lead_time": 45,
                "arrival_date_year": 2017,
                "arrival_date_month": "July",
                "arrival_date_week_number": 27,
                "arrival_date_day_of_month": 15,
                "stays_in_weekend_nights": 2,
                "stays_in_week_nights": 3,
                "adults": 2,
                "children": 1,
                "babies": 0,
                "adr": 120.5,
                "meal": "BB",
                "market_segment": "Online TA",
                "distribution_channel": "TA/TO",
                "reserved_room_type": "A",
                "deposit_type": "No Deposit",
                "customer_type": "Transient"
            }
        }


# ==============================
# OUTPUT SCHEMA
# ==============================

class HotelBookingOutput(BaseModel):
    """
    Esquema de salida del modelo
    """

    prediction: int = Field(..., description="0 = No cancelado, 1 = Cancelado")
    probability: float = Field(..., ge=0, le=1)
    label: Literal["Not Canceled", "Canceled"]