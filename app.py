# Cargar liberias
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Cargar datos
df = pd.read_csv('vehicles_us.csv')

# Poner título
st.header('Estudio sobre la venta de vehículos', divider = "gray")

# Descargar dataset
st.download_button(
    label = "Descargar dataset", 
    data = df.to_csv(index=False), 
    file_name = "df.csv"
)

st.divider()

# Gráficos de barras, tendencias modelos más vendidos
st.subheader("Modelos más vendidos")
top_20_models = df['model'].value_counts().head(20)

fig = px.bar(
    x=top_20_models.index,
    y=top_20_models.values,
    title='Top 20 histórico de Modelos de Vehículos Más Vendidos',
    labels={'x': 'Modelo', 'y': 'Autos vendidos'},
    color_discrete_sequence=['navy']
)

fig.update_layout(xaxis_tickangle=-45)

st.plotly_chart(fig, use_container_width=True)

# Años de modelos más vendidos
st.subheader("Años de modelos más vendidos")
top_years = df['model_year'].value_counts().sort_values(ascending = False)

fig1 = px.bar(
    x=top_years.index,  # Los nombres de los modelos
    y=top_years.values, # Las cantidades
    title='Número de autos vendidos de acuerdo al año del modelo',
    labels={'x': 'Año de modelo', 'y': 'Autos vendidos'},
    color_discrete_sequence=['navy']
)

# Rotar las etiquetas del eje x para mejor legibilidad
fig1.update_layout(xaxis_tickangle=-45)

st.plotly_chart(fig1, use_container_width=True)


### SEGUNDA SECCION
st.header("Distribución de precios")

opcion = st.selectbox(
    "Selecciona una variable para analizar el precio según:",
    ["condition", "cylinders", "fuel", "transmission", "type"],
    index=0
)

fig = px.histogram(
    df, 
    x="price", 
    color=opcion,
    nbins=30,
    title=f"Distribución del precio según {opcion}",
    template="plotly_white"
)

fig.update_layout(
    xaxis_title="Precio (USD)",
    yaxis_title="Frecuencia",
    title_x=0.5
)
fig.update_traces(opacity=0.75)

st.plotly_chart(fig, use_container_width=True)

### TERCERA PARTE, GRÁFICO DE DISPERSIÓN
# --- Relación entre variables ---
st.subheader("Relación entre Odómetro y Precio")

# Diagrama de dispersión: Precio vs Kilometraje
disp_plot = px.scatter(
    df,
    x = "price",
    y = "odometer",
    color = "condition",
    title = "Relación negativa entre precio y kilometraje",
    width = 700,
    height = 400,
    template="plotly_white"
)


# Mostrar la gráfica
st.plotly_chart(disp_plot, use_container_width=True)

# Calcular correlación de Pearson
corr_df = df[['odometer', 'price']].dropna()
correl = np.corrcoef(corr_df['odometer'], corr_df['price'])

# Mostrar correlación como métrica
st.metric(
    label="Correlación de Pearson (Precio vs Kilometraje)",
    value="{:.1%}".format(correl[0,1])
)

## CUARTA SECCIÓN: DESEMPEÑO DE VENTAS

st.header("Velocidad de venta según tipo de carro")

resumen = df.groupby('type').agg(
    mean_days=('days_listed', 'mean'),
    std_days=('days_listed', 'std')
).reset_index()

dias_tipo = px.bar(resumen,
             x='type',
             y='mean_days',
             error_y='std_days',
             title='Promedio y desviación estándar del número de días en venta por tipo de carro',
             labels={'type': 'Tipo de carro', 'mean_days': 'Promedio de días en venta'},
             template="plotly_white")  # opcional, para darle color a cada barra

dias_tipo.update_layout(xaxis_tickangle=-45)  # rotar etiquetas si son largas

st.plotly_chart(dias_tipo, use_container_width=True)