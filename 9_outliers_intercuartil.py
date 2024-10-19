import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

st.set_page_config(layout="wide")
df = pd.read_csv('df/datos_imputacion_mice.csv', delimiter=',', encoding='latin1')

# Función para detectar valores atípicos usando el rango intercuartil (IQR) en múltiples columnas
def eliminar_valores_atipicos_multiple(df, columns):
    df_clean = df.copy()
    for column in columns:
        # Calcular el cuartil 1 (Q1) y cuartil 3 (Q3)
        Q1 = df_clean[column].quantile(0.25)
        Q3 = df_clean[column].quantile(0.75)
        IQR = Q3 - Q1

        # Definir límites para detectar los outliers
        lower_limit = Q1 - 1.5 * IQR
        upper_limit = Q3 + 1.5 * IQR

        # Filtrar los datos que están dentro de los límites
        df_clean = df_clean[(df_clean[column] >= lower_limit) & (df_clean[column] <= upper_limit)]
    return df_clean

# Mostrar los datos originales
st.title('Outlieres con Rango Intercuartil')
st.subheader("Datos originales")
st.dataframe(df)

# Gráficos de distribución (curvas de Gauss) y boxplots antes de eliminar outliers
st.subheader("Gráficos antes de eliminar valores atípicos")
fig, ax = plt.subplots(1, 2, figsize=(10, 5))
sns.histplot(df['energy_efficiency'], kde=True, ax=ax[0])
ax[0].set_title('Distribución energy_efficiency (Original)')
sns.histplot(df['co2_saved'], kde=True, ax=ax[1])
ax[1].set_title('Distribución co2_saved (Original)')
st.pyplot(fig)

# Gráfico de cajas (Boxplot) con Plotly Express
fig_box_energy_efficiency = px.box(df, y='energy_efficiency', title="Boxplot energy_efficiency (Original)")
fig_box_co2_saved = px.box(df, y='co2_saved', title="Boxplot co2_saved (Original)")

c1, c2 = st.columns(2)
with c1:
    st.plotly_chart(fig_box_energy_efficiency)
with c2:
    st.plotly_chart(fig_box_co2_saved)

# Eliminar valores atípicos en las columnas 'energy_efficiency' y 'co2_saved'
columns_to_clean = ['energy_efficiency', 'co2_saved']
df_sin_atipicos = eliminar_valores_atipicos_multiple(df, columns_to_clean)

# Mostrar los datos después de eliminar valores atípicos
st.subheader("Datos después de eliminar valores atípicos en ambas columnas")
st.dataframe(df_sin_atipicos)

# Gráficos de distribución (curvas de Gauss) después de eliminar outliers
st.subheader("Gráficos después de eliminar valores atípicos")
fig, ax = plt.subplots(1, 2, figsize=(10, 5))
sns.histplot(df_sin_atipicos['energy_efficiency'], kde=True, ax=ax[0])
ax[0].set_title('Distribución energy_efficiency (Sin Outliers)')
sns.histplot(df_sin_atipicos['co2_saved'], kde=True, ax=ax[1])
ax[1].set_title('Distribución co2_saved (Sin Outliers)')
st.pyplot(fig)

# Gráficos de cajas (Boxplot) después de eliminar outliers
c1, c2 = st.columns(2)
with c1:
    fig_box_energy_efficiency_sin = px.box(df_sin_atipicos, y='energy_efficiency', title="Boxplot energy_efficiency (Sin Outliers)")
    st.plotly_chart(fig_box_energy_efficiency_sin)
with c2:
    fig_box_co2_saved_sin = px.box(df_sin_atipicos, y='co2_saved', title="Boxplot co2_saved (Sin Outliers)")
    st.plotly_chart(fig_box_co2_saved_sin)

# Guardar el dataframe en un solo archivo CSV
df_sin_atipicos.to_csv('datos_sin_atipicos.csv', index=False)





# import streamlit as st
# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
# import numpy as np
# import plotly.express as px

# # Configurar el diseño de la página de Streamlit
# st.set_page_config(layout="wide")

