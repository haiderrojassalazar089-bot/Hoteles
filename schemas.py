from pydantic import BaseModel, Field, StrictInt, StrictFloat, model_validator, ConfigDict
from typing import Optional
from enum import Enum


# ==============================
# ENUMS FORMALES
# ==============================

class HotelType(str, Enum):
    RESORT = "Resort Hotel"
    CITY = "City Hotel"


class Month(str, Enum):
    JAN = "January"
    FEB = "February"
    MAR = "March"
    APR = "April"
    MAY = "May"
    JUN = "June"
    JUL = "July"
    AUG = "August"
    SEP = "September"
    OCT = "October"
    NOV = "November"
    DEC = "December"


class Label(str, Enum):
    NOT_CANCELED = "Not Canceled"
    CANCELED = "Canceled"


# ==============================
# INPUT SCHEMA
# ==============================

class HotelBookingInput(BaseModel):

    model_config = ConfigDict(
        extra="forbid",            # No permitir campos no definidos
        validate_assignment=True   # Revalidar si se modifica un campo
    )

    # Hotel
    hotel: HotelType

    # Tiempo
    lead_time: StrictInt = Field(..., ge=0, le=1000)
    arrival_date_year: StrictInt = Field(..., ge=2015, le=2030)
    arrival_date_month: Month
    arrival_date_week_number: StrictInt = Field(..., ge=1, le=53)
    arrival_date_day_of_month: StrictInt = Field(..., ge=1, le=31)

    # Estadía
    stays_in_weekend_nights: StrictInt = Field(..., ge=0, le=30)
    stays_in_week_nights: StrictInt = Field(..., ge=0, le=60)

    # Huéspedes
    adults: StrictInt = Field(..., ge=0, le=10)
    children: Optional[StrictFloat] = Field(0, ge=0, le=10)
    babies: StrictInt = Field(..., ge=0, le=5)

    # Precio
    adr: StrictFloat = Field(..., ge=0, le=5000)

    # Segmentación
    meal: str
    market_segment: str
    distribution_channel: str
    reserved_room_type: str
    deposit_type: str
    customer_type: str

    # ==============================
    # VALIDACIONES CRUZADAS
    # ==============================

    @model_validator(mode="after")
    def validar_reglas_negocio(self):

        total_guests = self.adults + (self.children or 0) + self.babies
        total_nights = self.stays_in_weekend_nights + self.stays_in_week_nights

        if total_guests <= 0:
            raise ValueError("Debe haber al menos un huésped en la reserva.")

        if total_nights <= 0:
            raise ValueError("La reserva debe tener al menos una noche.")

        return self


# ==============================
# OUTPUT SCHEMA
# ==============================

class HotelBookingOutput(BaseModel):

    model_config = ConfigDict(extra="forbid")

    prediction: StrictInt = Field(..., ge=0, le=1)
    probability: StrictFloat = Field(..., ge=0, le=1)
    label: Label

    @model_validator(mode="after")
    def consistencia_prediccion(self):

        if self.prediction == 1 and self.label != Label.CANCELED:
            raise ValueError("Inconsistencia entre prediction y label.")

        if self.prediction == 0 and self.label != Label.NOT_CANCELED:
            raise ValueError("Inconsistencia entre prediction y label.")

        return self