import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")


def transformar_logaritmicamente(df, column):
    df['Log_' + column] = np.log(df[column].replace(0, np.nan))  # Evitar el log(0)
    return df

def calcular_z_score_log(df, column):
    mean = df['Log_' + column].mean()
    std = df['Log_' + column].std()
    df['z_score_log_' + column] = (df['Log_' + column] - mean) / std
    return df

def eliminar_outliers_z_score(df, column, threshold=3):
    return df[(df['z_score_log_' + column] >= -threshold) & (df['z_score_log_' + column] <= threshold)]

def main():
    df = pd.read_csv('df/datos_imputacion_mice.csv', delimiter=',', encoding='latin1')
    st.title('Deteccion de Outliers con Transformacion Logaritmica y  Z-Score')
    st.subheader('Datos Originales')
    st.dataframe(df)
    
    df= transformar_logaritmicamente(df,'co2_saved')
    st.subheader('Datos Originales Trasnformados')
    st.dataframe(df)

    
    df = calcular_z_score_log(df, 'co2_saved')
    st.subheader('Datos Originales Trasnformados  Logaritmica y Z-Score')
    st.dataframe(df)
    
    st.subheader("Distribución de Ventas Mensuales (Original y Logarítmica)")
    fig, ax = plt.subplots(1, 2, figsize=(10, 5))
    sns.histplot(df['co2_saved'], kde=True, ax=ax[0])
    ax[0].set_title('Distribución Ventas Mensuales (Original)')
    sns.histplot(df['Log_co2_saved'], kde=True, ax=ax[1])
    ax[1].set_title('Distribución Logarítmica de Ventas Mensuales')
    st.pyplot(fig)
    
    df_sin_outliers = eliminar_outliers_z_score(df, 'co2_saved')

    st.subheader("Datos después de eliminar outliers basados en Z-Score (Logaritmo)")
    st.dataframe(df_sin_outliers)
    
    st.subheader("Distribución de Ventas Mensuales después de eliminar outliers")
    fig, ax = plt.subplots(1, 2, figsize=(10, 5))
    sns.histplot(df_sin_outliers['co2_saved'], kde=True, ax=ax[0])
    ax[0].set_title('Distribución Ventas Mensuales (Sin Outliers)')
    sns.histplot(df_sin_outliers['Log_co2_saved'], kde=True, ax=ax[1])
    ax[1].set_title('Distribución Logarítmica Ventas Mensuales (Sin Outliers)')
    st.pyplot(fig)

    st.subheader("Boxplot antes y después de eliminar outliers")

    fig_box_antes = px.box(df, y='co2_saved', title="Boxplot Ventas Mensuales (Original)")
    fig_box_despues = px.box(df_sin_outliers, y='co2_saved', title="Boxplot Ventas Mensuales (Sin Outliers)")

    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(fig_box_antes)
    with c2:
        st.plotly_chart(fig_box_despues)
    
if __name__=="__main__":
    main()