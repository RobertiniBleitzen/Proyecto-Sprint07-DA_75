# Proyecto-Sprint07-DA_75  
### Interactive Data Dashboard with Streamlit

Este proyecto corresponde al **Sprint 07 – Herramientas de desarrollo de software** y tiene como objetivo construir, documentar y desplegar un **dashboard interactivo** utilizando **Streamlit**, aplicando buenas prácticas reales de desarrollo y despliegue en la nube.

La aplicación permite explorar un dataset de anuncios de venta de vehículos mediante filtros dinámicos y visualizaciones interactivas, ofreciendo métricas clave que apoyan el análisis exploratorio de datos (EDA).

---

## 🚀 Aplicación en producción (Render)

La aplicación está desplegada y accesible públicamente en el siguiente enlace:

🔗 **https://proyecto-sprint07-da-75.onrender.com**

> Nota: al estar desplegada en una instancia gratuita, la aplicación puede tardar algunos segundos en activarse si ha estado inactiva.

---

## 📊 Funcionalidades principales

- Filtros interactivos por:
  - Tipo de vehículo
  - Condición
  - Año del modelo
  - Rango de precios
- Eliminación opcional de outliers
- KPIs clave:
  - Total de registros
  - Registros filtrados
  - Precio mediano
  - Odómetro mediano
- Visualizaciones interactivas:
  - Histograma
  - Gráfico de dispersión
- Vista previa del dataset filtrado
- Manejo seguro de casos sin registros (UX robusta)

---

## 🛠️ Tecnologías utilizadas

- **Python 3**
- **Streamlit** – desarrollo del dashboard
- **Pandas** – manipulación y análisis de datos
- **Plotly Express** – visualizaciones interactivas

---

## 📁 Estructura del proyecto

```text
.
├── README.md
├── app.py
├── vehicles_us.csv
├── requirements.txt
└── notebooks
    └── EDA.ipynb
