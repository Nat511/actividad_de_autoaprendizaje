import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.experimental import enable_iterative_imputer  # Necesario para activar el iterador
from sklearn.impute import IterativeImputer
import streamlit as st

df = pd.read_csv('df/IEA Global EV Data 2024 full.csv', delimiter=',', encoding='latin1')

st.title("Imputación de Datos Faltantes en el Dataset de EV Global 2024")

st.subheader("Datos Originales con Valores Faltantes:")
st.write(df)

df_copy2 = df.copy()

columnas_numericas = ['year','value','price', 'range_km', 'charging_time', 'sales_volume', 'co2_saved', 
                      'battery_capacity', 'energy_efficiency', 'weight_kg', 
                      'number_of_seats', 'motor_power', 'distance_traveled']

imputer = SimpleImputer(strategy='mean')
df[columnas_numericas] = imputer.fit_transform(df[columnas_numericas])

st.subheader("Datos Después de la Imputación Simple:")
st.write(df)

csv_simple = df.to_csv(index=False).encode('utf-8')
st.download_button(label="Descargar CSV con Imputación Simple", data=csv_simple, file_name='datos_imputacion_simple.csv', mime='text/csv')

df_mice = df_copy2.copy()
imputer_mice = IterativeImputer(max_iter=10, random_state=0)
df_mice[columnas_numericas] = imputer_mice.fit_transform(df_mice[columnas_numericas])

st.subheader("Datos Después de la Imputación MICE:")
st.write(df_mice)

csv_mice = df_mice.to_csv(index=False).encode('utf-8')
st.download_button(label="Descargar CSV con Imputación MICE", data=csv_mice, file_name='datos_imputacion_mice.csv', mime='text/csv')