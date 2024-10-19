import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler, StandardScaler
import plotly.express as px

# Configurar la página
st.set_page_config(layout="wide")

# Cargar el DataFrame desde un archivo CSV
df = pd.read_csv('df/datos_sin_atipicos.csv', delimiter=',', encoding='latin1')

# Revisar si las columnas numéricas están presentes y no contienen valores no numéricos
columnas_numericas = [
     'price', 'range_km', 'charging_time', 'sales_volume', 'co2_saved', 
    'battery_capacity', 'energy_efficiency', 'weight_kg', 'number_of_seats', 'motor_power', 
    'distance_traveled'
]

# Filtrar solo las columnas numéricas que deseas normalizar
df_numerico = df[columnas_numericas].copy()

# Reemplazar valores faltantes en las columnas numéricas con la media (puedes usar otro método si prefieres)
df_numerico.fillna(df_numerico.mean(), inplace=True)

# Título de la aplicación
st.title("Normalización y Estandarización de Datos con Gráficos de Distribución")

# Mostrar el dataset original
st.subheader("Dataset Original")
st.dataframe(df_numerico)

# 1. Normalización Min-Max
scaler_minmax = MinMaxScaler()
df_minmax = pd.DataFrame(scaler_minmax.fit_transform(df_numerico), columns=df_numerico.columns)

# 2. Estandarización Z-Score (StandardScaler)
scaler_standard = StandardScaler()
df_standard = pd.DataFrame(scaler_standard.fit_transform(df_numerico), columns=df_numerico.columns)

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

# Gráficos de distribución (Gaussianas) para los datos originales y transformados
st.subheader("Distribución de los Datos Antes y Después de la Transformación")

# Distribución de los datos originales
# c1, c2, c3 = st.columns(3)
# with c1:
#     st.write("Original - [Precio]")
#     fig = plot_distribution(df_numerico['price'], "Distribución Precio Original")
#     st.pyplot(fig)

# with c2:
#     st.write("Original - Ventas")
#     fig = plot_distribution(df_numerico['sales_volume'], "Distribución Ventas Original")
#     st.pyplot(fig)

# with c3:
#     st.write("Original - Inventario")
#     fig = plot_distribution(df_numerico['battery_capacity'], "Distribución Inventario Original")
#     st.pyplot(fig)

# Selecciona las primeras tres columnas que deseas mostrar
columnas_a_mostrar = df_numerico.columns[:3]

# Crear columnas en Streamlit para mostrar gráficos y nombres
c1, c2, c3 = st.columns(3)

# Muestra automáticamente cada gráfico y nombre de columna en cada sección
for col, container in zip(columnas_a_mostrar, [c1, c2, c3]):
    with container:
        st.write(f"Original - [{col}]")
        fig = plot_distribution(df_numerico[col], f"Distribución {col} Original")
        st.pyplot(fig)


# Distribución de los datos después de la normalización Min-Max
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

# Distribución de los datos después de la estandarización Z-Score
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

# Gráficos Boxplot antes y después de las transformaciones
st.subheader("Boxplot de Datos Antes y Después de la Transformación")

# Boxplot original
fig_box_original = px.box(df_numerico, title="Boxplot Datos Originales")

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

# Opción para descargar los datos sin outliers como archivos CSV
st.subheader("Descargar Datos Normalizados y Estandarizados")

# Convertir los DataFrames a CSV
csv_minmax = df_minmax.to_csv(index=False).encode('utf-8')
csv_standard = df_standard.to_csv(index=False).encode('utf-8')

# Botones de descarga
st.download_button(label="Descargar CSV Normalización Min-Max", data=csv_minmax, file_name='datos_normalizados_minmax.csv', mime='text/csv')
st.download_button(label="Descargar CSV Estandarización Z-Score", data=csv_standard, file_name='datos_estandarizados_zscore.csv', mime='text/csv')