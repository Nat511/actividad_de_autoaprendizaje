import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.experimental import enable_iterative_imputer  # Necesario para activar el iterador
from sklearn.impute import IterativeImputer
import streamlit as st

# Cargar el DataFrame con valores faltantes
df = pd.read_csv('df/IEA Global EV Data 2024 full.csv', delimiter=',', encoding='latin1')

st.title("Imputación de Datos Faltantes en el Dataset de EV Global 2024")

st.subheader("Datos Originales con Valores Faltantes:")
st.write(df)

# Crear una copia del dataset para el proceso de MICE
df_copy2 = df.copy()

# Definir las columnas numéricas para la imputación
columnas_numericas = ['year','value','price', 'range_km', 'charging_time', 'sales_volume', 'co2_saved', 
                      'battery_capacity', 'energy_efficiency', 'weight_kg', 
                      'number_of_seats', 'motor_power', 'distance_traveled']

# Imputación simple usando la media
imputer = SimpleImputer(strategy='mean')
df[columnas_numericas] = imputer.fit_transform(df[columnas_numericas])

# Mostrar el dataset después de la imputación simple
st.subheader("Datos Después de la Imputación Simple:")
st.write(df)

# Imputación usando MICE (IterativeImputer)
df_mice = df_copy2.copy()
imputer_mice = IterativeImputer(max_iter=10, random_state=0)
df_mice[columnas_numericas] = imputer_mice.fit_transform(df_mice[columnas_numericas])

# Mostrar el dataset después de la imputación MICE
st.subheader("Datos Después de la Imputación MICE:")
st.write(df_mice)
