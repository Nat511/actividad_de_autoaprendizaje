import pandas as pd
import streamlit as st
import numpy as np

# Cargar el dataset con las nuevas columnas
df = pd.read_csv('df/datos_sin_atipicos.csv', delimiter=',', encoding='latin1')

# Mostrar el dataset original
st.write("### Dataset Original")
st.dataframe(df)

# Agregaciones basadas en las nuevas columnas

# 1. Agregación simple por region y powertrain mostrando la suma de sales_volume
ventas_por_region_powertrain = df.groupby(["region", "powertrain"])["sales_volume"].sum().reset_index()
st.write("### Ventas totales por región y tipo de motorización (powertrain)")
st.dataframe(ventas_por_region_powertrain)

# 2. Agregación múltiple con category y year, mostrando la suma y el promedio de price y range_km
precio_y_rango_por_categoria = df.groupby(["category", "year"]).agg(
    Total_Precio=('price', 'sum'),
    Promedio_Rango=('range_km', 'mean')
).reset_index()
st.write("### Suma de precios y promedio de rango por categoría y año")
st.dataframe(precio_y_rango_por_categoria)

# 3. Agregación con múltiples funciones: Ventas y Eficiencia Energética por parameter y mode
ventas_y_eficiencia_por_parametro = df.groupby(['parameter', 'mode']).agg(
    Total_Ventas=('sales_volume', 'sum'),
    Promedio_Eficiencia=('energy_efficiency', 'mean')
).reset_index()
st.write("### Suma de Ventas y Promedio de Eficiencia Energética por Parámetro y Modo:")
st.dataframe(ventas_y_eficiencia_por_parametro)

# Nuevos campos y variables derivadas

# 4. Crear una variable de Ganancia (asumida como diferencia entre price y costs si es aplicable)
df['Ganancia'] = df['price'] - (df['price'] * 0.3)  # Ejemplo de cálculo con 30% de costos
st.write("### Después de crear el nuevo campo Ganancia")
st.dataframe(df[['category', 'price', 'Ganancia']])

# 5. Crear una variable categórica Rentabilidad basada en Ganancia
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

# 6. Crear una variable Costo_Por_Venta como la relación entre price y sales_volume
df['Costo_Por_Venta'] = df['price'] / df['sales_volume']
st.write("### Después de Crear la Variable 'Costo_Por_Venta':")
st.dataframe(df[['category', 'price', 'sales_volume', 'Costo_Por_Venta']])

# 7. Crear una variable Precio_Efectivo que aplique un descuento del 10% a productos con un rango mayor a 400 km
df['Precio_Efectivo'] = df.apply(lambda row: row['price'] * 0.9 if row['range_km'] > 400 else row['price'], axis=1)
st.write("### Después de Crear la Variable 'Precio Efectivo':")
st.dataframe(df[['category', 'price', 'range_km', 'Precio_Efectivo']])

# Agregaciones específicas para las nuevas columnas
# 8. Agregación por powertrain y year mostrando la suma de co2_saved y el promedio de battery_capacity
co2_y_bateria_por_motorizacion = df.groupby(["powertrain", "year"]).agg(
    Total_CO2_Saved=('co2_saved', 'sum'),
    Promedio_Capacidad_Bateria=('battery_capacity', 'mean')
).reset_index()
st.write("### Suma de CO2 Ahorrado y Promedio de Capacidad de Batería por Tipo de Motorización y Año:")
st.dataframe(co2_y_bateria_por_motorizacion)