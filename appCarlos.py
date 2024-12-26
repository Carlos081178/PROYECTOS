import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

def generar_estadisticas(df):
    """
    GENERA ESTADISTICAS DESCRIPTIVAS DE UN DATA FRAME
    """
    return df.describe()
 
def exportar_excel(df):  
    """
    Exporta un data frame a un archivo excel
    """
    with open("estadisticas_descriptivas.xlsx", "wb") as archivo:
        df.to_excel(archivo, index=False, sheet_name="Estadisticas")
    return "estadisticas_descriptivas.xlsx"

st.title("Analizador de archivos Excel o CSV")

archivo_subido = st.file_uploader("Sube tu archivo excel o csv", type=["xlsx", "xls", "csv"])

if archivo_subido is not None:
    st.write("El archivo ha sido cargado")

    if archivo_subido.name.endswith("csv"):
        df = pd.read_csv(archivo_subido)
    else:
        df = pd.read_excel(archivo_subido)

    st.write("### Dataframe original")     
    st.dataframe(df)

    # Generar estadísticas descriptivas
    df_estadisticas = generar_estadisticas(df)
    st.write("### Estadísticas Descriptivas")
    st.dataframe(df_estadisticas)

    # Exportar a Excel
    ruta_archivo = exportar_excel(df_estadisticas)
    
    with open(ruta_archivo, "rb") as archivo:
        st.download_button(
            label="Descargar estadísticas en Excel", 
            data=archivo, 
            file_name="Estadisticas_descriptivas.xlsx", 
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    # Selección de variables para graficar
    st.write("### Seleccionar Variables para Graficar")
    
    columnas = df.columns.tolist()
    
    x_variable = st.selectbox("Selecciona la variable para el eje X:", columnas)
    y_variable = st.selectbox("Selecciona la variable para el eje Y:", columnas)

    if st.button("Generar Gráfico"):
        fig = px.scatter(df, x=x_variable, y=y_variable, title=f'Gráfico de {y_variable} vs {x_variable}')
        st.plotly_chart(fig)

else:
    st.write("Por favor cargar el archivo")