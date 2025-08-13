# my_project
My test Project

# Explorador de Vehículos (Streamlit)

Aplicación web simple para explorar datos de vehículos y **cumplir los requisitos** del proyecto:
- Encabezado con texto.
- - **ENLACE AL DASHBOARD** (https://my-project-2-thlk.onrender.com/)
- **Histograma** configurable.
- **Gráfico de dispersión** configurable.
- Al menos **un botón** y **una casilla de verificación**.

## Requisitos
- Python 3.11+  
- `pip install -r requirements.txt`

## Cómo ejecutar localmente
```bash
python -m venv vehicles_env
# Windows:
.\vehicles_env\Scripts\activate
# macOS/Linux:
source vehicles_env/bin/activate

pip install -r requirements.txt
python -m streamlit run app.py
