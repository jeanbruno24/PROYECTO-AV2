import pandas as pd
import plotly.express as px

# Cargar el dataset, normalizar encabezados y eliminar filas duplicadas
df = pd.read_csv("Pervious_Concrete_0.csv", encoding="utf-8-sig")
df.columns = df.columns.str.strip()
df = df.drop_duplicates()

# Variable de tiempo y variable objetivo
tiempo = "Age (Day)"
fc = "Compressive Strength (Kg/m2)"
cemento = "Cement KG/M3 (component 1)"
agregado_grueso = "Coarse Aggregate KG/M3 (component 2)"
agregado_fino = "Fine Aggregate KG/M3 (component 3)"
agua = "Water KG/M3 (component 4)"
superplastificante = "Superplasticizer KG/M3 (component 5)"

componentes = [cemento, agregado_grueso, agregado_fino, agua, superplastificante]

# Calcular promedios de resistencia y componentes de mezcla para cada edad
serie = df.groupby(tiempo)[[fc, *componentes]].mean().reset_index()

# Crear la serie en 3D
fig = px.scatter_3d(
    serie,
    x=tiempo,
    y=cemento,
    z=fc,
    color=agua,
    color_continuous_scale="Viridis",
    opacity=0.75,
    hover_data=[superplastificante, agregado_grueso, agregado_fino],
    title="Serie temporal: edad, cemento y resistencia del concreto",
    labels={
        tiempo: "Edad del concreto (días)",
        cemento: "Cemento (kg/m³)",
        fc: "Resistencia a la compresión (Kg/m2)",
        agua: "Agua (kg/m³)",
        superplastificante: "Superplastificante (kg/m³)",
        agregado_grueso: "Agregado grueso (kg/m³)",
        agregado_fino: "Agregado fino (kg/m³)",
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
    coloraxis_colorbar={"title": "Agua (kg/m³)"},
)

fig.show()