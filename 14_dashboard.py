import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Configuración de la página
st.set_page_config(page_title="Análisis Exploratorio de Vehículos Eléctricos", layout="wide")

# Cargar el DataFrame desde un archivo CSV
df = pd.read_csv('df/datos_normalizados_minmax_completo.csv', delimiter=',', encoding='latin1')

# Convertir la columna 'year' a tipo entero para eliminar decimales
df['year'] = df['year'].astype(int)

st.title("Análisis Exploratorio de Vehículos Eléctricos por Región")

# Barra lateral de filtros
st.sidebar.header("Filtros")

# Filtro de selección de países
select_country = st.sidebar.multiselect("Seleccione el/los países", df['region'].unique(), default=df["region"].unique())

# Filtro de selección de año
select_year = st.sidebar.slider("Seleccione el año", int(df['year'].min()), int(df['year'].max()), (int(df['year'].min()), int(df['year'].max())))

# Filtro de variable para gráficos
select_variable = st.sidebar.selectbox("Seleccionar una variable para las gráficas", df.columns[2:])

# Filtrado de los datos según los filtros seleccionados
df_filtered = df[(df["region"].isin(select_country)) & (df['year'].between(select_year[0], select_year[1]))]

# Mostrar información del dataset si se selecciona el checkbox
if st.sidebar.checkbox("Mostrar información del dataset"):
    st.markdown("### Estadísticas Descriptivas")
    st.write(df_filtered.describe())

    st.markdown("### Datos Filtrados")
    st.write(df_filtered)

# Crear gráficos de distribución
st.markdown("## Distribuciones de Variables Seleccionadas")

col1, col2 = st.columns(2)

with col1:
    fig_hist = px.histogram(df_filtered, x=select_variable, nbins=30, color="region",
                            title=f"Distribución de {select_variable} por Región",
                            labels={select_variable: f"{select_variable.capitalize()}"})
    st.plotly_chart(fig_hist, use_container_width=True)

with col2:
    fig_box = px.box(df_filtered, x="region", y=select_variable, color="region",
                     title=f"Boxplot de {select_variable} por Región",
                     labels={"region": "Región", select_variable: select_variable.capitalize()})
    st.plotly_chart(fig_box, use_container_width=True)

# Gráfico de barras para la variable seleccionada
st.markdown("## Indicadores por Región")
fig_bar = px.bar(df_filtered, x="region", y=select_variable, color="region", barmode="overlay",
                 title=f"Barras de Región vs {select_variable}")
st.plotly_chart(fig_bar, use_container_width=True)

# Sección de Nube de Palabras
st.markdown("## Nube de Palabras de 'parameter' según Región")

text = " ".join(df_filtered["parameter"].dropna())
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
st.image(wordcloud.to_array(), use_column_width=True)

# Gráficos dinámicos de ventas y CO2
st.markdown("## Relación entre Ventas y CO₂ Ahorrado")

fig_scatter = px.scatter(df_filtered, x="sales_volume", y="co2_saved", color="region", size="sales_volume",
                         hover_data=['parameter', 'year'],
                         title="Relación entre Ventas de EV y CO₂ Ahorrado",
                         labels={"sales_volume": "Volumen de Ventas", "co2_saved": "CO₂ Ahorrado (toneladas)"})
st.plotly_chart(fig_scatter, use_container_width=True)


# Gráficos de Líneas de Crecimiento por Año
st.markdown("## Evolución a lo largo del tiempo")

# Agrupar por año y calcular la suma de las columnas relevantes
df_yearly = df_filtered.groupby("year", as_index=False).agg({"sales_volume": "sum", "co2_saved": "sum"})

