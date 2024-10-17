import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler, MaxAbsScaler, Normalizer, StandardScaler, RobustScaler
import plotly.express as px

# Configurar la página
st.set_page_config(layout="wide")

# Título de la aplicación
st.title("Normalización y Estandarización de Datos con Gráficos de Distribución")

df = pd.read_csv('datos_sin_atipicos.csv',delimiter=',', encoding='utf-8')
df= df.drop('Producto', axis=1)
# Mostrar el dataset original
st.subheader("Dataset Original")
st.dataframe(df)

# 1. Normalización Min-Max
scaler_minmax = MinMaxScaler()
df_minmax = pd.DataFrame(scaler_minmax.fit_transform(df), columns=df.columns)

# 2. Estandarización Z-Score (StandardScaler)
scaler_standard = StandardScaler()
df_standard = pd.DataFrame(scaler_standard.fit_transform(df), columns=df.columns)

# Mostrar los DataFrames transformados en Streamlit
st.subheader("Datos Normalizados y Estandarizados")

with st.expander("Normalización Min-Max"):
    st.dataframe(df_minmax)

with st.expander("Estandarización Z-Score (StandardScaler)"):
    st.dataframe(df_standard)



# Función para mostrar gráficos de distribución (Gaussianas)
def plot_distribution(data, title):
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(data, kde=True, ax=ax)
    ax.set_title(title)
    return fig

# Gráficos de distribución (Gaussianas) para los datos original y transformados
st.subheader("Distribución de los Datos Antes y Después de la Transformación")

# Distribución de los datos originales
c1, c2, c3 = st.columns(3)
with c1:
    st.write("Original")
    fig = plot_distribution(df['Precio'], "Distribución Precio Original")
    st.pyplot(fig)

with c2:
    st.write("Original")
    fig = plot_distribution(df['Ventas_Mensuales'], "Distribución Ventas Original")
    st.pyplot(fig)

with c3:
    st.write("Original")
    fig = plot_distribution(df['Inventario_Disponible'], "Distribución Inventario Original")
    st.pyplot(fig)
    
    

# Distribución de los datos después de la normalización Min-Max
st.subheader("Distribución después de Normalización Min-Max")

c1, c2, c3 = st.columns(3)
with c1:
    fig = plot_distribution(df_minmax['Precio'], "Distribución Precio (Min-Max)")
    st.pyplot(fig)

with c2:
    fig = plot_distribution(df_minmax['Ventas_Mensuales'], "Distribución Ventas (Min-Max)")
    st.pyplot(fig)

with c3:
    fig = plot_distribution(df_minmax['Inventario_Disponible'], "Distribución Inventario (Min-Max)")
    st.pyplot(fig)


# Distribución de los datos después de la estandarización Z-Score
st.subheader("Distribución después de Estandarización Z-Score")

c1, c2, c3 = st.columns(3)
with c1:
    fig = plot_distribution(df_standard['Precio'], "Distribución Precio (Z-Score)")
    st.pyplot(fig)

with c2:
    fig = plot_distribution(df_standard['Ventas_Mensuales'], "Distribución Ventas (Z-Score)")
    st.pyplot(fig)

with c3:
    fig = plot_distribution(df_standard['Inventario_Disponible'], "Distribución Inventario (Z-Score)")
    st.pyplot(fig)



# Gráficos Boxplot antes y después de las transformaciones
st.subheader("Boxplot de Datos Antes y Después de la Transformación")

# Boxplot original
fig_box_original = px.box(df, title="Boxplot Datos Originales")

# Boxplot después de la normalización Min-Max
fig_box_minmax = px.box(df_minmax, title="Boxplot Datos (Normalización Min-Max)")

# Boxplot después de la estandarización Z-Score
fig_box_standard = px.box(df_standard, title="Boxplot Datos (Estandarización Z-Score)")

# Mostrar boxplots en columnas
c1, c2, c3 = st.columns(3)
with c1:
    st.plotly_chart(fig_box_original)

with c2:
    st.plotly_chart(fig_box_minmax)

with c3:
    st.plotly_chart(fig_box_standard)
