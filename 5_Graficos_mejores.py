#Diagrama de dispersion
#Relación: Edad vs Resistencia.
import pandas as pd
import plotly.express as px

# Cargar el dataset y eliminar filas duplicadas completas
df = pd.read_csv("Pervious_Concrete_0.csv", encoding="utf-8-sig")
df.columns = df.columns.str.strip()
df = df.drop_duplicates()

# Definir la variable objetivo
fc = "Compressive Strength (Kg/m2)"
cemento = "Cement KG/M3 (component 1)"
agua = "Water KG/M3 (component 4)"

# Crear un diagrama 3D interactivo: permite girar y acercar la vista
fig = px.scatter_3d(
    df,
    x="Age (Day)",
    y=cemento,
    z=fc,
    color=fc,
    color_continuous_scale="Viridis",
    opacity=0.75,
    hover_data=[agua],
    title="Edad y cantidad de cemento vs resistencia del concreto",
    labels={
        "Age (Day)": "Edad del concreto (días)",
        cemento: "Cemento (kg/m³)",
        fc: "Resistencia a la compresión (Kg/m2)",
        agua: "Agua (kg/m³)",
    },
)

fig.update_traces(marker={"size": 4})
fig.update_layout(
    scene={
        "xaxis_title": "Edad (días)",
        "yaxis_title": "Cemento (kg/m³)",
        "zaxis_title": "Resistencia (Kg/m2)",
        "camera": {"eye": {"x": 1.6, "y": 1.6, "z": 1.2}},
    },
    coloraxis_colorbar={"title": "Resistencia (Kg/m2)"},
)

fig.show()