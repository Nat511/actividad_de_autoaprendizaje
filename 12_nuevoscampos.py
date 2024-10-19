import pandas as pd
import streamlit as st
import numpy as np

df = pd.read_csv('df/datos_sin_atipicos.csv', delimiter=',', encoding='latin1')

st.write("### Dataset Original")
st.dataframe(df)

ventas_por_region_powertrain = df.groupby(["region", "powertrain"])["sales_volume"].sum().reset_index()
st.write("### Ventas totales por región y tipo de motorización (powertrain)")
st.dataframe(ventas_por_region_powertrain)

precio_y_rango_por_categoria = df.groupby(["category", "year"]).agg(
    Total_Precio=('price', 'sum'),
    Promedio_Rango=('range_km', 'mean')
).reset_index()
st.write("### Suma de precios y promedio de rango por categoría y año")
st.dataframe(precio_y_rango_por_categoria)

ventas_y_eficiencia_por_parametro = df.groupby(['parameter', 'mode']).agg(
    Total_Ventas=('sales_volume', 'sum'),
    Promedio_Eficiencia=('energy_efficiency', 'mean')
).reset_index()
st.write("### Suma de Ventas y Promedio de Eficiencia Energética por Parámetro y Modo:")
st.dataframe(ventas_y_eficiencia_por_parametro)


df['Ganancia'] = df['price'] - (df['price'] * 0.3)  #n 30% de costos
st.write("### Después de crear el nuevo campo Ganancia")
st.dataframe(df[['category', 'price', 'Ganancia']])

def clasificar_rentabilidad(g):
    if g > 200:
        return 'alta'
    elif g > 100:
        return 'media'
    else:
        return 'baja'

df['Rentabilidad'] = df['Ganancia'].apply(clasificar_rentabilidad)
st.write("### Crear el campo categórico Rentabilidad")
st.dataframe(df[['category', 'Ganancia', 'Rentabilidad']])

df['Costo_Por_Venta'] = df['price'] / df['sales_volume']
st.write("### Después de Crear la Variable 'Costo_Por_Venta':")
st.dataframe(df[['category', 'price', 'sales_volume', 'Costo_Por_Venta']])

df['Precio_Efectivo'] = df.apply(lambda row: row['price'] * 0.9 if row['range_km'] > 400 else row['price'], axis=1)
st.write("### Después de Crear la Variable 'Precio Efectivo':")
st.dataframe(df[['category', 'price', 'range_km', 'Precio_Efectivo']])

co2_y_bateria_por_motorizacion = df.groupby(["powertrain", "year"]).agg(
    Total_CO2_Saved=('co2_saved', 'sum'),
    Promedio_Capacidad_Bateria=('battery_capacity', 'mean')
).reset_index()
st.write("### Suma de CO2 Ahorrado y Promedio de Capacidad de Batería por Tipo de Motorización y Año:")
st.dataframe(co2_y_bateria_por_motorizacion)