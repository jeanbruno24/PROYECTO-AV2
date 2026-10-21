from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st
from sklearn.linear_model import LinearRegression


st.set_page_config(
    page_title="Dashboard de resistencia del concreto",
    page_icon="🏗️",
    layout="wide",
)

DATASET = Path(__file__).resolve().parent / "Pervious_Concrete_0.csv"
FC = "Compressive Strength (Kg/m2)"
EDAD = "Age (Day)"
VARIABLE = "% Voids"  # reemplaza a la edad, porque en tu CSV todas son de 28 días
COMPONENTES = {
    "Cemento": "Cement KG/M3 (component 1)",
    "Agregado grueso": "Coarse Aggregate KG/M3 (component 2)",
    "Agregado fino": "Fine Aggregate KG/M3 (component 3)",
    "Agua": "Water KG/M3 (component 4)",
    "Superplastificante": "Superplasticizer KG/M3 (component 5)",
}

st.title("Dashboard de resistencia del concreto")
st.caption("Indicadores, análisis de mezclas y predicción de resistencia")

if not DATASET.is_file():
    st.error(f"No se encontró el archivo del dataset: {DATASET}")
    st.stop()

df = pd.read_csv(DATASET, encoding="utf-8-sig")
df.columns = df.columns.str.strip()

columnas_requeridas = [FC, EDAD, VARIABLE, *COMPONENTES.values()]
faltantes = [columna for columna in columnas_requeridas if columna not in df.columns]
if faltantes:
    st.error("Faltan columnas requeridas en el CSV: " + ", ".join(faltantes))
    st.stop()

filas_originales = len(df)
df = df.drop_duplicates()
duplicados_eliminados = filas_originales - len(df)

with st.sidebar:
    st.header("Datos")
    st.write(f"Registros cargados: **{filas_originales:,}**")
    st.write(f"Duplicados completos excluidos: **{duplicados_eliminados:,}**")
    st.write(f"Registros analizados: **{len(df):,}**")
    st.caption("Los análisis excluyen filas idénticas en todas sus columnas.")

media = df[FC].mean()
mediana = df[FC].median()
moda = df[FC].mode().iloc[0]
desviacion_estandar = df[FC].std()

tab_resumen, tab_distribucion, tab_mezclas, tab_correlaciones, tab_modelo = st.tabs(
    ["Resumen", "Distribución", "Mezclas y vacíos", "Correlaciones", "Modelo predictivo"]
)

with tab_resumen:
    st.subheader("Indicadores clave (KPIs)")
    kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
    kpi1.metric("Resistencia promedio", f"{media:.2f} Kg/m2")
    kpi2.metric("Resistencia máxima", f"{df[FC].max():.2f} Kg/m2")
    kpi3.metric("Resistencia mínima", f"{df[FC].min():.2f} Kg/m2")
    kpi4.metric("Registros analizados", f"{len(df):,}")
    kpi5.metric("Edad promedio", f"{df[EDAD].mean():.2f} días")

    st.subheader("Vista previa del dataset limpio")
    st.dataframe(df.head(10), use_container_width=True)

with tab_distribucion:
    st.subheader("Distribución de la resistencia")
    st.caption(
        f"Media: {media:.2f} Kg/m2 · Mediana: {mediana:.2f} Kg/m2 · "
        f"Moda: {moda:.2f} Kg/m2 · Desviación estándar: {desviacion_estandar:.2f} Kg/m2"
    )
    histograma = px.histogram(
        df,
        x=FC,
        nbins=30,
        title="Distribución de la resistencia del concreto (sin filas duplicadas)",
    )
    for nombre, valor, color, estilo in [
        ("Media", media, "red", "dash"),
        ("Mediana", mediana, "blue", "dashdot"),
        ("Moda", moda, "green", "dot"),
    ]:
        histograma.add_vline(
            x=valor,
            line_dash=estilo,
            line_color=color,
            annotation_text=f"{nombre}: {valor:.2f}",
        )
    st.plotly_chart(histograma, use_container_width=True)

