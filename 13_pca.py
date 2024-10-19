import streamlit as st
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import plotly.express as px
import numpy as np

st.set_page_config(layout="wide")

st.title("Análisis de Componentes Principales (PCA) con Streamlit y Plotly")

df = pd.read_csv('df/datos_normalizados_minmax_completo.csv', delimiter=',', encoding='latin1')

# Visualizar el dataset original
st.write("### Dataset original:", df.head())

numeric_columns = ['year', 'value', 'price', 'range_km', 'charging_time', 'sales_volume', 'co2_saved',
                   'battery_capacity', 'energy_efficiency', 'weight_kg', 'number_of_seats', 
                   'motor_power', 'distance_traveled']

numeric_columns = [col for col in numeric_columns if col in df.columns]

st.header("2. Selección de variables para PCA")
selected_columns = st.multiselect("Selecciona las variables para el PCA", numeric_columns, default=numeric_columns)
st.write("Variables seleccionadas:", selected_columns)

st.header("3. Estandarización de los datos")
st.write("El PCA requiere que las variables estén estandarizadas para que todas tengan la misma importancia.")

scaler = StandardScaler()
scaled_data = scaler.fit_transform(df[selected_columns])

st.write("### Datos escalados (primeras 5 filas):")
st.dataframe(pd.DataFrame(scaled_data, columns=selected_columns).head())

st.header("4. Matriz de Covarianza")
cov_matrix = np.cov(scaled_data, rowvar=False)
st.write("### Matriz de Covarianza:")
st.dataframe(pd.DataFrame(cov_matrix, columns=selected_columns, index=selected_columns))

st.header("5. Aplicación de PCA")
st.write("Selecciona el número de componentes principales que deseas obtener.")

n_components = st.slider("Número de componentes", min_value=1, max_value=len(selected_columns), value=2)

pca = PCA(n_components=n_components)
pca_result = pca.fit_transform(scaled_data)

st.header("6. Vectores propios (Eigenvectors)")
st.write("Cada fila representa un vector propio, y cada columna es una de las variables originales seleccionadas.")

eigenvectors = pca.components_
st.dataframe(pd.DataFrame(eigenvectors, columns=selected_columns, index=[f'PC{i+1}' for i in range(n_components)]))

st.write("Los vectores propios nos dicen hacia dónde apuntan los componentes principales en el espacio original de las variables.")

pca_df = pd.DataFrame(pca_result, columns=[f'PC{i+1}' for i in range(n_components)])

st.write(f"### Resultado del PCA con {n_components} componentes principales:")
st.dataframe(pca_df.head())

st.write("### Varianza explicada por cada componente principal:")
explained_variance = pca.explained_variance_ratio_
st.bar_chart(explained_variance)

total_variance = sum(explained_variance)
st.write(f"### Varianza total explicada: {total_variance:.2f}")

st.header("7. Visualización de los Componentes Principales")

if 'region' not in df.columns:
    st.error("La columna 'region' no está presente en el dataset. Asegúrate de que exista una columna de 'region'.")
else:
    pca_df = pd.DataFrame(pca_result, columns=[f'PC{i+1}' for i in range(n_components)])
    pca_df['region'] = df['region']

    st.write(f"### Resultado del PCA con {n_components} componentes principales:")
    st.dataframe(pca_df.head())

    st.header("7. Visualización de los Componentes Principales por Región")

    if n_components >= 2:
        st.write("Gráfico interactivo de los dos primeros componentes principales diferenciados por región.")
        fig = px.scatter(
            pca_df, x='PC1', y='PC2', 
            title="Gráfico de los dos primeros Componentes Principales diferenciados por región",
            labels={'PC1': f'PC1 ({explained_variance[0]*100:.2f}% varianza explicada)',
                    'PC2': f'PC2 ({explained_variance[1]*100:.2f}% varianza explicada)'},
            color='region',  
            hover_data=['region']  
        )
        st.plotly_chart(fig)

    if n_components >= 3:
        st.write("Gráfico interactivo 3D de los tres primeros componentes principales diferenciados por región.")
        fig_3d = px.scatter_3d(
            pca_df, x='PC1', y='PC2', z='PC3',
            title="Gráfico 3D de los tres primeros Componentes Principales diferenciados por región",
            labels={'PC1': f'PC1 ({explained_variance[0]*100:.2f}% varianza explicada)',
                    'PC2': f'PC2 ({explained_variance[1]*100:.2f}% varianza explicada)',
                    'PC3': f'PC3 ({explained_variance[2]*100:.2f}% varianza explicada)'},
            color='region',  
            hover_data=['region']  
        )
        st.plotly_chart(fig_3d)