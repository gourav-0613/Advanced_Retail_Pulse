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

from utils.clustering import (
    demand_segmentation,
    cluster_summary,
)

from components.ui import sidebar_brand, page_header, style_fig

# =====================================================
# Page Configuration
# =====================================================

st.set_page_config(
    page_title="RetailPulse | Demand Segments",
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

page_header("demand", "Demand Segments", "Identify product demand groups using K-Means Clustering.")

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

st.sidebar.header("Clustering Settings")

cluster_count = st.sidebar.slider(
    "Number of Clusters",
    min_value=2,
    max_value=6,
    value=3,
    disabled=True,
    help="Fixed at 3 clusters (High / Medium / Low demand)"
)
st.sidebar.caption("Fixed at 3 clusters (High / Medium / Low demand)")

# =====================================================
# Prepare Data
# =====================================================

cluster_df = demand_segmentation(df)

summary = cluster_summary(df)

# =====================================================
# KPI Cards
# =====================================================

total_products = len(cluster_df)
st.subheader("Demand Summary")

avg_sales = cluster_df["Total_Sales"].mean()
avg_sale_order = cluster_df["Average_Sales"].mean()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Products",
        total_products,
    )

with col2:
    st.metric(
        "Average Sales",
        f"${avg_sales:,.0f}",
    )

with col3:
    st.metric(
        "Avg Sale per Order",
        f"${avg_sale_order:,.0f}",
        help="Mean of the average sale value across sub-categories",
    )

st.divider()

# =====================================================
# Scatter Plot
# =====================================================

st.subheader("Demand Cluster Visualization")

fig = px.scatter(
    cluster_df,
    x="Average_Sales",
    y="Total_Sales",
    color="Demand Segment",
    hover_name="Sub-Category",
    size="Orders",
    color_discrete_map={
        "High Demand": "#22C55E",
        "Medium Demand": "#F59E0B",
        "Low Demand": "#EF4444",
    }
)

fig.update_layout(
    xaxis_title="Average Sales",
    yaxis_title="Total Sales",
)

fig = style_fig(fig, height=500, margin_r=20)

st.plotly_chart(
    fig,
    use_container_width=True,
)

st.markdown("<br>", unsafe_allow_html=True)
st.divider()

# =====================================================
# Cluster Summary
# =====================================================

st.subheader("Product Demand Segments")

st.dataframe(
    cluster_df.sort_values(
        [
            "Demand Segment",
            "Total_Sales"
        ],
        ascending=[
            True,
            False
        ]
    ),
    use_container_width=True,
    hide_index=True,
)

st.divider()

# =====================================================
# Cluster Statistics
# =====================================================

st.subheader("Cluster Summary")

st.dataframe(
    summary,
    use_container_width=True,
    hide_index=True,
)

csv = cluster_df.to_csv(index=False).encode("utf-8")

st.download_button(
    "Download Demand Segment Report",
    csv,
    "demand_segments.csv",
    "text/csv",
)