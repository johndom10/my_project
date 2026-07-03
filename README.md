# Used Vehicles Market Analysis

Exploratory analysis and interactive dashboard of a US used-vehicles marketplace. Built to identify price drivers, segment turnover, and inventory dynamics that inform pricing and listing strategy.

**🔗 Live dashboard:** [pega-aquí-tu-URL-de-Render]

---

## Business questions
- Which vehicle attributes most influence listing price?
- How do condition and odometer affect days on market?
- Which vehicle types and segments turn over fastest?

## Dataset
US used-vehicles marketplace listings. Fields include price, model year, condition, odometer, fuel type, transmission, type, paint color and days listed.

## Stack
Python · pandas · NumPy · Plotly Express · Streamlit · Render (deployment)

## Key findings
- [Hallazgo 1 — ej: "El precio cae ~X% por cada 20k millas de odómetro hasta el umbral Y, luego se estabiliza"]
- [Hallazgo 2 — ej: "SUVs y trucks retienen mejor valor a través de los años modelo"]
- [Hallazgo 3 — ej: "Listados en condición 'excellent' se venden en ~X días vs ~Y en condición 'fair'"]

## Repo structure
```
├── notebooks/eda.ipynb    # Exploratory data analysis
├── app.py                 # Streamlit dashboard
├── vehicles_us.csv        # Source dataset
└── requirements.txt
```

## Run locally
```bash
git clone https://github.com/johndom10/used-vehicles-market-analysis
cd used-vehicles-market-analysis
pip install -r requirements.txt
streamlit run app.py
```

## Author
**Jonathan Dominguez** — Data & BI Analyst
[LinkedIn](https://www.linkedin.com/in/johndom10) · [Tableau Public](https://public.tableau.com/app/profile/jonathan.dominguez)
