import pandas as pd
import numpy as np
import streamlit as st

from sklearn.ensemble import IsolationForest
from scipy.stats import zscore


# =====================================================
# Weekly Sales
# =====================================================
@st.cache_data
def prepare_weekly_sales(df):
    """
    Convert daily sales into weekly sales.
    """

    weekly = (
        df.groupby(
            pd.Grouper(
                key="Order Date",
                freq="W"
            )
        )["Sales"]
        .sum()
        .reset_index()
    )

    return weekly


# =====================================================
# Isolation Forest
# =====================================================
@st.cache_data
def isolation_forest_detection(weekly_df):

    data = weekly_df.copy()

    model = IsolationForest(
        contamination=0.05,
        random_state=42
    )

    data["Anomaly"] = model.fit_predict(
        data[["Sales"]]
    )

    data["Anomaly"] = data["Anomaly"].map(
        {
            1: "Normal",
            -1: "Anomaly"
        }
    )

    return data


# =====================================================
# Z-Score Detection
# =====================================================
@st.cache_data
def zscore_detection(weekly_df, threshold=2.5):

    data = weekly_df.copy()

    data["Z-Score"] = np.abs(
        zscore(data["Sales"])
    )

    data["Z_Anomaly"] = np.where(
        data["Z-Score"] > threshold,
        "Anomaly",
        "Normal"
    )

    return data


# =====================================================
# Combined Detection
# =====================================================
@st.cache_data
def detect_anomalies(df):

    weekly = prepare_weekly_sales(df)

    iso = isolation_forest_detection(weekly)

    z = zscore_detection(weekly)

    result = iso.merge(
        z[
            [
                "Order Date",
                "Z-Score",
                "Z_Anomaly"
            ]
        ],
        on="Order Date"
    )

    return result


# =====================================================
# Only Anomalies
# =====================================================
@st.cache_data
def anomaly_table(df):

    detected = detect_anomalies(df)

    anomalies = detected[
        detected["Anomaly"] == "Anomaly"
    ].copy()

    anomalies = anomalies.sort_values(
        "Order Date"
    )

    return anomalies


# =====================================================
# Summary
# =====================================================
@st.cache_data
def anomaly_summary(df):

    anomalies = anomaly_table(df)

    total_weeks = len(prepare_weekly_sales(df))

    return {
        "Total Weeks": total_weeks,
        "Detected Anomalies": len(anomalies),
        "Normal Weeks": total_weeks - len(anomalies)
    }