# Crear el gráfico de líneas con colores fluorescentes
fig_line = go.Figure()
fig_line.add_trace(go.Scatter(
    x=df_yearly['year'], y=df_yearly['sales_volume'], mode='lines+markers',
    name='Ventas de EV',
    line=dict(color='#00FF00', width=3),  # Verde fluorescente
    marker=dict(color='#00FF00', size=8)
))
fig_line.add_trace(go.Scatter(
    x=df_yearly['year'], y=df_yearly['co2_saved'], mode='lines+markers',
    name='CO₂ Ahorrado',
    line=dict(color='#FF00FF', width=3),  # Rosa fluorescente
    marker=dict(color='#FF00FF', size=8)
))

# Actualizar el diseño del gráfico
fig_line.update_layout(
    title="Evolución de Ventas de EV y CO₂ Ahorrado",
    xaxis_title="Año",
    yaxis_title="Cantidad",
    legend_title="Indicador",
    hovermode="x unified"
)

st.plotly_chart(fig_line, use_container_width=True)

# Gráfico de barras apiladas para mostrar el CO₂ ahorrado y ventas a lo largo del tiempo
st.subheader("Evolución de Ventas de Vehículos Eléctricos y CO₂ Ahorrado a lo largo del Tiempo")

fig_bar = px.bar(
    df_yearly,
    x="year",
    y=["sales_volume", "co2_saved"],
    title="Ventas de EV y CO₂ Ahorrado a lo largo del Tiempo",
    labels={"year": "Año", "value": "Cantidad", "variable": "Indicador"},
    barmode="group",
    color_discrete_map={
        "sales_volume": "#39FF14",  # Verde fluorescente
        "co2_saved": "#FF1493"  # Rosa fluorescente
    }
)

st.plotly_chart(fig_bar, use_container_width=True)


# Crear gráfico de Pareto para ventas por región
st.markdown("## Gráfico de Pareto de Ventas por Región")
df_pareto = df_filtered.groupby('region')['sales_volume'].sum().sort_values(ascending=False).reset_index()
df_pareto['cumulative_percentage'] = df_pareto['sales_volume'].cumsum() / df_pareto['sales_volume'].sum() * 100

fig_pareto = go.Figure()
fig_pareto.add_trace(go.Bar(x=df_pareto['region'], y=df_pareto['sales_volume'], name='Ventas de EV'))
fig_pareto.add_trace(go.Scatter(x=df_pareto['region'], y=df_pareto['cumulative_percentage'], name='Porcentaje Acumulado',
                                mode='lines+markers', yaxis='y2'))

fig_pareto.update_layout(
    title="Gráfico de Pareto de Ventas de Vehículos Eléctricos por Región",
    yaxis=dict(title="Ventas de EV"),
    yaxis2=dict(title="Porcentaje Acumulado", overlaying='y', side='right'),
    xaxis=dict(title="Región"),
    legend=dict(x=0.85, y=1)
)
st.plotly_chart(fig_pareto, use_container_width=True)



# Agrupar por año y calcular la suma de las columnas relevantes
df_yearly = df_filtered.groupby("year", as_index=False).agg({"sales_volume": "sum", "co2_saved": "sum"})

fig_bar = px.bar(
    df_yearly,
    x="year",
    y=["sales_volume", "co2_saved"],
    title="Ventas de EV y CO₂ Ahorrado a lo largo del Tiempo",
    labels={"year": "Año", "value": "Cantidad", "variable": "Indicador"},
    barmode="group"
)

st.plotly_chart(fig_bar, use_container_width=True)

st.markdown("""
            ### Interpretación:
- El gráfico de dispersión muestra la relación entre el volumen de ventas de vehículos eléctricos y la cantidad de CO₂ ahorrado. Si observamos una tendencia creciente, sugiere que un mayor volumen de ventas se asocia con una reducción significativa de emisiones.
- El gráfico de barras agrupadas muestra cómo han evolucionado las ventas de vehículos eléctricos y el CO₂ ahorrado a lo largo de los años, destacando el impacto ambiental de la adopción de esta tecnología.
""")

# import streamlit as st
# import pandas as pd
# import matplotlib.pyplot as plt
# import plotly.express as px
# from wordcloud import WordCloud
# import seaborn as sns

# st.set_page_config(layout="wide")

