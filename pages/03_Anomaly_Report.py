# pyrefly: ignore [missing-import]
import streamlit as st
import pandas as pd
# pyrefly: ignore [missing-import]
import plotly.express as px

from utils.preprocessing import (
    load_data,
    clean_data,
    create_features,
)

from utils.anomaly import (
    detect_anomalies,
    anomaly_summary,
)

from components.ui import sidebar_brand, page_header, style_fig

# =====================================================
# Page Configuration
# =====================================================

st.set_page_config(
    page_title="RetailPulse | Anomaly Report",
    page_icon="assets/retailpulse-logo.png",
    layout="wide",
)

# =====================================================
# Load CSS
# =====================================================

with open("assets/css.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True,
    )

# =====================================================
# Sidebar Branding
# =====================================================

sidebar_brand()

# =====================================================
# Page Header
# =====================================================

page_header("warning", "Anomaly Report", "Detect unusual retail sales patterns using Isolation Forest and Z-Score.")

st.markdown("---")

# =====================================================
# Load Dataset
# =====================================================

df = load_data("data/train.csv")
df = clean_data(df)
df = create_features(df)

# =====================================================
# Sidebar
# =====================================================

st.sidebar.header("Analysis Filters")

filter_type = st.sidebar.radio(
    "Analyze By",
    [
        "Overall",
        "Category",
        "Region",
    ],
)

filtered_df = df.copy()

# =====================================================
# Category Filter
# =====================================================

if filter_type == "Category":

    category = st.sidebar.selectbox(
        "Category",
        sorted(df["Category"].unique())
    )

    filtered_df = df[
        df["Category"] == category
    ]

# =====================================================
# Region Filter
# =====================================================

elif filter_type == "Region":

    region = st.sidebar.selectbox(
        "Region",
        sorted(df["Region"].unique())
    )

    filtered_df = df[
        df["Region"] == region
    ]

# =====================================================
# Detect Anomalies
# =====================================================

anomaly_df = detect_anomalies(filtered_df)

summary = anomaly_summary(filtered_df)

method = st.sidebar.selectbox(
    "Detection Method",
    [
        "Isolation Forest",
        "Z-Score"
    ]
)

if method == "Isolation Forest":
    anomaly_df["Status"] = anomaly_df["Anomaly"]
else:
    anomaly_df["Status"] = anomaly_df["Z_Anomaly"]


# =====================================================
# KPI Cards
# =====================================================

total_points = summary["Total Weeks"]
anomaly_count = summary["Detected Anomalies"]
normal_count = summary["Normal Weeks"]

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Weeks",
        total_points,
    )

with col2:
    st.metric(
        "Anomalies",
        anomaly_count,
    )

with col3:
    st.metric(
        "Normal Weeks",
        normal_count,
    )

st.divider()

# =====================================================
# Prepare Plot Data
# =====================================================

plot_df = anomaly_df.copy()

# =====================================================
# Interactive Chart
# =====================================================

st.subheader("Weekly Sales with Detected Anomalies")

fig = px.scatter(
    plot_df,
    x="Order Date",
    y="Sales",
    color="Status",
    size="Sales",
    hover_data=["Sales"],
    title=f"{method} Detection",
    color_discrete_map={
        "Normal": "#60A5FA",
        "Anomaly": "#EF4444",
    }
)

fig.update_traces(marker=dict(size=12))

fig.update_layout(
    xaxis_title="Week",
    yaxis_title="Sales",
    hovermode="closest",
)

fig = style_fig(fig, height=500, margin_r=20)

st.plotly_chart(
    fig,
    use_container_width=True,
)

st.markdown("<br>", unsafe_allow_html=True)

st.divider()

# =====================================================
# Anomaly Table
# =====================================================

st.subheader("Detected Anomalies")

if "Status" in plot_df.columns:
    anomalies_only = plot_df[
        plot_df["Status"] == "Anomaly"
    ].copy()
else:
    anomalies_only = pd.DataFrame()

if anomalies_only.empty:

    st.success(
        "No anomalies detected for the selected filter."
    )

else:

    display_df = anomalies_only.copy()

    display_df["Order Date"] = (
        pd.to_datetime(display_df["Order Date"])
        .dt.strftime("%b %Y")
    )

    keep_cols = [
        col
        for col in [
            "Order Date",
            "Sales",
            "Status",
            "Z_Score",
        ]
        if col in display_df.columns
    ]

    st.dataframe(
        display_df[keep_cols],
        use_container_width=True,
        hide_index=True,
    )

    csv = display_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download Anomaly Report",
        data=csv,
        file_name="anomaly_report.csv",
        mime="text/csv",
    )

st.divider()

st.success(
    f"Detection Method: {method}"
)