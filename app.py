import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Botones: Histograma y Dispersión")

@st.cache_data
def load_data():
    for name in ("vehicles_us.csv", "vehicles_us_sample.csv"):
        try:
            return pd.read_csv(name)
        except Exception:
            pass
    return pd.DataFrame({
        "price":[12000, 8000,15000,5000,22000,17000,9000,13000,27000,7000],
        "odometer":[60000,120000,45000,180000,30000,80000,110000,65000,25000,140000]
    })

df = load_data()
num_cols = df.select_dtypes(include="number").columns.tolist()
if len(num_cols) < 2:
    st.error("Se requieren al menos 2 columnas numéricas.")
    st.stop()

use_logy = st.checkbox("Escala logarítmica en Y (para dispersión)", value=True)

hist_col = st.selectbox(
    "Columna para histograma",
    num_cols,
    index=(num_cols.index("odometer") if "odometer" in num_cols else 0)
)
x_col = st.selectbox(
    "X (dispersión)",
    num_cols,
    index=(num_cols.index("odometer") if "odometer" in num_cols else 0)
)
y_col = st.selectbox(
    "Y (dispersión)",
    num_cols,
    index=(num_cols.index("price") if "price" in num_cols else 1)
)

if "last_plot" not in st.session_state:
    st.session_state.last_plot = None

c1, c2 = st.columns(2)
with c1:
    if st.button("Mostrar histograma"):
        st.session_state.last_plot = "hist"

with c2:
    if st.button("Mostrar dispersión"):
        st.session_state.last_plot = "scatter"

# Render según el botón
if st.session_state.last_plot == "hist":
    fig = px.histogram(df, x=hist_col, nbins=40, title=f"Histograma de {hist_col}")
    st.plotly_chart(fig, use_container_width=True)

elif st.session_state.last_plot == "scatter":
    fig = px.scatter(df, x=x_col, y=y_col, opacity=0.7, title=f"{y_col} vs {x_col}")
    if use_logy:
        fig.update_yaxes(type="log")
    st.plotly_chart(fig, use_container_width=True)

else:
    st.info("Haz clic en un botón para ver la gráfica.")