# # Cargar los datos desde el archivo CSV
# df = pd.read_csv('df/datos_sin_outliers.csv', delimiter=',', encoding='latin1')

# st.title("Análisis exploratorio de datos por región")

# st.sidebar.header("Filtros")

# # Filtros para 'region', 'year', y una columna seleccionable para gráficas
# select_region = st.sidebar.multiselect("Seleccione la/las regiones", df['region'].unique(), default=df["region"].unique())
# select_year = st.sidebar.selectbox("Seleccione el año", df["year"].unique())
# select_variable = st.sidebar.selectbox("Selección de una variable para las gráficas", df.columns[8:])

# # Filtrar el dataframe por región y año
# df = df[df["region"].isin(select_region) & (df['year'] == select_year)]

# # Mostrar información del dataset si se selecciona la opción
# if st.checkbox("Mostrar información del dataset"):
#     with st.expander("Estadísticas descriptivas del dataset"):
#         st.subheader("Estadísticas descriptivas del dataset")
#         st.write(df.describe())
#     with st.expander("Datos originales"):
#         st.subheader("Datos originales")
#         st.write(df)

# # Crear dos columnas para gráficos
# col1, col2 = st.columns(2)

# with col1:
#     st.subheader(f"Distribución del {select_variable}")
#     st.write(f"Este gráfico muestra la distribución del {select_variable} por regiones")
#     fig_distribution = px.histogram(df, x=select_variable, nbins=30, title=f"Distribución del {select_variable}")
#     st.plotly_chart(fig_distribution)

# with col2:
#     st.subheader(f"Distribución del {select_variable}")
#     st.write(f"Este gráfico representa la distribución del {select_variable}")
#     fig_boxplot = px.box(df, x="region", title=f"Distribución del {select_variable} por regiones", color="region")
#     st.plotly_chart(fig_boxplot)

# # Indicadores económicos en gráfico de barras
# with st.expander("Indicadores por regiones"):
#     st.subheader("Gráfico de barras - Indicadores")
#     fig_bar = px.bar(df, x="region", y=select_variable, color="region", barmode="overlay", title=f"Barras de región vs {select_variable}")
#     st.plotly_chart(fig_bar)

# # Gráfico de dispersión (scatter)
# st.subheader(f"{select_variable} vs Peso del Vehículo (weight_kg)")
# fig_scatter = px.scatter(df, x=select_variable, y='weight_kg', title=f"{select_variable} vs Peso del Vehículo", color="region")
# st.plotly_chart(fig_scatter)

# # Crecimiento de la variable a lo largo del tiempo
# st.subheader(f"Crecimiento {select_variable} a lo largo del tiempo")
# fig_line = px.line(df, x="year", y=select_variable, color="region", title=f"Crecimiento {select_variable} a lo largo del tiempo")
# st.plotly_chart(fig_line)

# # Gráfico de violín
# st.subheader(f"Cuota de {select_variable} por región")
# fig_violin = px.violin(df, x="region", y=select_variable, title=f"{select_variable} por región", color="region")
# st.plotly_chart(fig_violin)

# # Nube de palabras por región según la variable seleccionada
# st.subheader(f"Nube de palabras de regiones según {select_variable}")
# fig_cloud = dict(zip(df['region'], df[select_variable]))

# # Crear la nube de palabras
# wordcloud = WordCloud(width=800, height=400, background_color='white')
# wordcloud.generate_from_frequencies(fig_cloud)

# # Mostrar la nube de palabras usando matplotlib
# plt.figure(figsize=(10, 5))
# plt.imshow(wordcloud, interpolation='bilinear')
# plt.axis('off')
# st.pyplot(plt)

# # Gráfico de barras por región
# st.subheader(f"Gráfico de barras {select_variable} por región")
# df_barras = df.groupby('region')[select_variable].mean()
# with st.expander(f"Datos Agrupados por {select_variable}"):
#     st.write(df_barras)
# st.bar_chart(df_barras)
