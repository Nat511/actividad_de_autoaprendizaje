import streamlit as st
import pandas as pd
import numpy as np

df = pd.read_csv('df/IEA Global EV Data 2024 full.csv', delimiter=',', encoding='latin1')


# Mostrar el dataset original
st.write("Datos originales con valores faltantes:")
st.dataframe(df)



# Eliminar filas con cualquier valor faltante
df_sin_filas_nulas = df.dropna(how='any')
st.subheader("Datos después de eliminar filas con valores faltantes:")
st.dataframe(df_sin_filas_nulas)

# Eliminar columnas con cualquier valor faltante
df_sin_columnas_nulas = df.dropna(axis=1, how='any')
st.subheader("Datos después de eliminar columnas con valores faltantes:")
st.dataframe(df_sin_columnas_nulas)

# 3. Imputar valores faltantes con valores por defecto
df_fill_default = df.fillna({
    'Precio': 100,  # Rellenar valores faltantes en 'Precio' con 100
    'Ventas_Mensuales': 0,  # Rellenar valores faltantes en 'Ventas_Mensuales' con 0
    'Inventario_Disponible': 0  # Rellenar valores faltantes en 'Inventario_Disponible' con 0
})

# Mostrar el dataset después de rellenar con valores por defecto
st.write("Datos después de rellenar valores faltantes con valores por defecto:")
st.dataframe(df_fill_default)

# Guardar el DataFrame en un archivo CSV
if st.button('Guardar CSV'):
    file_path = 'df/datos_rellenados.csv'  # Cambia la ruta según sea necesario
    df_fill_default.to_csv(file_path, index=False)
    st.success(f'Dataset guardado en {file_path}')