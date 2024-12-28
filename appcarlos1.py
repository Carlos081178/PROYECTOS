import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generar_estadisticas(df):
    """Genera estadísticas descriptivas de un DataFrame."""
    return df.describe()

def exportar_excel(df):  
    """Exporta un DataFrame a un archivo Excel."""
    ruta_archivo = "estadisticas_descriptivas.xlsx"
    df.to_excel(ruta_archivo, index=False, sheet_name="Estadisticas")
    return ruta_archivo

def crear_pdf(df_estadisticas, graficos):
    """Crea un informe en PDF con las estadísticas descriptivas y gráficos."""
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    
    # Título
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 750, "Informe de Estadísticas Descriptivas")

    # Estadísticas Descriptivas
    c.setFont("Helvetica", 12)
    c.drawString(100, 730, "Estadísticas Descriptivas:")
    
    # Convertir el DataFrame a texto y agregarlo al PDF
    text = df_estadisticas.to_string()
    text_lines = text.split('\n')
    
    y_position = 710
    for line in text_lines:
        c.drawString(100, y_position, line)
        y_position -= 15

    # Texto adicional sobre las estadísticas descriptivas
    c.drawString(100, y_position - 10, "Este informe contiene las estadísticas descriptivas de los datos.")
    y_position -= 25
    c.drawString(100, y_position - 10, "Las estadísticas incluyen medidas como la media, mediana,")
    y_position -= 15
    c.drawString(100, y_position - 10, "desviación estándar, valores mínimo y máximo, entre otros.")
    
    # Agregar gráficos al PDF si existen
    for grafico in graficos:
        c.showPage()  # Nueva página para cada gráfico
        c.drawImage(grafico, 50, 50, width=500, height=400)  # Ajusta el tamaño según sea necesario
    
    c.save()
    
    buffer.seek(0)
    return buffer

# Título de la aplicación
st.title("Analizador de Archivos Excel o CSV")

# Carga de archivo
archivo_subido = st.file_uploader("Sube tu archivo Excel o CSV", type=["xlsx", "xls", "csv"])

if archivo_subido is not None:
    st.write("El archivo ha sido cargado")

    # Leer el archivo según su tipo
    if archivo_subido.name.endswith("csv"):
        df = pd.read_csv(archivo_subido)
    else:
        df = pd.read_excel(archivo_subido)

    st.write("### Dataframe Original")     
    st.dataframe(df)

    # Generar estadísticas descriptivas
    df_estadisticas = generar_estadisticas(df)
    st.write("### Estadísticas Descriptivas")
    st.dataframe(df_estadisticas)

    # Exportar a Excel
    ruta_archivo_excel = exportar_excel(df_estadisticas)
    
    with open(ruta_archivo_excel, "rb") as archivo:
        st.download_button(
            label="Descargar Estadísticas en Excel", 
            data=archivo, 
            file_name="Estadisticas_descriptivas.xlsx", 
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    # Inicializar la lista de gráficos
    graficos = []  

    # Selección de variables para graficar
    st.write("### Seleccionar Variables para Graficar")
    
    columnas = df.columns.tolist()
    
    x_variable = st.selectbox("Selecciona la variable para el eje X:", columnas)
    y_variable = st.selectbox("Selecciona la variable para el eje Y:", columnas)

    if st.button("Generar Gráfico"):
        fig = px.scatter(df, x=x_variable, y=y_variable, title=f'Gráfico de {y_variable} vs {x_variable}')
        st.plotly_chart(fig)

        # Guardar gráfico como imagen temporal
        grafico_path = f"grafico_{x_variable}_{y_variable}.png"
        fig.write_image(grafico_path)
        graficos.append(grafico_path)

        st.success(f"Gráfico generado: {grafico_path}")

    # Crear PDF después de generar el gráfico o incluso si no se genera uno.
    
    pdf_buffer = crear_pdf(df_estadisticas, graficos)

    # Opción para descargar el informe en PDF siempre que haya estadísticas generadas.
    st.download_button(
        label="Descargar Informe PDF",
        data=pdf_buffer,
        file_name="informe_estadisticas.pdf",
        mime="application/pdf"
    )
else:
    st.write("Por favor carga un archivo.")