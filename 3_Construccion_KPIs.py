import pandas as pd

# Cargar el dataset y eliminar filas duplicadas
df = pd.read_csv("Pervious_Concrete_0.csv", encoding="utf-8-sig")
df.columns = df.columns.str.strip()
df = df.drop_duplicates()

# Definir la variable objetivo
fc = "Compressive Strength (Kg/m2)"

# Calcular KPIs
resistencia_promedio = df[fc].mean()
resistencia_maxima = df[fc].max()
resistencia_minima = df[fc].min()
cantidad_registros = df.shape[0]
edad_promedio = df["Age (Day)"].mean()

# Mostrar resultados
print(f"Resistencia promedio: {resistencia_promedio:.2f} Kg/m2")
print(f"Resistencia máxima: {resistencia_maxima:.2f} Kg/m2")
print(f"Resistencia mínima: {resistencia_minima:.2f} Kg/m2")
print(f"Número de registros: {cantidad_registros}")
print(f"Edad promedio: {edad_promedio:.2f} días")