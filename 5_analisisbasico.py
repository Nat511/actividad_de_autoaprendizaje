import streamlit as st
import pandas as pd

st.title('Análisis de Datos')

# Subir archivo CSV
uploaded_file = st.file_uploader('Subir Archivo CSV', type=['csv'])

def detectar_columnas_con_outliers(df):
    """
    Detecta columnas con valores atípicos en un DataFrame usando el rango intercuartil (IQR).
    Retorna una lista de columnas que contienen outliers.
    """
    columnas_con_outliers = []

    # Recorremos solo las columnas numéricas
    for column in df.select_dtypes(include='number').columns:
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1

        # Definir límites para detectar outliers
        lower_limit = Q1 - 1.5 * IQR
        upper_limit = Q3 + 1.5 * IQR

        # Verificar si hay algún valor fuera de los límites
        if df[(df[column] < lower_limit) | (df[column] > upper_limit)].shape[0] > 0:
            columnas_con_outliers.append(column)

    return columnas_con_outliers

if uploaded_file is not None:
    # Cargar el archivo CSV
    df = pd.read_csv(uploaded_file, encoding='latin-1', delimiter=',')
    
    st.subheader('Primeras filas del dataset')
    st.dataframe(df.head())

    st.subheader('Resumen estadístico')
    st.write(df.describe())

    st.subheader('Nombres de las columnas')
    st.write(df.columns)

    st.subheader('Tipos de datos')
    st.write(df.dtypes)

    st.subheader('Tamaño del dataset')
    st.write(df.shape)

    st.subheader('Valores nulos por columna')
    st.write(df.isnull().sum())

    st.subheader('Número de filas duplicadas')
    st.write(df.duplicated().sum())

    # Detectar y mostrar columnas con outliers
    columnas_con_outliers = detectar_columnas_con_outliers(df)
    st.subheader('Columnas con datos atípicos (Outliers)')
    if columnas_con_outliers:
        st.write(columnas_con_outliers)
    else:
        st.write('No se encontraron columnas con outliers.')
else:
    st.write('Por favor sube un archivo CSV')