with tab_mezclas:
    st.subheader("Vacíos, diseño de mezcla y resistencia")
    st.markdown(
        "Cada punto representa una mezcla. Gira el gráfico y coloca el cursor sobre un "
        "punto para consultar las cantidades de sus componentes."
    )
    ingredientes = list(COMPONENTES.values())
    nombres_componentes = list(COMPONENTES.keys())
    scatter3d = px.scatter_3d(
        df,
        x=VARIABLE,
        y=COMPONENTES["Cemento"],
        z=FC,
        color=FC,
        color_continuous_scale="Viridis",
        opacity=0.75,
        hover_data=[COMPONENTES["Agua"]],
        title="Vacíos y cantidad de cemento vs resistencia del concreto",
        labels={
            VARIABLE: "Vacíos (%)",
            COMPONENTES["Cemento"]: "Cemento (kg/m³)",
            FC: "Resistencia (Kg/m2)",
            COMPONENTES["Agua"]: "Agua (kg/m³)",
        },
    )
    scatter3d.update_traces(marker={"size": 4})
    scatter3d.update_layout(
        scene={
            "xaxis_title": "Vacíos (%)",
            "yaxis_title": "Cemento (kg/m³)",
            "zaxis_title": "Resistencia (Kg/m2)",
            "camera": {"eye": {"x": 1.6, "y": 1.6, "z": 1.2}},
        },
        coloraxis_colorbar={"title": "Resistencia (Kg/m2)"},
    )
    st.plotly_chart(scatter3d, use_container_width=True)

    serie = df.groupby(VARIABLE)[[FC, *ingredientes]].mean().reset_index()
    etiquetas = {
        VARIABLE: "Vacíos (%)",
        FC: "Resistencia promedio (Kg/m2)",
        **{
            columna: f"{nombre} (kg/m³)"
            for nombre, columna in COMPONENTES.items()
        },
    }
    linea = px.line(
        serie,
        x=VARIABLE,
        y=FC,
        markers=True,
        hover_data=ingredientes,
        title="Resistencia promedio y diseño de mezcla por vacíos",
        labels=etiquetas,
    )
    st.plotly_chart(linea, use_container_width=True)

with tab_correlaciones:
    st.subheader("Mapa de correlaciones")
    numericas = df.select_dtypes("number")
    numericas = numericas.loc[:, numericas.nunique() > 1]  # quita columnas constantes (Edad)
    corr = numericas.corr()
    mapa = px.imshow(
        corr,
        text_auto=".2f",
        color_continuous_scale="RdBu_r",
        zmin=-1,
        zmax=1,
        aspect="auto",
        title="Correlación entre variables numéricas",
        labels={"color": "Correlación"},
    )
    st.plotly_chart(mapa, use_container_width=True)
    st.caption("La correlación describe asociación lineal; no implica causalidad.")

with tab_modelo:
    st.subheader("Predicción con regresión lineal")
    st.write("El modelo usa únicamente el % de vacíos del concreto para predecir su resistencia.")

    minimo = float(df[VARIABLE].min())
    maximo = float(df[VARIABLE].max())
    vacios_prediccion = st.number_input(
        "% de vacíos para la predicción",
        min_value=0.0,
        max_value=100.0,
        value=float(df[VARIABLE].median()),
        step=1.0,
    )

    X = df[[VARIABLE]]
    y = df[FC]
    modelo = LinearRegression()
    modelo.fit(X, y)

    resistencia_predicha = modelo.predict(pd.DataFrame({VARIABLE: [vacios_prediccion]}))[0]
    r2 = modelo.score(X, y)

    col1, col2 = st.columns(2)
    col1.metric("Resistencia predicha", f"{resistencia_predicha:.2f} Kg/m2")
    col2.metric("R² (datos de entrenamiento)", f"{r2:.4f}")

    if not (minimo <= vacios_prediccion <= maximo):
        st.warning(
            f"El valor está fuera del rango de tus datos ({minimo:.0f} a {maximo:.0f}). "
            "La predicción no es confiable."
        )

    ajuste = px.scatter(
        df,
        x=VARIABLE,
        y=FC,
        trendline="ols",
        title="Ajuste lineal: vacíos vs resistencia",
        labels={VARIABLE: "Vacíos (%)", FC: "Resistencia (Kg/m2)"},
    )
    st.plotly_chart(ajuste, use_container_width=True)