# # Cargar los datos desde un archivo CSV
# # Cargar el dataset
# df = pd.read_csv('df/datos_imputacion_mice.csv', delimiter=',', encoding='latin1')


# # Mostrar los datos originales
# st.title('Outliers con Rango Intercuartil')
# st.subheader("Datos originales")
# st.dataframe(df)

# # Función para detectar valores atípicos usando el rango intercuartil (IQR)
# def eliminar_valores_atipicos(df, column):
#     # Calcular el cuartil 1 (Q1) y cuartil 3 (Q3)
#     Q1 = df[column].quantile(0.25)
#     Q3 = df[column].quantile(0.75)
#     IQR = Q3 - Q1
    
#     # Definir límites para detectar los outliers
#     lower_limit = Q1 - 1.5 * IQR
#     upper_limit = Q3 + 1.5 * IQR
    
#     # Filtrar los datos que están dentro de los límites
#     df_sin_atipicos = df[(df[column] >= lower_limit) & (df[column] <= upper_limit)]
    
#     return df_sin_atipicos

# # Gráficos de distribución (curvas de Gauss) y boxplots antes de eliminar outliers
# st.subheader("Gráficos antes de eliminar valores atípicos")

# # Seleccionar columnas para análisis
# columnas_analisis = ["value", "co2_saved", "energy_efficiency"]

# # Curvas de Gauss
# fig, ax = plt.subplots(1, 3, figsize=(15, 5))
# for i, col in enumerate(columnas_analisis):
#     sns.histplot(df[col], kde=True, ax=ax[i])
#     ax[i].set_title(f'Distribución {col} (Original)')
# st.pyplot(fig)

# # Gráficos de boxplot antes de eliminar outliers con Plotly Express
# c1, c2, c3 = st.columns(3)
# for i, col in enumerate(columnas_analisis):
#     fig_box = px.box(df, y=col, title=f"Boxplot {col} (Original)")
#     if i == 0:
#         c1.plotly_chart(fig_box)
#     elif i == 1:
#         c2.plotly_chart(fig_box)
#     else:
#         c3.plotly_chart(fig_box)

# # Eliminar valores atípicos en las columnas seleccionadas
# df_sin_atipicos = df.copy()
# for col in columnas_analisis:
#     df_sin_atipicos = eliminar_valores_atipicos(df_sin_atipicos, col)

# # Mostrar los datos después de eliminar valores atípicos
# st.subheader("Datos después de eliminar valores atípicos")
# st.dataframe(df_sin_atipicos)

# # Gráficos de distribución (curvas de Gauss) y boxplots después de eliminar outliers
# st.subheader("Gráficos después de eliminar valores atípicos")

# # Curvas de Gauss
# fig, ax = plt.subplots(1, 3, figsize=(15, 5))
# for i, col in enumerate(columnas_analisis):
#     sns.histplot(df_sin_atipicos[col], kde=True, ax=ax[i])
#     ax[i].set_title(f'Distribución {col} (Sin Outliers)')
# st.pyplot(fig)

# # Gráficos de boxplot después de eliminar outliers con Plotly Express
# c1, c2, c3 = st.columns(3)
# for i, col in enumerate(columnas_analisis):
#     fig_box_sin = px.box(df_sin_atipicos, y=col, title=f"Boxplot {col} (Sin Outliers)")
#     if i == 0:
#         c1.plotly_chart(fig_box_sin)
#     elif i == 1:
#         c2.plotly_chart(fig_box_sin)
#     else:
#         c3.plotly_chart(fig_box_sin)

# # Guardar los resultados en archivos CSV
# df_sin_atipicos.to_csv('datos_sin_atipicos.csv', index=False)


# import streamlit as st
# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
# import numpy as np
# import plotly.express as px



# df = pd.read_csv('df/datos_imputacion_mice.csv', delimiter=',', encoding='latin1')


# # Función para detectar valores atípicos usando el rango intercuartil (IQR)
# def eliminar_valores_atipicos(df, column):
#     # Calcular el cuartil 1 (Q1) y cuartil 3 (Q3)
#     Q1 = df[column].quantile(0.25)
#     Q3 = df[column].quantile(0.75)
#     IQR = Q3 - Q1
    
