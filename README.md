# AVPF-2

## Título del Proyecto

Dashboard interactivo para el análisis y la predicción de la resistencia a la compresión del concreto permeable.

**Curso:** Herramientas de Desarrollo Profesional Civil · Universidad Tecnológica del Perú · Ingeniería Civil
**Grupo:** 9 (AVPF2_G9)
**Docente:** Hilder Javier Jimenez Pesantes

## Objetivo

Analizar y visualizar información técnica mediante herramientas de Data Analytics: estudiar 49 mezclas de concreto permeable, calcular indicadores clave, explorar la relación entre los componentes de la mezcla y la resistencia, y estimar la resistencia a la compresión a partir del porcentaje de vacíos mediante una regresión lineal simple.

## Dataset

**Archivo:** `Pervious_Concrete_0.csv` (49 registros, 1 mezcla o muestra por registro).

**Fuente:**

https://drive.google.com/drive/folders/1RmXQKY0Tn3p_zdRw8ULk5vRrm1H1Sl2Z?usp=drive_link

| Variable | Unidad | Rol |
|---|---|---|
| Vacíos | % | Predictora del modelo (rango 8 % a 16 %) |
| Cemento | kg/m³ | Explicativa |
| Agregado grueso | kg/m³ | Explicativa |
| Agregado fino | kg/m³ | Explicativa |
| Agua | kg/m³ | Explicativa |
| Superplastificante | kg/m³ | Explicativa |
| Permeabilidad K | mm/seg | Característica hidráulica |
| Edad | días | Control (todas las muestras: 28 días) |
| Resistencia a la compresión | Kg/m² | Variable objetivo |

Tras la validación no hubo filas duplicadas: 49 registros recibidos y 49 analizados.

> **Nota sobre unidades:** el dashboard rotula la resistencia en Kg/m². Por su orden de magnitud (110 a 264), es probable que los valores correspondan a kg/cm².

## Tecnologías Utilizadas

- Python
- Pandas
- Plotly
- Scikit-Learn
- Streamlit (dashboard en Python)
- HTML + Plotly.js (dashboard web, `Dashboard_AVPF2.html`)
- Jupyter
- GitHub

## KPIs

| Indicador | Valor |
|---|---|
| Resistencia promedio | 174.49 Kg/m² |
| Resistencia máxima | 264.00 Kg/m² |
| Resistencia mínima | 110.00 Kg/m² |
| Edad promedio | 28.00 días |
| Número de registros | 49 |

Estadísticos complementarios: mediana 145.00, moda 141.00, desviación estándar 52.66 Kg/m² (coeficiente de variación ≈ 30.2 %).

## Dashboard

Aplicación web que se ejecuta en el navegador; los datos se procesan localmente y no se envían a ningún servidor. Sus componentes son:

1. **Carga de datos:** selección del CSV y reporte de registros recibidos, duplicados excluidos y analizados.
2. **Tarjetas de KPIs:** resistencia promedio, máxima y mínima, registros analizados y edad promedio.
3. **Distribución de la resistencia:** histograma con media, mediana y moda.
4. **Correlaciones:** matriz de Pearson entre las variables numéricas.
5. **Vacíos, mezcla y resistencia:** diagrama 3D interactivo (vacíos, cemento y resistencia).
6. **Serie por % de vacíos:** resistencia promedio para cada nivel de vacíos.
7. **Modelo predictivo lineal:** ingreso de % de vacíos, resistencia predicha, R² y aviso de extrapolación.

### Vista general

![Carga de datos e indicadores clave](imagenes/01_kpis_dashboard.png)

![Distribución y correlaciones](imagenes/02_distribucion_correlaciones.png)

![Vacíos, diseño de mezcla y resistencia](imagenes/03_vacios_3d.png)

![Resistencia promedio por % de vacíos](imagenes/04_serie_vacios.png)

![Modelo predictivo lineal](imagenes/05_modelo_predictivo.png)

## Resultados principales

- El porcentaje de vacíos tiene la relación lineal inversa más clara con la resistencia (r = −0.94).
- Entre 8 % y 16 % de vacíos, la resistencia promedio baja de ≈255 a ≈113 Kg/m² (≈55 %).
- Existe un compromiso entre permeabilidad y resistencia: más vacíos implican más permeabilidad (r = 0.85) pero menos resistencia.
- La distribución de la resistencia es bimodal; la media (174.49) no representa bien a ninguno de los dos grupos de mezclas.
- Modelo de regresión lineal simple: **R² = 0.8757** (entrenamiento). Es confiable solo entre 8 % y 16 % de vacíos; por ejemplo, 20 % → 21.00 Kg/m² es una extrapolación no confiable.
- La correlación mide asociación lineal y no demuestra causalidad.

## Estructura del proyecto

El código está organizado de forma secuencial en la raíz del proyecto para facilitar su auditoría paso a paso:

├── .git/                      # Carpeta de control de versiones
├── 1_Cargar_Dataset.py         # Conexión e importación del dataset original
├── 2_Limpieza-rapida.py       # Tratamiento de nulos y formato de variables
├── 3_Construccion_KPIs.py     # Procesamiento y cálculo de métricas técnicas
├── 4_Graficos_basicos.py       # Primeras exploraciones visuales
├── 5_Graficos_mejores.py       # Gráficos refinados para el informe
├── 6_Mapa-calor_correlaciones.py # Matriz estadística de Pearson
├── 7_Serie_Temporal.py         # Análisis del comportamiento secuencial
├── 8_Modelo_predictivo.py      # Entrenamiento de la regresión lineal simple
├── 9_Dashboard_Integral.py     # Código base de la aplicación interactiva (Streamlit)
├── 9_Dashboard_propia-web      # Archivo de origen HTML con el dashboard generado
├── Pervious_Concrete_0.csv     # Dataset con los 49 registros de las mezclas
└── README.md                   # Este archivo de documentación


## Cómo ejecutar

1. **Instalar dependencias:**
   Asegúrate de contar con las librerías necesarias ejecutando en tu terminal:
   ```bash
   pip install pandas plotly scikit-learn streamlit
   ```

2. **Ejecutar el pipeline paso a paso:**
   Puedes correr cualquiera de los scripts numéricos directamente en Python, por ejemplo:
   ```bash
   python 1_Cargar_Dataset.py
   ```

3. **Lanzar el Dashboard Interactivo:**
   Para desplegar la interfaz gráfica de Streamlit en tu navegador local, ejecuta:
   ```bash
   streamlit run 9_Dashboard_Integral.py
   ```
   *(Alternativamente, puedes abrir directamente el archivo interactivo `9_Dashboard_propia-web` en tu navegador favorito).*


## Integrantes

- Jean Piere Bruno Silupu
