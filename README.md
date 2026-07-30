<h1 align="center">
🛍️ RetailPulse
</h1>

<h3 align="center">
Forecasting & Demand Analytics Dashboard
</h3>

<p align="center">
An Interactive AI-powered Retail Analytics Dashboard built with Streamlit for Sales Forecasting, Demand Segmentation, Business Insights and Anomaly Detection.
</p>

---

<p align="center">

<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
<img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white"/>
<img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white"/>
<img src="https://img.shields.io/badge/Numpy-013243?style=for-the-badge&logo=numpy&logoColor=white"/>
<img src="https://img.shields.io/badge/Scikit--Learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white"/>
<img src="https://img.shields.io/badge/Statsmodels-0C55A5?style=for-the-badge"/>
<img src="https://img.shields.io/badge/XGBoost-EC6C00?style=for-the-badge"/>
<img src="https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white"/>
<img src="https://img.shields.io/badge/Machine%20Learning-00C853?style=for-the-badge"/>
<img src="https://img.shields.io/badge/Forecasting-3949AB?style=for-the-badge"/>
<img src="https://img.shields.io/badge/Data%20Analytics-6A1B9A?style=for-the-badge"/>

</p>

---

# 📖 Overview

RetailPulse is an end-to-end Machine Learning and Business Analytics dashboard built with Streamlit that helps retail businesses analyze historical sales, forecast future demand, detect anomalies, segment products, and explain model predictions using SHAP.

The project combines data preprocessing, time-series forecasting, anomaly detection, clustering, and interactive business visualization into a single production-style analytics dashboard.

The application is deployed as an interactive **Streamlit Dashboard** where users can explore business insights without writing code.

---

# 🌐 Live Demo

### 🚀 Streamlit App

> **Paste your deployed Streamlit link here**

```text
https://retailpulse-rgq7dm3dok9ap7bhmappdcu.streamlit.app/
```
### Google Colab Link:
```text
https://colab.research.google.com/drive/1CTzulpUN_2HDFRcjteue_1XjjzAgT0Ek?usp=sharing
```

---

# 📸 Dashboard Preview

## Sales Overview

<p align="center">
  <img src="assets/dashboard.png" width="100%">
</p>

---

## Forecast Explorer

<p align="center">
  <img src="assets/forecast.png" width="100%">
</p>

---

## Anomaly Report

<p align="center">
  <img src="assets/anomaly.png" width="100%">
</p>

---

## Demand Segments

<p align="center">
  <img src="assets/clustering.png" width="100%">
</p>
---

# 🎯 Project Status

| Module | Status |
|----------|--------|
| 📊 Data Cleaning | 🟩🟩🟩🟩🟩 100% |
| 📈 Exploratory Data Analysis | 🟩🟩🟩🟩🟩 100% |
| 🔮 Sales Forecasting | 🟩🟩🟩🟩🟩 100% |
| 🚨 Anomaly Detection | 🟩🟩🟩🟩🟩 100% |
| 📦 Demand Segmentation | 🟩🟩🟩🟩🟩 100% |
| 🌐 Streamlit Dashboard | 🟩🟩🟩🟩🟩 100% |

---

#  Features

✅ Interactive Streamlit Dashboard

✅ Sales Trend Analysis

✅ Monthly Sales Forecasting using Gradient Boosting & SARIMA

✅ SHAP Explainability (Feature Importance)

✅ Walk-Forward Backtesting (TimeSeriesSplit)

✅ Isolation Forest Anomaly Detection

✅ Product Demand Segmentation using KMeans

✅ Dynamic Business Insights

✅ Interactive Plotly Charts

✅ Downloadable Visual Analytics

---

# ⚡ Dashboard Modules

| Page | Description |
|-------|-------------|
| 📊 Sales Overview | KPI Cards, Monthly Sales, Region & Category Analysis |
| 🔮 Forecast Explorer | Future Sales Forecasting using ML Models |
| 🚨 Anomaly Report | Detects abnormal sales patterns using Isolation Forest |
| 📦 Demand Segments | Product Clustering using KMeans |

---

# 📊 Machine Learning Pipeline

```text
Retail Sales Dataset
        │
        ▼
Data Cleaning
        │
        ▼
Feature Engineering
        │
        ▼
Exploratory Data Analysis
        │
        ▼
Time Series Aggregation
        │
        ▼
Forecasting Models
        │
        ├────────► Gradient Boosting Regressor
        │
        ├────────► SARIMA
        │
        ├────────► Walk-Forward Backtesting
        │
        └────────► SHAP Explainability
        │
        ▼
Anomaly Detection
(Isolation Forest)
        │
        ▼
Demand Segmentation
(KMeans Clustering)
        │
        ▼
Interactive Streamlit Dashboard
```

---

# 📈 Visualizations

- Monthly Sales Trend
- Sales by Category
- Sales by Region
- Forecast vs Actual
- Forecast Confidence Bands
- Cluster Distribution
- Anomaly Detection
- Interactive Plotly Charts

---

# 🧠 Machine Learning Models

| Model | Purpose |
|---------|----------|
| Gradient Boosting Regressor | Sales Forecasting |
| SARIMA | Time Series Forecasting |
| Isolation Forest | Sales Anomaly Detection |
| KMeans | Product Demand Segmentation |
| SHAP | Model Explainability |

---

# 📂 Project Structure

```text
RetailPulse
│
├── app.py
├── analysis.ipynb
├── retrain_model.py
├── model.pkl
├── requirements.txt
├── README.md
│
├── assets/
├── components/
├── charts/
├── data/
├── pages/
│
├── utils/
│      ├── preprocessing.py
│      ├── forecasting.py
│      ├── anomaly.py
│      ├── clustering.py
│      └── charts.py
│
└── .streamlit/
```

---

# ⚙️ Tech Stack

| Category | Technology |
|------------|------------|
| Language | Python |
| Dashboard | Streamlit |
| Data Analysis | Pandas, NumPy |
| Visualization | Plotly, Matplotlib |
| Machine Learning | Scikit-Learn |
| Time Series | Statsmodels |
| Explainability | SHAP |
| Forecast Validation | TimeSeriesSplit |
| Clustering | KMeans |
| Anomaly Detection | Isolation Forest |

---

# 🛠️ Installation

```bash
git clone https://github.com/<YOUR_GITHUB_USERNAME>/RetailPulse.git

cd RetailPulse

pip install -r requirements.txt

streamlit run app.py
```

---

# 📊 Dataset

The project uses retail sales transaction data containing:

- Order Date
- Sales
- Region
- Category
- Sub-Category
- Quantity
- Discount
- Profit

---

# 📌 Future Improvements

- LSTM-based Forecasting
- LightGBM / CatBoost Models
- Inventory Optimization
- Customer Segmentation
- PDF Report Generation
- Cloud Deployment
- User Authentication

---

# 🏆 Highlights

- 📈 Gradient Boosting & SARIMA Forecasting
- 🔍 SHAP Explainability
- 📊 Walk-Forward Backtesting using TimeSeriesSplit
- 🚨 Isolation Forest for Anomaly Detection
- 📦 KMeans Demand Segmentation
- 🎨 Interactive Streamlit Dashboard
- 📉 Business KPI Visualizations

# 👨‍💻 Author

**Gourav Sanadhya**

B.Tech CSE (Artificial Intelligence)

SKIT Jaipur

---

<h3 align="center">

⭐ If you found this project useful, don't forget to Star this repository!

</h3>
