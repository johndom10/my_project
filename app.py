import os, shutil, zipfile, textwrap, json
from pathlib import Path
import pandas as pd

base_dir = Path("/mnt/data/vehicles_streamlit_app")
if base_dir.exists():
    shutil.rmtree(base_dir)
base_dir.mkdir(parents=True, exist_ok=True)

app_py = textwrap.dedent("""
    import streamlit as st
    import pandas as pd
    import plotly.express as px
    from pathlib import Path

    st.set_page_config(page_title="Explorador de Vehículos", layout="wide")

    st.title("Explorador de Vehículos 🚗")
    st.markdown(
        "Esta aplicación de **Streamlit** cumple con los requisitos mínimos del proyecto:"
        "\\n- Un encabezado con texto (este)."
        "\\n- Un **histograma** configurable."
        "\\n- Un **gráfico de dispersión** configurable."
        "\\n- Al menos un **botón** y una **casilla de verificación** en la interfaz."
    )

    @st.cache_data(show_spinner=False)
    def load_local_csv():
        \"\"\"Busca un CSV local llamado 'vehicles_us.csv' o 'vehicles_us_sample.csv'\"\"\"
        root = Path(__file__).parent
        for name in ("vehicles_us.csv", "vehicles_us_sample.csv"):
            p = root / name
            if p.exists():
                df = pd.read_csv(p)
                return df, name
        return None, None

    # Sidebar: fuente de datos
    st.sidebar.header("Fuentes de datos")
    source = st.sidebar.radio("¿Qué datos usar?", ["Incluido en el proyecto", "Subir mi propio CSV"])

    df = None
    data_name = None

    if source == "Subir mi propio CSV":
        up = st.sidebar.file_uploader("Arrastra aquí tu CSV", type=["csv"])
        if up is not None:
            df = pd.read_csv(up)
            data_name = up.name
        else:
            st.info("Sube un archivo CSV para continuar o elige 'Incluido en el proyecto'.")
            st.stop()
    else:
        df, data_name = load_local_csv()
        if df is None:
            st.error("No se encontró 'vehicles_us.csv' ni 'vehicles_us_sample.csv' en el proyecto.")
            st.stop()

    st.success(f"Datos cargados: **{data_name}**  |  Filas: {len(df):,}  |  Columnas: {len(df.columns):,}")

    # Limpieza rápida: quitar filas completamente vacías y duplicados
    df = df.dropna(how="all").drop_duplicates()

    # Selección de columnas
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    categorical_cols = df.select_dtypes(exclude="number").columns.tolist()

    if len(numeric_cols) < 2:
        st.warning("Se necesitan al menos 2 columnas numéricas para el dispersión. Carga otro CSV si es necesario.")
    
    # Filtros opcionales
    with st.sidebar.expander("Filtros opcionales", expanded=False):
        year_col = "model_year" if "model_year" in df.columns else None
        if year_col:
            min_y, max_y = int(df[year_col].min()), int(df[year_col].max())
            y_from, y_to = st.slider("Rango de año del modelo", min_value=min_y, max_value=max_y, value=(min_y, max_y))
            df = df[(df[year_col] >= y_from) & (df[year_col] <= y_to)]

        use_sample = st.checkbox("Usar una muestra de hasta 5,000 filas (más rápido)", value=True)
        if use_sample and len(df) > 5000:
            df_scatter = df.sample(5000, random_state=42)
        else:
            df_scatter = df

        show_data = st.checkbox("Mostrar tabla de datos")

    # --------------------
    # HISTOGRAMA
    # --------------------
    st.subheader("Histograma")
    default_hist_col = "odometer" if "odometer" in numeric_cols else (numeric_cols[0] if numeric_cols else None)
    if default_hist_col is None:
        st.error("No hay columnas numéricas para el histograma.")
        st.stop()

    col_hist = st.selectbox("Columna numérica para el histograma", numeric_cols, index=numeric_cols.index(default_hist_col))
    bins = st.slider("Número de bins", min_value=5, max_value=100, value=40, step=5)
    fig_hist = px.histogram(df, x=col_hist, nbins=bins, title=f"Histograma de {col_hist}")
    st.plotly_chart(fig_hist, use_container_width=True)

    # --------------------
    # DISPERSIÓN
    # --------------------
    st.subheader("Gráfico de dispersión")
    default_x = "odometer" if "odometer" in numeric_cols else numeric_cols[0]
    default_y = "price" if "price" in numeric_cols else (numeric_cols[1] if len(numeric_cols) > 1 else numeric_cols[0])

    c1, c2, c3 = st.columns(3)
    with c1:
        x_col = st.selectbox("Eje X", numeric_cols, index=numeric_cols.index(default_x))
    with c2:
        y_col = st.selectbox("Eje Y", numeric_cols, index=numeric_cols.index(default_y) if default_y in numeric_cols else 0)
    with c3:
        color_col = st.selectbox("Color (opcional)", [None] + categorical_cols, index=0)

    log_y = st.checkbox("Escala logarítmica en Y", value=True if y_col.lower() == "price" else False)

    fig_scatter = px.scatter(
        df_scatter,
        x=x_col,
        y=y_col,
        color=None if color_col in (None, "None") else color_col,
        opacity=0.7,
        hover_data=[col for col in df.columns if col not in (x_col, y_col)][:5],
        title=f"{y_col} vs {x_col}"
    )

    if log_y:
        fig_scatter.update_yaxes(type="log")

    st.plotly_chart(fig_scatter, use_container_width=True)

    # --------------------
    # BOTONES (interacción)
    # --------------------
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("Restablecer selección (recargar)"):
            st.cache_data.clear()
            st.rerun()

    with col_b:
        csv_bytes = df.to_csv(index=False).encode("utf-8")
        st.download_button("Descargar datos actuales (CSV)", data=csv_bytes, file_name="vehicles_filtrados.csv", mime="text/csv")

    if show_data:
        st.dataframe(df.head(100))
""")

