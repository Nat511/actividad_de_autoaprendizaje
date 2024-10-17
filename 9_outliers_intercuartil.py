import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import plotly.express as px



st.set_page_config(layout="wide")
# Función para generar datos inventados con algunos valores atípicos
def generar_datos():
    np.random.seed(42)  # Fijar semilla para reproducibilidad
    data = {
        'Producto': ['Guantes', 'Vestido', 'Paraguas', 'Zapatos', 'Lampara'] * 3,
        'Precio': np.random.normal(150, 50, 15).tolist(),
        'Ventas_Mensuales': np.random.normal(70, 20, 15).tolist(),
        'Inventario_Disponible': np.random.randint(1, 10, size=15).tolist()
    }
    data['Precio'][3] = 1000  # Añadir valor atípico en Precio
    data['Ventas_Mensuales'][12] = 5000  # Añadir valor atípico en Ventas_Mensuales
    return pd.DataFrame(data)


# Función para detectar valores atípicos usando el rango intercuartil (IQR)
def eliminar_valores_atipicos(df, column):
    # Calcular el cuartil 1 (Q1) y cuartil 3 (Q3)
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    
    # Definir límites para detectar los outliers
    lower_limit = Q1 - 1.5 * IQR
    upper_limit = Q3 + 1.5 * IQR
    
    # Filtrar los datos que están dentro de los límites
    df_sin_atipicos = df[(df[column] >= lower_limit) & (df[column] <= upper_limit)]
    
    return df_sin_atipicos


# Mostrar los datos originales
st.title('Outlieres con Rango Intercuartil')
st.subheader("Datos originales")

df = generar_datos()
st.dataframe(df)

# Gráficos de distribución (curvas de Gauss) y boxplots antes de eliminar outliers
st.subheader("Gráficos antes de eliminar valores atípicos")

# Curvas de Gauss
fig, ax = plt.subplots(1, 2, figsize=(10, 5))
sns.histplot(df['Precio'], kde=True, ax=ax[0])
ax[0].set_title('Distribución Precio (Original)')
sns.histplot(df['Ventas_Mensuales'], kde=True, ax=ax[1])
ax[1].set_title('Distribución Ventas Mensuales (Original)')
st.pyplot(fig)



# Gráfico de cajas (Boxplot) con Plotly Express
fig_box_precio = px.box(df, y='Precio', title="Boxplot Precio (Original)")
fig_box_ventas = px.box(df, y='Ventas_Mensuales', title="Boxplot Ventas Mensuales (Original)")

c1,c2= st.columns(2)
with c1:
    st.plotly_chart(fig_box_precio)
with c2:
    st.plotly_chart(fig_box_ventas)





# Eliminar valores atípicos en la columna 'Precio'
df_sin_atipicos_precio = eliminar_valores_atipicos(df, 'Precio')

# Eliminar valores atípicos en la columna 'Ventas_Mensuales'
df_sin_atipicos_ventas = eliminar_valores_atipicos(df, 'Ventas_Mensuales')

# Mostrar los datos después de eliminar valores atípicos
st.subheader("Datos después de eliminar valores atípicos")
c1,c2=st.columns(2)
with c1:
    st.dataframe(df_sin_atipicos_precio)
with c2:
    st.dataframe(df_sin_atipicos_ventas)

# Gráficos de distribución (curvas de Gauss) y boxplots después de eliminar outliers
st.subheader("Gráficos después de eliminar valores atípicos")

# Curvas de Gauss
fig, ax = plt.subplots(1, 2, figsize=(10, 5))
sns.histplot(df_sin_atipicos_precio['Precio'], kde=True, ax=ax[0])
ax[0].set_title('Distribución Precio (Sin Outliers)')
sns.histplot(df_sin_atipicos_ventas['Ventas_Mensuales'], kde=True, ax=ax[1])
ax[1].set_title('Distribución Ventas Mensuales (Sin Outliers)')
st.pyplot(fig)



c1,c2= st.columns(2)
with c1:
    fig_box_precio_sin = px.box(df_sin_atipicos_precio, y='Precio', title="Boxplot Precio (Sin Outliers)")
    st.plotly_chart(fig_box_precio_sin)
with c2:
    fig_box_ventas_sin = px.box(df_sin_atipicos_ventas, y='Ventas_Mensuales', title="Boxplot Ventas Mensuales (Sin Outliers)")
    st.plotly_chart(fig_box_ventas_sin)





# Guardar los resultados en archivos CSV
df_sin_atipicos_precio.to_csv('datos_sin_atipicos_precio.csv', index=False)
df_sin_atipicos_ventas.to_csv('datos_sin_atipicos_ventas.csv', index=False)