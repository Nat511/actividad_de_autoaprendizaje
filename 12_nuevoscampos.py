import pandas as pd
import streamlit as st
import numpy as np

# Crear un DataFrame con 5 vendedores, 10 productos y 50 registros

# Generar datos extendidos a 50 registros
vendedores = np.random.choice(['Carlos', 'Maria', 'Luis', 'Ana', 'Pedro'], 50)
productos = np.random.choice(['Bicicleta', 'Casco', 'Guantes', 'Rodilleras', 'Luz', 'Cadena', 'Frenos', 'Timbre', 'Manillar', 'Sillin'], 50)
regiones = np.random.choice(['Norte', 'Sur'], 50)
ventas = np.random.randint(100, 500, 50)
costos = ventas * np.random.uniform(0.6, 0.9, 50)

# Crear DataFrame de ejemplo con 50 registros
df = pd.DataFrame({
    'Vendedor': vendedores,
    'Producto': productos,
    'Región': regiones,
    'Ventas': ventas,
    'Costos': costos
})

# Mostrar el dataset original
st.write("### Dataset Original con 50 registros:")
st.dataframe(df)


##Agregacion simple
ventas_por_vendedor=df.groupby("Vendedor")["Ventas"].sum().reset_index()
st.write("Ventasa totales por vendedor")
st.dataframe(ventas_por_vendedor)

ventas_agrupadas=df.groupby(["Vendedor","Región"])["Ventas"].agg(['sum','mean']).reset_index()
st.write("SUMA y promedio de ventas por vendedor y region")
st.dataframe(ventas_agrupadas)

# --- Ejemplo 3: Agregación con múltiples funciones ---
ventas_costos = df.groupby('Vendedor').agg(
    Total_Ventas=('Ventas', 'sum'),
    Total_Costos=('Costos', 'sum'),
    Promedio_Ventas=('Ventas', 'mean')
).reset_index()
st.write("### Suma de Ventas y Costos, y Promedio de Ventas por Vendedor:")
st.dataframe(ventas_costos)

#nuevos campos
#crear variable ganancia
df['Ganancia']=df['Ventas']-df['Costos']
st.write("### Despues de crear el nuevo campo ganancia")
st.dataframe(df)

#creacion de variables categoricas
def clasificar_rentabilidad(g):
    if(g>200):
        return 'alta'
    elif(g>100):
        return 'media'
    else:
        return 'baja'

df['Rentabiidad']=df['Ganancia'].apply(clasificar_rentabilidad)
st.write("### crear el campo categorico rentabilidad")
st.dataframe(df)

 #3. Crear una variable 'Costo_Por_Venta' (Costos / Ventas)
df['Costo_Por_Venta'] = df['Costos'] / df['Ventas']
st.write("### Después de Crear la Variable 'Costo_Por_Venta':")
st.dataframe(df[['Producto', 'Costos', 'Ventas', 'Costo_Por_Venta']])

# 4. Crear una variable 'Precio_Efectivo' que aplique un descuento del 10% a productos con ventas mayores a 300
df['Precio_Efectivo'] = df.apply(lambda row: row['Ventas'] * 0.9 if row['Ventas'] > 300 else row['Ventas'], axis=1)
st.write("### Después de Crear la Variable 'Precio Efectivo':")
st.dataframe(df[['Producto', 'Ventas', 'Precio_Efectivo']])