#     # Definir límites para detectar los outliers
#     lower_limit = Q1 - 1.5 * IQR
#     upper_limit = Q3 + 1.5 * IQR
    
#     # Filtrar los datos que están dentro de los límites
#     df_sin_atipicos = df[(df[column] >= lower_limit) & (df[column] <= upper_limit)]
    
#     return df_sin_atipicos


# # Mostrar los datos originales
# st.title('Outlieres con Rango Intercuartil')
# st.subheader("Datos originales")

# st.dataframe(df)

# # Gráficos de distribución (curvas de Gauss) y boxplots antes de eliminar outliers
# st.subheader("Gráficos antes de eliminar valores atípicos")

# # Curvas de Gauss
# fig, ax = plt.subplots(1, 2, figsize=(10, 5))
# sns.histplot(df['co2_saved'], kde=True, ax=ax[0])
# ax[0].set_title('Distribución co2_saved (Original)')
# sns.histplot(df['energy_efficiency'], kde=True, ax=ax[1])
# ax[1].set_title('Distribución Ventas Mensuales (Original)')
# st.pyplot(fig)



# # Gráfico de cajas (Boxplot) con Plotly Express
# fig_box_co2_saved = px.box(df, y='co2_saved', title="Boxplot co2_saved (Original)")
# fig_box_ventas = px.box(df, y='energy_efficiency', title="Boxplot Ventas Mensuales (Original)")

# c1,c2= st.columns(2)
# with c1:
#     st.plotly_chart(fig_box_co2_saved)
# with c2:
#     st.plotly_chart(fig_box_ventas)





# # Eliminar valores atípicos en la columna 'co2_saved'
# df_sin_atipicos_co2_saved = eliminar_valores_atipicos(df, 'co2_saved')

# # Eliminar valores atípicos en la columna 'energy_efficiency'
# df_sin_atipicos_ventas = eliminar_valores_atipicos(df, 'energy_efficiency')

# # Mostrar los datos después de eliminar valores atípicos
# st.subheader("Datos después de eliminar valores atípicos")
# c1,c2=st.columns(2)
# with c1:
#     st.dataframe(df_sin_atipicos_co2_saved)
# with c2:
#     st.dataframe(df_sin_atipicos_ventas)

# # Gráficos de distribución (curvas de Gauss) y boxplots después de eliminar outliers
# st.subheader("Gráficos después de eliminar valores atípicos")

# # Curvas de Gauss
# fig, ax = plt.subplots(1, 2, figsize=(10, 5))
# sns.histplot(df_sin_atipicos_co2_saved['co2_saved'], kde=True, ax=ax[0])
# ax[0].set_title('Distribución co2_saved (Sin Outliers)')
# sns.histplot(df_sin_atipicos_ventas['energy_efficiency'], kde=True, ax=ax[1])
# ax[1].set_title('Distribución Ventas Mensuales (Sin Outliers)')
# st.pyplot(fig)



# c1,c2= st.columns(2)
# with c1:
#     fig_box_co2_saved_sin = px.box(df_sin_atipicos_co2_saved, y='co2_saved', title="Boxplot co2_saved (Sin Outliers)")
#     st.plotly_chart(fig_box_co2_saved_sin)
# with c2:
#     fig_box_ventas_sin = px.box(df_sin_atipicos_ventas, y='energy_efficiency', title="Boxplot Ventas Mensuales (Sin Outliers)")
#     st.plotly_chart(fig_box_ventas_sin)





# # Combinar los DataFrames sin outliers
# # Primero, asegúrate de tener las mismas filas en ambos DataFrames para evitar problemas de alineación.
# # Por ejemplo, puedes usar un inner join basado en un índice común o simplemente concatenar columnas.

# # Asumiendo que el índice se mantiene consistente tras la eliminación de outliers
# df_sin_atipicos_combinado = df_sin_atipicos_co2_saved[['co2_saved']].join(
#     df_sin_atipicos_ventas[['energy_efficiency']], how='inner'
# )

# # Guardar el DataFrame combinado en un solo archivo CSV
# df_sin_atipicos_combinado.to_csv('datos_sin_atipicos_combinado.csv', index=False)






