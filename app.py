import streamlit as st
import pandas as pd
import plotly.express as px
from io import StringIO
from pathlib import Path

st.set_page_config(page_title="Vehicles Explorer", layout="wide")

st.title("🚗 Vehicles Explorer (pandas + plotly + streamlit)")
     
car_data = pd.read_csv('vehicles_us.csv') # leer los datos
hist_button = st.button('Construir histograma') # crear un botón
     
if hist_button: # al hacer clic en el botón
         # escribir un mensaje
         st.write('Creación de un histograma para el conjunto de datos de anuncios de venta de coches')
         
         # crear un histograma
         fig = px.histogram(car_data, x="odometer")
     
         # mostrar un gráfico Plotly interactivo
         st.plotly_chart(fig, use_container_width=True)