import streamlit as st
import pandas as pd  # corregido de dp a pd

st.title('Análisis de Datos')

# Se corrige el tipo de archivo esperado
uploaded_file = st.file_uploader('Subir Archivo CSV', type=['csv'])

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
    st.write(df.dtypes)  # Corregido: muestra los tipos de datos correctos

    st.subheader('Tamaño del dataset')
    st.write(df.shape)  # Muestra el tamaño correcto del dataset (filas, columnas)

    st.subheader('Valores nulos por columna')
    st.write(df.isnull().sum())  # Corregido: cuenta los valores nulos por columna

    st.subheader('Número de filas duplicadas')
    st.write(df.duplicated().sum())  # Corregido: cuenta el número de filas duplicadas
else:
    st.write('Por favor sube un archivo CSV')