(base_dir / "app.py").write_text(app_py, encoding="utf-8")

# Write requirements.txt
requirements = textwrap.dedent("""
    streamlit>=1.31
    pandas>=2.1
    plotly>=5.20
    numpy>=1.25
""")
(base_dir / "requirements.txt").write_text(requirements, encoding="utf-8")

# Write README.md
readme = textwrap.dedent("""
    # Explorador de Vehículos (Streamlit)

    App web mínima que cumple con:
    - Encabezado con texto.
    - Un histograma.
    - Un gráfico de dispersión.
    - Al menos un botón y una casilla de verificación.

    ## Estructura
    ```text
    vehicles_streamlit_app/
    ├─ app.py
    ├─ requirements.txt
    ├─ vehicles_us_sample.csv   # (incluido para pruebas rápidas)
    └─ README.md
    ```

    > Si tienes `vehicles_us.csv`, colócalo junto a `app.py`. La app lo usará automáticamente.

    ## Ejecutar localmente

    **Windows (PowerShell):**
    ```powershell
    cd vehicles_streamlit_app
    python -m venv vehicles_env
    .\\vehicles_env\\Scripts\\activate
    pip install --upgrade pip
    pip install -r requirements.txt
    streamlit run app.py
    ```

    **macOS / Linux:**
    ```bash
    cd vehicles_streamlit_app
    python3 -m venv vehicles_env
    source vehicles_env/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    streamlit run app.py
    ```

    Luego abre el navegador en la URL que te muestre la terminal (por ejemplo `http://localhost:8501`).

    ## Subir a GitHub

    1. Crea un repo nuevo (público o privado).
    2. Sube **todos** los archivos del folder.
    3. Verifica que `requirements.txt` y `app.py` estén en la raíz del repo.

    ## Deploy en Render.com

    - **Build Command**: `pip install -r requirements.txt`
    - **Start Command**: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
    - **Runtime**: Python 3.11 o 3.12
    - Tipo de servicio: *Web Service*

    ### Problemas comunes
    - **"streamlit: command not found"** o **"No module named streamlit"**: faltó instalar dependencias o `requirements.txt` no está en la raíz.
    - **"Could not open requirements file"**: el archivo no existe o el nombre/ruta no coincide (debe ser exactamente `requirements.txt` en la raíz).
    - Para **eliminar archivos en GitHub** desde la web: abre el archivo ▶️ icono de tacho ▶️ "Commit changes". O con Git: `git rm archivo && git commit -m "remove" && git push`.

    ---
    © Demo educativa.
""")
(base_dir / "README.md").write_text(readme, encoding="utf-8")

# If the user-provided CSV exists, include a small sample to keep the project light
src_csv = Path("/mnt/data/vehicles_us.csv")
sample_written = False
if src_csv.exists():
    try:
        df_full = pd.read_csv(src_csv)
        # Write a sampled subset to keep the repo light
        n = 5000 if len(df_full) > 5000 else len(df_full)
        df_sample = df_full.sample(n=n, random_state=42) if len(df_full) > 0 else df_full
        df_sample.to_csv(base_dir / "vehicles_us_sample.csv", index=False)
        sample_written = True
    except Exception as e:
        # Fallback: create an empty sample with typical columns
        cols = ["price","odometer","model_year","condition","fuel","model"]
        pd.DataFrame(columns=cols).to_csv(base_dir / "vehicles_us_sample.csv", index=False)
        sample_written = True
else:
    # Create a small synthetic sample to avoid empty app
    data = {
        "price": [12000, 8000, 15000, 5000, 22000, 17000, 9000, 13000, 27000, 7000],
        "odometer": [60000, 120000, 45000, 180000, 30000, 80000, 110000, 65000, 25000, 140000],
        "model_year": [2012, 2009, 2015, 2005, 2018, 2014, 2010, 2013, 2019, 2007],
        "condition": ["good","fair","like new","salvage","excellent","good","good","fair","excellent","fair"],
        "fuel": ["gas","gas","gas","diesel","gas","gas","hybrid","gas","electric","gas"],
        "model": ["sedan","pickup","sedan","suv","suv","sedan","hatchback","pickup","sedan","suv"]
    }
    pd.DataFrame(data).to_csv(base_dir / "vehicles_us_sample.csv", index=False)
    sample_written = True

# Zip the project
zip_path = Path("/mnt/data/vehicles_streamlit_app.zip")
if zip_path.exists():
    zip_path.unlink()

with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
    for p in base_dir.rglob("*"):
        z.write(p, p.relative_to(base_dir.parent))

zip_path, list(base_dir.iterdir())