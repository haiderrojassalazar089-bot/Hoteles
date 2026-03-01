from schemas import HotelBookingInput, HotelBookingOutput

# Ejemplo de entrada válida
input_data = {
    "hotel": "Resort Hotel",
    "lead_time": 30,
    "arrival_date_year": 2017,
    "arrival_date_month": "July",
    "arrival_date_week_number": 27,
    "arrival_date_day_of_month": 15,
    "stays_in_weekend_nights": 2,
    "stays_in_week_nights": 3,
    "adults": 2,
    "children": 1,
    "babies": 0,
    "adr": 100.0,
    "meal": "BB",
    "market_segment": "Online TA",
    "distribution_channel": "TA/TO",
    "reserved_room_type": "A",
    "deposit_type": "No Deposit",
    "customer_type": "Transient"
}

validated_input = HotelBookingInput(**input_data)
print("Input validado correctamente:")
print(validated_input)

# Simulación de salida del modelo
output = HotelBookingOutput(
    prediction=1,
    probability=0.82,
    label="Canceled"
)

print("\nOutput generado:")
print(output)