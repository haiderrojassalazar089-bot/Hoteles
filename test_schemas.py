from schemas import HotelBookingInput, HotelBookingOutput, Label


# ==============================
# TEST INPUT VÁLIDO
# ==============================

valid_input = {
    "hotel": "Resort Hotel",
    "lead_time": 30,
    "arrival_date_year": 2017,
    "arrival_date_month": "July",
    "arrival_date_week_number": 27,
    "arrival_date_day_of_month": 15,
    "stays_in_weekend_nights": 2,
    "stays_in_week_nights": 3,
    "adults": 2,
    "children": 1.0,
    "babies": 0,
    "adr": 120.5,
    "meal": "BB",
    "market_segment": "Online TA",
    "distribution_channel": "TA/TO",
    "reserved_room_type": "A",
    "deposit_type": "No Deposit",
    "customer_type": "Transient"
}

booking = HotelBookingInput(**valid_input)
print("Entrada validada correctamente:")
print(booking)


# ==============================
# TEST OUTPUT VÁLIDO
# ==============================

valid_output = HotelBookingOutput(
    prediction=1,
    probability=0.82,
    label=Label.CANCELED
)

print("\nSalida validada correctamente:")
print(valid_output)


# ==============================
# TEST ERROR INTENCIONAL
# ==============================

try:
    invalid_input = valid_input.copy()
    invalid_input["adults"] = 0
    invalid_input["children"] = 0
    invalid_input["babies"] = 0

    HotelBookingInput(**invalid_input)

except Exception as e:
    print("\nError detectado correctamente:")
    print(e)