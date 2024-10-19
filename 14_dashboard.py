import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
import matplotlib.pyplot as plt

st.set_page_config(page_title="Análisis Exploratorio de Vehículos Eléctricos", layout="wide")

df = pd.read_csv('df/datos_normalizados_minmax_completo.csv', delimiter=',', encoding='latin1')

df['year'] = df['year'].astype(int)

st.title("Análisis Exploratorio de Vehículos Eléctricos por Región")

st.sidebar.header("Filtros")

default_countries = sorted(df['region'].unique())[:5]

select_country = st.sidebar.multiselect(
    "Seleccione el/los países",
    options=sorted(df['region'].unique()),  
    default=default_countries  
)


select_year = st.sidebar.slider("Seleccione el año", int(df['year'].min()), int(df['year'].max()), (int(df['year'].min()), int(df['year'].max())))

select_variable = st.sidebar.selectbox("Seleccionar una variable para las gráficas", df.columns[2:])

df_filtered = df[(df["region"].isin(select_country)) & (df['year'].between(select_year[0], select_year[1]))]

if st.sidebar.checkbox("Mostrar información del dataset"):
    st.markdown("### Estadísticas Descriptivas")
    st.write(df_filtered.describe())

    st.markdown("### Datos Filtrados")
    st.write(df_filtered)

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

st.markdown("## Indicadores por Región")
fig_bar = px.bar(df_filtered, x="region", y=select_variable, color="region", barmode="overlay",
                 title=f"Barras de Región vs {select_variable}")
st.plotly_chart(fig_bar, use_container_width=True)

st.markdown("## Nube de Palabras de 'parameter' según Región")

text = " ".join(df_filtered["parameter"].dropna())
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
st.image(wordcloud.to_array(), use_column_width=True)

st.markdown("## Relación entre Ventas y CO₂ Ahorrado")

fig_scatter = px.scatter(df_filtered, x="sales_volume", y="co2_saved", color="region", size="sales_volume",
                         hover_data=['parameter', 'year'],
                         title="Relación entre Ventas de EV y CO₂ Ahorrado",
                         labels={"sales_volume": "Volumen de Ventas", "co2_saved": "CO₂ Ahorrado (toneladas)"})
st.plotly_chart(fig_scatter, use_container_width=True)


st.markdown("## Evolución a lo largo del tiempo")

df_yearly = df_filtered.groupby("year", as_index=False).agg({"sales_volume": "sum", "co2_saved": "sum"})

fig_line = go.Figure()
fig_line.add_trace(go.Scatter(
    x=df_yearly['year'], y=df_yearly['sales_volume'], mode='lines+markers',
    name='Ventas de EV',
    line=dict(color='#00FF00', width=3),  
    marker=dict(color='#00FF00', size=8)
))
fig_line.add_trace(go.Scatter(
    x=df_yearly['year'], y=df_yearly['co2_saved'], mode='lines+markers',
    name='CO₂ Ahorrado',
    line=dict(color='#FF00FF', width=3),  
    marker=dict(color='#FF00FF', size=8)
))

fig_line.update_layout(
    title="Evolución de Ventas de EV y CO₂ Ahorrado",
    xaxis_title="Año",
    yaxis_title="Cantidad",
    legend_title="Indicador",
    hovermode="x unified"
)

st.plotly_chart(fig_line, use_container_width=True)

st.subheader("Evolución de Ventas de Vehículos Eléctricos y CO₂ Ahorrado a lo largo del Tiempo")

fig_bar = px.bar(
    df_yearly,
    x="year",
    y=["sales_volume", "co2_saved"],
    title="Ventas de EV y CO₂ Ahorrado a lo largo del Tiempo",
    labels={"year": "Año", "value": "Cantidad", "variable": "Indicador"},
    barmode="group",
    color_discrete_map={
        "sales_volume": "#39FF14",  
        "co2_saved": "#FF1493" 
    }
)

st.plotly_chart(fig_bar, use_container_width=True)


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

st.markdown("## Clasificación por Unidades Tipo de Venta")
fig_unidades = px.bar(
    df_filtered, 
    x="parameter", 
    y="sales_volume", 
    color="region", 
    title="Clasificación por Unidades Tipo de Venta",
    labels={"parameter": "Tipo de Venta", "sales_volume": "Volumen de Ventas"},
    barmode="stack"  
)
st.plotly_chart(fig_unidades, use_container_width=True)


df_count = df_filtered.groupby(["region", "category"]).size().reset_index(name='count')

st.markdown("## Clasificación por Región y Conteo de Categorías")
fig_pais_bar_count = px.bar(
    df_count, 
    x="region", 
    y="count", 
    color="category", 
    title="Clasificación por Región y Conteo de Categorías",
    labels={"region": "País", "count": "Conteo", "category": "Categoría"},
    barmode="group"
)
st.plotly_chart(fig_pais_bar_count, use_container_width=True)



st.markdown("## Tendencias de Ventas por Año")
df_yearly_trend = df_filtered.groupby("year").agg({"sales_volume": "sum"}).reset_index()
fig_tendencias = px.line(df_yearly_trend, x="year", y="sales_volume", title="Tendencias de Ventas por Año",
                         labels={"year": "Año", "sales_volume": "Volumen de Ventas"})
st.plotly_chart(fig_tendencias, use_container_width=True)