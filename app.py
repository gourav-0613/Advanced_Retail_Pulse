# pyrefly: ignore [missing-import]
import streamlit as st
# pyrefly: ignore [missing-import]
import matplotlib.pyplot as plt
# pyrefly: ignore [missing-import]
import numpy as np
import pandas as pd
# pyrefly: ignore [missing-import]
import joblib
# pyrefly: ignore [missing-import]
import shap
import calendar

from components.ui import sidebar_brand, page_header, feature_cards, hero_image, style_fig

# -----------------------------------------------------
# Page Config (Streamlit rules: must be at the top!)
# -----------------------------------------------------
st.set_page_config(
    page_title="RetailPulse: Forecasting & Demand Analytics",
    page_icon="assets/retailpulse-logo.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------------------------------
# Load CSS
# -----------------------------------------------------
try:
    with open("assets/css.css") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True,
        )
except FileNotFoundError:
    pass

# =====================================================
# Sidebar Branding
# =====================================================
sidebar_brand()

# -----------------------------------------------------
# Header
# -----------------------------------------------------
page_header("home", "RetailPulse: Forecasting & Demand Analytics", "Retail Intelligence Dashboard")
hero_image("assets/hero.svg")

st.markdown("---")

# -----------------------------------------------------
# Project Overview
# -----------------------------------------------------
st.subheader("Project Overview")

st.write(
    """
RetailPulse is an end-to-end AI-powered retail analytics dashboard built
using **Python, Streamlit, Scikit-learn and Machine Learning**.

The dashboard enables business users to analyze historical sales,
forecast future demand, detect anomalies and identify demand segments
through interactive visualizations.
"""
)

st.markdown("---")

# -----------------------------------------------------
# Features
# -----------------------------------------------------
st.subheader("Dashboard Features")

feature_cards([
    {
        "icon": "dashboard",
        "title": "Sales Overview",
        "desc": "KPIs, yearly/monthly trends, region & category analysis"
    },
    {
        "icon": "forecast",
        "title": "Forecast Explorer",
        "desc": "Gradient Boosting vs SARIMA forecasts with MAE/RMSE/MAPE"
    },
    {
        "icon": "warning",
        "title": "Anomaly Report",
        "desc": "Isolation Forest and Z-Score on weekly sales"
    },
    {
        "icon": "demand",
        "title": "Demand Segments",
        "desc": "K-Means product demand clusters"
    }
])

# -----------------------------------------------------
# Models & Dataset
# -----------------------------------------------------
feature_cards([
    {
        "icon": "ai",
        "title": "Models Used",
        "bullets": [
            "Gradient Boosting Regressor",
            "SARIMA",
            "Isolation Forest",
            "K-Means Clustering"
        ]
    },
    {
        "icon": "database",
        "title": "Dataset",
        "desc": "Superstore Sales Dataset, 9,800 records, 2015-2018"
    }
])

st.markdown("---")

# =====================================================
# SHAP Visualizer Section (Direct — no FastAPI)
# =====================================================
st.subheader("🤖 Live Model & SHAP Explanation")

st.caption(
    "Select a future month to get a real-time sales forecast from the "
    "GradientBoosting model, with SHAP feature impact explanation."
)

FEATURE_NAMES = ["Year", "Month", "Quarter", "Lag1", "Lag2", "Lag3", "Rolling3", "Rolling6"]

# --- Load model & SHAP explainer once (cached) ---
@st.cache_resource
def _load_model_and_explainer():
    try:
        model = joblib.load("model.pkl")
        explainer = shap.TreeExplainer(model)
        return model, explainer
    except Exception:
        return None, None

