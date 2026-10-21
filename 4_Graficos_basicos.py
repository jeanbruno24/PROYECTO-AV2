import pandas as pd
import plotly.express as px

# Cargar el dataset y preparar la variable objetivo
df = pd.read_csv("Pervious_Concrete_0.csv", encoding="utf-8-sig")
df.columns = df.columns.str.strip()
df = df.drop_duplicates()
fc = "Compressive Strength (Kg/m2)"

media = df[fc].mean()
moda = df[fc].mode().iloc[0]
mediana = df[fc].median()
desviacion_estandar = df[fc].std()

# Crear el histograma de la resistencia del concreto
fig = px.histogram(
    df,
    x=fc,
    nbins=30,
    title="Distribución de la resistencia del concreto (sin filas duplicadas)",
)

fig.add_vline(
    x=media,
    line_dash="dash",
    line_color="red",
    annotation_text=f"Media: {media:.2f}",
    annotation_position="top right",
)
fig.add_vline(
    x=moda,
    line_dash="dot",
    line_color="green",
    annotation_text=f"Moda: {moda:.2f}",
    annotation_position="top left",
)
fig.add_vline(
    x=mediana,
    line_dash="dashdot",
    line_color="blue",
    annotation_text=f"Mediana: {mediana:.2f}",
    annotation_position="top",
)
fig.add_annotation(
    text=f"Desviación estándar: {desviacion_estandar:.2f} Kg/m2",
    xref="paper", yref="paper",
    x=0.99, y=0.99,
    showarrow=False,
    bgcolor="white",
)

fig.show()