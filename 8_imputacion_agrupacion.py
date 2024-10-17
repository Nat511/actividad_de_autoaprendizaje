import streamlit as st
import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.experimental import enable_iterative_imputer  # Necesario para activar el iterador
from sklearn.impute import IterativeImputer

# Cargar el DataFrame de ejemplo
df = pd.read_csv('df/IEA Global EV Data 2024 full.csv', delimiter=',', encoding='latin1')

# Título de la aplicación
st.title("Eliminación e Imputación de Valores por Región")

# Selección de la región desde un combo box
region_seleccionada = st.selectbox('Seleccione una región', df['region'].unique())

# Filtrar el DataFrame por la región seleccionada
df_filtrado = df[df['region'] == region_seleccionada]

# Mostrar las columnas numéricas disponibles para la eliminación de valores
columnas_numericas = ['year','value','price', 'range_km', 'charging_time',
                        'sales_volume', 'co2_saved', 'battery_capacity', 
                        'energy_efficiency', 'weight_kg','number_of_seats',
                         'motor_power', 'distance_traveled']

columnas_a_eliminar = st.multiselect('Seleccione columnas para eliminar valores', columnas_numericas)

# Selección del porcentaje a eliminar
porcentaje_seleccionado = st.slider('Seleccione el porcentaje de valores a eliminar', min_value=0.1, max_value=0.4, step=0.05)

# Función para eliminar un porcentaje de valores de las columnas seleccionadas
def eliminar_porcentaje_valores(df, columnas, porcentaje):
    df_copy = df.copy()
    for col in columnas:
        total_filas = len(df_copy[col])
        num_eliminar = int(total_filas * porcentaje)
        
        if num_eliminar > 0:
            # Seleccionar índices aleatorios donde eliminar valores
            indices_a_eliminar = np.random.choice(df_copy.index, size=num_eliminar, replace=False)
            # Reemplazar esos valores con NaN
            df_copy.loc[indices_a_eliminar, col] = np.nan

    return df_copy

# Si se seleccionan columnas, aplicar la eliminación de valores
if len(columnas_a_eliminar) > 0:
    # Crear una copia del DataFrame para modificar
    df_modificado = eliminar_porcentaje_valores(df_filtrado, columnas_a_eliminar, porcentaje_seleccionado)

    # Mostrar el DataFrame modificado
    st.write("DataFrame con valores eliminados:")
    st.write(df_modificado)

    # Mostrar el promedio de las columnas originales (antes de la imputación)
    st.subheader("Promedio de las columnas antes de la imputación:")
    for col in columnas_a_eliminar:
        promedio_original = df_filtrado[col].mean()
        st.write(f"Promedio original de {col}: {promedio_original}")
    
    # Imputación de los valores eliminados utilizando MICE
    imputer_mice = IterativeImputer(max_iter=10, random_state=0)
    df_modificado[columnas_a_eliminar] = imputer_mice.fit_transform(df_modificado[columnas_a_eliminar])

    # Redondear los valores imputados a dos decimales
    for col in columnas_a_eliminar:
        df_modificado[col] = df_modificado[col].round(2)

    # Mostrar el promedio de las columnas imputadas
    st.subheader("Promedio de las columnas después de la imputación:")
    for col in columnas_a_eliminar:
        promedio_imputado = df_modificado[col].mean()
        st.write(f"Promedio imputado de {col}: {promedio_imputado}")
        st.write(f"Diferencia del promedio en {col}: {promedio_original-promedio_imputado}")




    # Graficar la comparación de los datos actuales vs imputados usando Seaborn
    st.subheader("Comparación de los datos originales e imputados (distribución con curva de Gauss):")
    
    # Crear una figura para el gráfico
    fig, ax = plt.subplots()

    # Graficar los datos originales e imputados con Seaborn
    for col in columnas_a_eliminar:
        sns.kdeplot(df_filtrado[col], label=f'{col} (Original)', ax=ax)
        sns.kdeplot(df_modificado[col], label=f'{col} (Imputado)', ax=ax)

    # Configurar el gráfico
    ax.set_title("Distribución de los valores originales vs imputados")
    ax.set_xlabel("Valor")
    ax.set_ylabel("Densidad")
    plt.legend()

    # Mostrar el gráfico en Streamlit
    st.pyplot(fig)

    # Opción para descargar el DataFrame modificado
    st.download_button(
        label="Descargar CSV",
        data=df_modificado.to_csv(index=False),
        file_name='datos_modificados.csv',
        mime='text/csv'
    )
else:
    st.write("Seleccione columnas para eliminar valores.")
