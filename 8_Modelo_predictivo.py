import pandas as pd
from sklearn.linear_model import LinearRegression

# Cargar el dataset, normalizar encabezados y eliminar filas duplicadas
df = pd.read_csv("Pervious_Concrete_0.csv", encoding="utf-8-sig")
df.columns = df.columns.str.strip()
df = df.drop_duplicates()

# Definir la variable objetivo y la variable de entrada
fc = "Compressive Strength (Kg/m2)"
entrada = "% Voids"   # cambia a "Age (Day)" si tu profe exige edad
X = df[[entrada]]
y = df[fc]

# Entrenar el modelo lineal
modelo = LinearRegression()
modelo.fit(X, y)

# Predecir la resistencia para un nuevo valor de la variable de entrada
print(f"Rango de {entrada} en tus datos: {df[entrada].min()} a {df[entrada].max()}")
valor_nuevo = 20   # cambia este valor por uno dentro del rango que se imprime
nuevo = pd.DataFrame({entrada: [valor_nuevo]})
resistencia_nueva = modelo.predict(nuevo)[0]
print(f"Resistencia predicha con {valor_nuevo} de {entrada}: {resistencia_nueva:.2f} Kg/m2")

# Calcular R² sobre los mismos datos usados para entrenar
r2 = modelo.score(X, y)
print(f"R² en los datos de entrenamiento: {r2:.4f}")