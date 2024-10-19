import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Configurar la página
st.set_page_config(layout="wide")

# Leer los datos
@st.cache_data  # Cachear la lectura del archivo para mejorar el rendimiento
def load_data(file_path):
    try:
        return pd.read_csv(file_path, delimiter=',', encoding='latin1')
    except Exception as e:
        st.error(f"Error al cargar los datos: {e}")
        return pd.DataFrame()  # Devolver un DataFrame vacío en caso de error

df = load_data('df/datos_imputacion_mice.csv')  # Cambia el nombre por la ruta de tu archivo si es necesario

# Verificar si los datos se han cargado correctamente
if df.empty:
    st.stop()

# Definir las columnas numéricas
columnas_numericas = ['year', 'value', 'price', 'range_km', 'charging_time', 'sales_volume', 'co2_saved', 
                      'battery_capacity', 'energy_efficiency', 'weight_kg', 
                      'number_of_seats', 'motor_power', 'distance_traveled']

# Función para aplicar la transformación logarítmica
def transformar_logaritmicamente(df, columnas):
    for column in columnas:
        # Verificar si hay valores negativos o cero en la columna
        if (df[column] <= 0).any():
            st.warning(f"La columna {column} contiene valores cero o negativos. Transformación logarítmica no será posible en esos casos.")
            # Reemplazar valores cero o negativos por NaN
            df['Log_' + column] = np.log(df[column].replace({0: np.nan, -np.inf: np.nan}))
        else:
            df['Log_' + column] = np.log(df[column])
    return df

# Función para calcular el Z-Score de los datos transformados
def calcular_z_score_log(df, columnas):
    for column in columnas:
        col_log = 'Log_' + column
        if col_log in df:
            mean = df[col_log].mean()
            std = df[col_log].std()
            df['z_score_log_' + column] = (df[col_log] - mean) / std
    return df

# Función para eliminar outliers basados en Z-Score
def eliminar_outliers_z_score(df, columnas, threshold=3):
    condiciones = [(df['z_score_log_' + col] >= -threshold) & (df['z_score_log_' + col] <= threshold) for col in columnas if 'z_score_log_' + col in df]
    if condiciones:
        condicion_final = np.logical_and.reduce(condiciones)
        df = df[condicion_final]
    return df

# Función para generar un archivo CSV para descargar
def convertir_csv(df):
    return df.to_csv(index=False).encode('utf-8')

def main():
    st.title('Detección de Outliers con Transformación Logarítmica y Z-Score')
    
    st.subheader('Datos Originales')
    st.dataframe(df)
    
    # Transformar logarítmicamente todas las columnas numéricas
    df_transformado = transformar_logaritmicamente(df.copy(), columnas_numericas)
    
    st.subheader('Datos Originales Transformados')
    st.dataframe(df_transformado)
    
    # Calcular el Z-Score en los datos transformados
    df_zscore = calcular_z_score_log(df_transformado.copy(), columnas_numericas)
    
    st.subheader('Datos Transformados con Logaritmo y Z-Score')
    st.dataframe(df_zscore)
    
    # Eliminar outliers usando Z-Score en todas las columnas numéricas
    df_sin_outliers = eliminar_outliers_z_score(df_zscore.copy(), columnas_numericas)
    
    # Mostrar los datos después de eliminar outliers
    st.subheader("Datos después de eliminar outliers basados en Z-Score (Logaritmo)")
    st.dataframe(df_sin_outliers)
    
    # Botón para descargar los datos
    csv = convertir_csv(df_sin_outliers)
    st.download_button(
        label="Descargar datos sin outliers como CSV",
        data=csv,
        file_name='datos_sin_outliers.csv',
        mime='text/csv'
    )
    
    # Gráfico de Boxplot antes y después de eliminar outliers
    st.subheader("Boxplot de Columnas Numéricas antes y después de eliminar outliers")
    
    # Visualizar los boxplots para cada columna numérica
    for column in columnas_numericas:
        if column in df and column in df_sin_outliers:
            fig_box_antes = px.box(df, y=column, title=f"Boxplot {column} (Original)")
            fig_box_despues = px.box(df_sin_outliers, y=column, title=f"Boxplot {column} (Sin Outliers)")
            
            c1, c2 = st.columns(2)
            with c1:
                st.plotly_chart(fig_box_antes)
            with c2:
                st.plotly_chart(fig_box_despues)

if __name__ == "__main__":
    main()
