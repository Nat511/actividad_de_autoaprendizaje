import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler, StandardScaler
import plotly.express as px

st.set_page_config(layout="wide")

df = pd.read_csv('df/datos_sin_atipicos.csv', delimiter=',', encoding='latin1')

columnas_numericas = ['year','value','price', 'range_km', 'charging_time', 'sales_volume', 'co2_saved', 
                      'battery_capacity', 'energy_efficiency', 'weight_kg', 
                      'number_of_seats', 'motor_power', 'distance_traveled']

df_numerico = df[columnas_numericas].copy()

df_numerico.fillna(df_numerico.mean(), inplace=True)

st.title("Normalización y Estandarización de Datos con Gráficos de Distribución")

st.subheader("Dataset Original")
st.dataframe(df_numerico)

scaler_minmax = MinMaxScaler()
df_minmax = pd.DataFrame(scaler_minmax.fit_transform(df_numerico), columns=df_numerico.columns)

scaler_standard = StandardScaler()
df_standard = pd.DataFrame(scaler_standard.fit_transform(df_numerico), columns=df_numerico.columns)

st.subheader("Datos Normalizados y Estandarizados")

with st.expander("Normalización Min-Max"):
    st.dataframe(df_minmax)

with st.expander("Estandarización Z-Score (StandardScaler)"):
    st.dataframe(df_standard)

def plot_distribution(data, title):
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(data, kde=True, ax=ax)
    ax.set_title(title)
    return fig

st.subheader("Distribución de los Datos Antes y Después de la Transformación")

c1, c2, c3 = st.columns(3)
with c1:
    st.write("Original - [Precio]")
    fig = plot_distribution(df_numerico['price'], "Distribución Precio Original")
    st.pyplot(fig)

with c2:
    st.write("Original - Ventas")
    fig = plot_distribution(df_numerico['sales_volume'], "Distribución Ventas Original")
    st.pyplot(fig)

with c3:
    st.write("Original - Inventario")
    fig = plot_distribution(df_numerico['battery_capacity'], "Distribución Inventario Original")
    st.pyplot(fig)


st.subheader("Distribución después de Normalización Min-Max")

c1, c2, c3 = st.columns(3)
with c1:
    fig = plot_distribution(df_minmax['price'], "Distribución Precio (Min-Max)")
    st.pyplot(fig)

with c2:
    fig = plot_distribution(df_minmax['sales_volume'], "Distribución Ventas (Min-Max)")
    st.pyplot(fig)

with c3:
    fig = plot_distribution(df_minmax['battery_capacity'], "Distribución Inventario (Min-Max)")
    st.pyplot(fig)

st.subheader("Distribución después de Estandarización Z-Score")

c1, c2, c3 = st.columns(3)
with c1:
    fig = plot_distribution(df_standard['price'], "Distribución Precio (Z-Score)")
    st.pyplot(fig)

with c2:
    fig = plot_distribution(df_standard['sales_volume'], "Distribución Ventas (Z-Score)")
    st.pyplot(fig)

with c3:
    fig = plot_distribution(df_standard['battery_capacity'], "Distribución Inventario (Z-Score)")
    st.pyplot(fig)

st.subheader("Boxplot de Datos Antes y Después de la Transformación")

fig_box_original = px.box(df_numerico, title="Boxplot Datos Originales")

fig_box_minmax = px.box(df_minmax, title="Boxplot Datos (Normalización Min-Max)")

fig_box_standard = px.box(df_standard, title="Boxplot Datos (Estandarización Z-Score)")

c1, c2, c3 = st.columns(3)
with c1:
    st.plotly_chart(fig_box_original)

with c2:
    st.plotly_chart(fig_box_minmax)

with c3:
    st.plotly_chart(fig_box_standard)

st.subheader("Descargar Datos Normalizados y Estandarizados")

csv_minmax = df_minmax.to_csv(index=False).encode('utf-8')
csv_standard = df_standard.to_csv(index=False).encode('utf-8')

st.download_button(label="Descargar CSV Normalización Min-Max", data=csv_minmax, file_name='datos_normalizados_minmax.csv', mime='text/csv')
st.download_button(label="Descargar CSV Estandarización Z-Score", data=csv_standard, file_name='datos_estandarizados_zscore.csv', mime='text/csv')