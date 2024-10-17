import streamlit as st
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import plotly.express as px
import numpy as np

# Configurar la página
st.set_page_config(layout="wide")

# Título de la aplicación
st.title("Análisis de Componentes Principales (PCA) con Streamlit y Plotly")

# Cargar el dataset externo
st.header("1. Cargar dataset")
st.write("Usamos el dataset 'Iris'.")

# Dataset de ejemplo (Iris)
##st.cache_data
def load_data():
    url = "https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data"
    columns = ['Longitud de sépalo', 'Ancho de sépalo', 'Longitud de pétalo', 'Ancho de pétalo', 'Species']
    df = pd.read_csv(url, header=None, names=columns)
    return df

df = load_data()
st.write("### Dataset original:", df.head())

# Seleccionar las variables para PCA (variables numéricas)
st.header("2. Selección de variables para PCA")
selected_columns = st.multiselect("Selecciona las variables para el PCA", df.columns[:-1], default=df.columns[:-1])
st.write("Variables seleccionadas:", selected_columns)

# Estandarización de los datos
st.header("3. Estandarización de los datos")
st.write("El PCA requiere que las variables estén estandarizadas para que todas tengan la misma importancia.")

# Escalar las variables seleccionadas
scaler = StandardScaler()
scaled_data = scaler.fit_transform(df[selected_columns])

st.write("### Datos escalados (primeras 5 filas):")
st.dataframe(pd.DataFrame(scaled_data, columns=selected_columns).head())

# Calcular la matriz de covarianza
st.header("4. Matriz de Covarianza")
cov_matrix = np.cov(scaled_data, rowvar=False)
st.write("### Matriz de Covarianza:")
st.dataframe(pd.DataFrame(cov_matrix, columns=selected_columns, index=selected_columns))

# Aplicar PCA
st.header("5. Aplicación de PCA")
st.write("Selecciona el número de componentes principales que deseas obtener.")

n_components = st.slider("Número de componentes", min_value=1, max_value=len(selected_columns), value=2)

pca = PCA(n_components=n_components)
pca_result = pca.fit_transform(scaled_data)

# Obtener los vectores propios
st.header("6. Vectores propios (Eigenvectors)")
st.write("Cada fila representa un vector propio, y cada columna es una de las variables originales seleccionadas.")

eigenvectors = pca.components_
st.dataframe(pd.DataFrame(eigenvectors, columns=selected_columns, index=[f'PC{i+1}' for i in range(n_components)]))

st.write("Los vectores propios nos dicen hacia dónde apuntan los componentes principales en el espacio original de las variables.")

# Crear un DataFrame con los resultados del PCA
pca_df = pd.DataFrame(pca_result, columns=[f'PC{i+1}' for i in range(n_components)])
pca_df['Species'] = df['Species']

st.write(f"### Resultado del PCA con {n_components} componentes principales:")
st.dataframe(pca_df.head())

# Explicación de la varianza acumulada
st.write("### Varianza explicada por cada componente principal:")
explained_variance = pca.explained_variance_ratio_
st.bar_chart(explained_variance)

# Varianza total
total_variance = sum(explained_variance)
st.write(f"### Varianza total explicada: {total_variance:.2f}")

# Visualización de los Componentes Principales
st.header("7. Visualización de los Componentes Principales")

if n_components<3:
    st.write("Gráfico interactivo de los dos primeros componentes principales.")
    fig = px.scatter(
        pca_df, x='PC1', y='PC2', color='Species', 
        title="Gráfico de los dos primeros Componentes Principales",
        labels={'PC1': f'PC1 ({explained_variance[0]:.2f} varianza explicada)',
                'PC2': f'PC2 ({explained_variance[1]:.2f} varianza explicada)'}
    )
    st.plotly_chart(fig)


# Gráfico 3D si se seleccionan 3 componentes
if n_components >= 3:
    st.write("Gráfico interactivo 3D de los tres primeros componentes principales.")
    fig_3d = px.scatter_3d(
        pca_df, x='PC1', y='PC2', z='PC3', color='Species',
        title="Gráfico 3D de los tres primeros Componentes Principales",
        labels={'PC1': f'PC1 ({explained_variance[0]:.2f} varianza explicada)',
                'PC2': f'PC2 ({explained_variance[1]:.2f} varianza explicada)',
                'PC3': f'PC3 ({explained_variance[2]:.2f} varianza explicada)'}
    )
    st.plotly_chart(fig_3d)