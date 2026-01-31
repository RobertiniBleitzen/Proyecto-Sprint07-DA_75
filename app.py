import pandas as pd
import plotly.express as px
import streamlit as st
from pathlib import Path

st.set_page_config(page_title="Sprint 07 Dashboard", layout="wide")

st.title("Sprint 07 — Panel de control con Streamlit")
st.caption("Dataset: vehicles_us.csv | EDA + visualizaciones interactivas")

# -----------------------------
# Carga de datos (con cache)
# -----------------------------


@st.cache_data
def load_data():
    # app.py está en la raíz del proyecto, igual que vehicles_us.csv
    data_path = Path(__file__).parent / "vehicles_us.csv"
    df = pd.read_csv(data_path)

    # Aseguramos tipos útiles
    # (si hay columnas que vienen como texto con NaN, esto ayuda)
    if "model_year" in df.columns:
        df["model_year"] = pd.to_numeric(df["model_year"], errors="coerce")
    if "price" in df.columns:
        df["price"] = pd.to_numeric(df["price"], errors="coerce")
    if "odometer" in df.columns:
        df["odometer"] = pd.to_numeric(df["odometer"], errors="coerce")

    return df


df = load_data()

# -----------------------------
# Sidebar: filtros
# -----------------------------
st.sidebar.header("Filtros")

# Filtro por tipo
type_options = sorted(df["type"].dropna().unique().tolist()
                      ) if "type" in df.columns else []
selected_types = st.sidebar.multiselect(
    "Tipo de vehículo (type)", type_options, default=type_options)

# Filtro por condición
condition_options = sorted(df["condition"].dropna(
).unique().tolist()) if "condition" in df.columns else []
selected_conditions = st.sidebar.multiselect(
    "Condición (condition)", condition_options, default=condition_options)

# Filtro por año (model_year)
if "model_year" in df.columns and df["model_year"].notna().any():
    min_year = int(df["model_year"].min())
    max_year = int(df["model_year"].max())
    year_range = st.sidebar.slider(
        "Rango de año (model_year)", min_year, max_year, (min_year, max_year))
else:
    year_range = None

# Filtro por precio
if "price" in df.columns and df["price"].notna().any():
    min_price = int(df["price"].min())
    max_price = int(df["price"].max())
    price_range = st.sidebar.slider(
        "Rango de precio (price)", min_price, max_price, (min_price, max_price))
else:
    price_range = None

# Checkbox: quitar outliers rápidos (opcional)
remove_outliers = st.sidebar.checkbox("Quitar outliers (rápido)", value=True)

# -----------------------------
# Aplicar filtros
# -----------------------------
filtered = df.copy()

if selected_types and "type" in filtered.columns:
    filtered = filtered[filtered["type"].isin(selected_types)]

if selected_conditions and "condition" in filtered.columns:
    filtered = filtered[filtered["condition"].isin(selected_conditions)]

if year_range and "model_year" in filtered.columns:
    filtered = filtered[(filtered["model_year"] >= year_range[0]) & (
        filtered["model_year"] <= year_range[1])]

if price_range and "price" in filtered.columns:
    filtered = filtered[(filtered["price"] >= price_range[0])
                        & (filtered["price"] <= price_range[1])]

# Outliers simples (puedes ajustar después)
if remove_outliers:
    if "price" in filtered.columns:
        filtered = filtered[filtered["price"].between(100, 200000)]
    if "odometer" in filtered.columns:
        filtered = filtered[filtered["odometer"].between(0, 500000)]

# -----------------------------
# KPIs
# -----------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("Registros (total)", f"{len(df):,}")
col2.metric("Registros (filtrados)", f"{len(filtered):,}")

if "price" in filtered.columns and filtered["price"].notna().any():
    col3.metric("Precio mediano", f"${filtered['price'].median():,.0f}")
else:
    col3.metric("Precio mediano", "N/A")

if "odometer" in filtered.columns and filtered["odometer"].notna().any():
    col4.metric("Odómetro mediano", f"{filtered['odometer'].median():,.0f}")
else:
    col4.metric("Odómetro mediano", "N/A")

st.divider()

# -----------------------------
# Tabs: Data / Gráficas
# -----------------------------
tab1, tab2 = st.tabs(["📄 Datos", "📊 Visualizaciones"])

with tab1:
    st.subheader("Vista previa del dataset filtrado")
    st.dataframe(filtered.head(50), use_container_width=True)

    with st.expander("Resumen rápido (info faltantes)"):
        if len(filtered) == 0:
            st.warning("No hay datos con los filtros actuales.")
        else:
            na_counts = filtered.isna().sum().sort_values(ascending=False)
            st.write("Valores faltantes por columna:")
            st.dataframe(na_counts, use_container_width=True)

with tab2:
    if len(filtered) == 0:
        st.warning(
            "No hay datos con los filtros actuales. Ajusta filtros en la barra lateral.")
    else:
        left, right = st.columns(2)

        with left:
            st.subheader("Histograma: Odómetro")
            if "odometer" in filtered.columns:
                fig_odo = px.histogram(
                    filtered, x="odometer", title="Distribución del odómetro")
                st.plotly_chart(fig_odo, use_container_width=True)
            else:
                st.info("No existe la columna 'odometer'.")

        with right:
            st.subheader("Histograma: Precio")
            if "price" in filtered.columns:
                fig_price = px.histogram(
                    filtered, x="price", title="Distribución de precios")
                st.plotly_chart(fig_price, use_container_width=True)
            else:
                st.info("No existe la columna 'price'.")

        st.subheader("Relación: Precio vs Odómetro")
        if "price" in filtered.columns and "odometer" in filtered.columns:
            fig_scatter = px.scatter(
                filtered,
                x="odometer",
                y="price",
                opacity=0.25,
                title="Precio vs Odómetro"
            )
            st.plotly_chart(fig_scatter, use_container_width=True)
        else:
            st.info("Se requieren columnas 'price' y 'odometer' para el scatter.")

        st.subheader("Precio por Tipo (Boxplot)")
        if "type" in filtered.columns and "price" in filtered.columns:
            fig_box = px.box(filtered, x="type", y="price",
                             title="Precio por tipo de vehículo")
            st.plotly_chart(fig_box, use_container_width=True)
        else:
            st.info("Se requieren columnas 'type' y 'price' para el boxplot.")
