import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from wordcloud import WordCloud
import seaborn as sns

st.set_page_config(layout="wide")
df = pd.read_csv('df/country_comparison_large_dataset_m.csv')

st.title("Análisis exploratorio de datos de país")

st.sidebar.header("Filtros")

select_country = st.sidebar.multiselect("Seleccione el/los países", df['Country'].unique(), default=df["Country"].unique())
select_year = st.sidebar.selectbox("Seleccione el año", df["Year"].unique())
select_variable = st.sidebar.selectbox("Selección de una variable para las gráficas", df.columns[2:])

df = df[df["Country"].isin(select_country) & (df['Year'] == select_year)]
if st.checkbox("Mostrar información del dataset"):
    with st.expander("Estadísticas descriptivas del dataset"):
        st.subheader("Estadísticas descriptivas del dataset")
        st.write(df.describe())
    with st.expander("Datos originales"):
        st.subheader("Datos originales")
        st.write(df)

col1, col2 = st.columns(2)

with col1:
    st.subheader(f"Distribución del {select_variable}")
    st.write(f"Este gráfico muestra la distribución del {select_variable} por países")
    fig_gdp = px.histogram(df, x=select_variable, nbins=30, title=f"Distribución del {select_variable}")
    st.plotly_chart(fig_gdp)

with col2:
    st.subheader(f"Distribución del {select_variable}")
    st.write(f"Este gráfico representa la distribución del {select_variable}")
    fig_gdp_capita = px.box(df, x="Country", title=f"Distribución del {select_variable}", color="Country")
    st.plotly_chart(fig_gdp_capita)

with st.expander("Indicadores económicos"):
    st.subheader("Gráfico de barras - Indicadores")
    fig_gdp2 = px.bar(df, x="Country", y=select_variable, color="Country", barmode="overlay", title=f"Barras de país vs {select_variable}")
    st.plotly_chart(fig_gdp2)

st.subheader(f"{select_variable} vs Esperanza de vida")
fig_scatter = px.scatter(df, x=select_variable, y='Life Expectancy (Years)', title=f"{select_variable} vs Esperanza de vida", color="Country")
st.plotly_chart(fig_scatter)


st.subheader(f"Crecimiento {select_variable} a lo largo del tiempo")
fig_line = px.line(df, x="Year", y=select_variable, color="Country", title=f"Crecimiento {select_variable} a lo largo del tiempo")
st.plotly_chart(fig_line)

st.subheader(f"Cuota de {select_variable} por país")
fig_violin = px.violin(df, x="Country", y=select_variable, title=f"{select_variable} por país", color="Country")
st.plotly_chart(fig_violin)

st.subheader(f"Nube de palabras de países según {select_variable}")
fig_cloud = dict(zip(df['Country'], df[select_variable]))

# Crear la nube de palabras
wordcloud = WordCloud(width=800, height=400, background_color='white')
wordcloud.generate_from_frequencies(fig_cloud)

# Mostrar la nube de palabras usando matplotlib
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
st.pyplot(plt)

st.subheader(f"grafico de barras {select_variable} por pais")
df_barras= df.groupby('Country')[select_variable].mean()
with st.expander (f"Datos Agrupados por {select_variable}"):
    st.write(df_barras)
st.bar_chart(df_barras)