# --- Load dataset to derive lag/rolling context ---
@st.cache_data
def _load_recent_sales():
    try:
        df_raw = pd.read_csv("data/train.csv")
        df_raw["Order Date"] = pd.to_datetime(df_raw["Order Date"], dayfirst=True, errors="coerce")
        monthly = (
            df_raw.groupby(df_raw["Order Date"].dt.to_period("M"))["Sales"]
            .sum()
            .reset_index()
        )
        monthly["Order Date"] = monthly["Order Date"].dt.to_timestamp()
        monthly = monthly.sort_values("Order Date").reset_index(drop=True)
        return monthly
    except Exception:
        return None

model, explainer = _load_model_and_explainer()
recent_sales = _load_recent_sales()

# --- Input Controls ---
api_col1, api_col2 = st.columns(2)

with api_col1:
    sel_year = st.selectbox(
        "Select Year",
        options=list(range(2014, 2020)),
        index=4,   # default 2018
        key="api_year"
    )
with api_col2:
    sel_month = st.selectbox(
        "Select Month",
        options=list(range(1, 13)),
        format_func=lambda m: pd.Timestamp(year=2000, month=m, day=1).strftime("%B"),
        key="api_month"
    )

# Derive quarter + lag/rolling from dataset's last N months
sel_quarter = (sel_month - 1) // 3 + 1

if recent_sales is not None and not recent_sales.empty and "Sales" in recent_sales.columns:
    tail = recent_sales["Sales"].tail(6).values
    lag1   = float(tail[-1]) if len(tail) >= 1 else 0.0
    lag2   = float(tail[-2]) if len(tail) >= 2 else lag1
    lag3   = float(tail[-3]) if len(tail) >= 3 else lag2
    roll3  = float(np.mean(tail[-3:])) if len(tail) >= 3 else lag1
    roll6  = float(np.mean(tail[-6:])) if len(tail) >= 6 else lag1
else:
    lag1 = lag2 = lag3 = roll3 = roll6 = 0.0

if st.button("🔮 Get Sales Forecast", key="api_predict_btn"):
    if model is None or explainer is None:
        st.error("Forecast model or explainer could not be loaded. Ensure model.pkl exists.")
    else:
        try:
            input_df = pd.DataFrame(
                [[
                    float(sel_year), float(sel_month), float(sel_quarter),
                    lag1, lag2, lag3, roll3, roll6
                ]],
                columns=FEATURE_NAMES
            )

            with st.spinner("Computing forecast..."):
                predicted = float(model.predict(input_df)[0])
                shap_values = explainer.shap_values(input_df)
                exp_val = explainer.expected_value
                base_value = float(exp_val[0]) if isinstance(exp_val, (list, np.ndarray)) else float(exp_val)

            st.success(
                f"📈 Predicted Sales for "
                f"{calendar.month_abbr[sel_month]} {sel_year}: "
                f"**${predicted:,.2f}**"
            )

            # --- SHAP Chart ---
            st.markdown("#### SHAP Feature Impact")
            shap_vals = shap_values[0] if isinstance(shap_values, list) else shap_values.flatten()

            fig, ax = plt.subplots(figsize=(8, 4))
            y_pos  = np.arange(len(FEATURE_NAMES))
            colors = ["#ff0051" if v > 0 else "#008bfb" for v in shap_vals]

            ax.barh(y_pos, shap_vals, align="center", color=colors)
            ax.set_yticks(y_pos)
            ax.set_yticklabels(FEATURE_NAMES)
            ax.invert_yaxis()
            ax.set_xlabel("SHAP Value (Impact on Prediction)")
            ax.set_title(
                f"Base prediction: ${base_value:,.2f}",
                fontsize=10, color="gray"
            )
            ax.set_facecolor("#0E1117")
            fig.patch.set_facecolor("#0E1117")
            ax.tick_params(colors="white")
            ax.xaxis.label.set_color("white")
            ax.title.set_color("white")

            st.pyplot(fig)
        except Exception as e:
            st.error(f"Forecast could not be generated: {e}")

st.markdown("---")

# -----------------------------------------------------
# Footer
# -----------------------------------------------------
st.success(
    "Open the pages from the left sidebar to explore the complete dashboard."
)
