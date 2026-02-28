import pandas as pd
import eda
from limpieza import limpieza_avanzada


# 1️⃣ Ejecutar EDA exactamente como está
print("\n========== EJECUTANDO EDA ==========")
eda.main()

# 2️⃣ Cargar datos para limpiar
ruta = "data/hotel_bookings.csv"
df = pd.read_csv(ruta)

# 3️⃣ Limpieza
print("\n========== INICIANDO LIMPIEZA ==========")
df_limpio = limpieza_avanzada(df)

# 4️⃣ Guardar limpio
df_limpio.to_csv("data/hotel_bookings_limpio.csv", index=False)

print("\nProceso completo finalizado.")