
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import plotly.express as px

st.set_page_config(layout="wide")

# Función para detectar valores atípicos usando el rango intercuartil (IQR) para múltiples columnas
def eliminar_valores_atipicos_multiples(df, columns):
    """
    Elimina los valores atípicos de múltiples columnas de un DataFrame usando el rango intercuartil (IQR).
    Parámetros:
        df (DataFrame): El DataFrame original.
        columns (list): Lista de nombres de columnas donde eliminar los outliers.
    Retorno:
        DataFrame sin valores atípicos en las columnas especificadas.
    """
    df_sin_atipicos = df.copy()  # Crear una copia para no modificar el original

    for column in columns:
        # Calcular cuartiles y límites
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_limit = Q1 - 1.5 * IQR
        upper_limit = Q3 + 1.5 * IQR

        # Filtrar valores dentro de los límites
        df_sin_atipicos = df_sin_atipicos[(df_sin_atipicos[column] >= lower_limit) & (df_sin_atipicos[column] <= upper_limit)]
    
    return df_sin_atipicos

# Leer los datos originales
st.title('Outliers con Rango Intercuartil')
st.subheader("Datos originales")

df = pd.read_csv('df/IEA Global EV Data 2024 full.csv', delimiter=',', encoding='latin1')
st.dataframe(df)

# Columnas que deseas analizar y eliminar outliers
columnas_a_analizar = ['price', 'sales_volume', 'range_km', 'charging_time', 'sales_volume', 'co2_saved', 
                      'battery_capacity', 'energy_efficiency', 'weight_kg', 
                      'number_of_seats', 'motor_power', 'distance_traveled']

# Mostrar gráficos antes de eliminar valores atípicos
st.subheader("Gráficos antes de eliminar valores atípicos")

# Curvas de Gauss antes de eliminar outliers
fig, ax = plt.subplots(1, len(columnas_a_analizar), figsize=(10, 5))
for i, column in enumerate(columnas_a_analizar):
    sns.histplot(df[column], kde=True, ax=ax[i])
    ax[i].set_title(f'Distribución {column} (Original)')
st.pyplot(fig)

# Gráficos de Boxplot antes de eliminar outliers
for column in columnas_a_analizar:
    st.plotly_chart(px.box(df, y=column, title=f"Boxplot {column} (Original)"))

# Eliminar valores atípicos en múltiples columnas
df_sin_atipicos = eliminar_valores_atipicos_multiples(df, columnas_a_analizar)

# Mostrar los datos después de eliminar valores atípicos
st.subheader("Datos después de eliminar valores atípicos")
st.dataframe(df_sin_atipicos)

# Gráficos después de eliminar outliers
st.subheader("Gráficos después de eliminar valores atípicos")

# Curvas de Gauss después de eliminar outliers
fig, ax = plt.subplots(1, len(columnas_a_analizar), figsize=(10, 5))
for i, column in enumerate(columnas_a_analizar):
    sns.histplot(df_sin_atipicos[column], kde=True, ax=ax[i])
    ax[i].set_title(f'Distribución {column} (Sin Outliers)')
st.pyplot(fig)

# Gráficos de Boxplot después de eliminar outliers
for column in columnas_a_analizar:
    st.plotly_chart(px.box(df_sin_atipicos, y=column, title=f"Boxplot {column} (Sin Outliers)"))

# Guardar los resultados en un solo archivo CSV
df_sin_atipicos.to_csv('datos_sin_atipicos.csv', index=False)
st.success("Datos procesados y guardados en 'datos_sin_atipicos.csv'")
