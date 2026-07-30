 
import pandas as pd
import streamlit as st

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


# =====================================================
# Prepare Clustering Data
# =====================================================
@st.cache_data
def prepare_cluster_data(df):
    """
    Aggregate sales by Sub-Category.
    """

    cluster_df = (
        df.groupby("Sub-Category")
        .agg(
            Total_Sales=("Sales", "sum"),
            Average_Sales=("Sales", "mean"),
            Orders=("Order ID", "count")
        )
        .reset_index()
    )

    return cluster_df


# =====================================================
# Scale Features
# =====================================================
@st.cache_data
def scale_features(cluster_df):

    features = cluster_df[
        [
            "Total_Sales",
            "Average_Sales",
            "Orders"
        ]
    ]

    scaler = StandardScaler()

    scaled = scaler.fit_transform(features)

    return scaled


# =====================================================
# Run KMeans
# =====================================================
@st.cache_data
def run_kmeans(cluster_df, n_clusters=3):

    data = cluster_df.copy()

    scaled = scale_features(data)

    model = KMeans(
        n_clusters=n_clusters,
        random_state=42,
        n_init=10
    )

    data["Cluster"] = model.fit_predict(scaled)

    return data


# =====================================================
# Rename Cluster Labels
# =====================================================
@st.cache_data
def label_clusters(cluster_df):

    data = cluster_df.copy()

    cluster_sales = (
        data.groupby("Cluster")["Total_Sales"]
        .mean()
        .sort_values()
    )

    labels = {
        cluster_sales.index[0]: "Low Demand",
        cluster_sales.index[1]: "Medium Demand",
        cluster_sales.index[2]: "High Demand"
    }

    data["Demand Segment"] = data["Cluster"].map(labels)

    return data


# =====================================================
# Complete Pipeline
# =====================================================
@st.cache_data
def demand_segmentation(df):

    cluster_df = prepare_cluster_data(df)

    cluster_df = run_kmeans(cluster_df)

    cluster_df = label_clusters(cluster_df)

    return cluster_df


# =====================================================
# Cluster Summary
# =====================================================
@st.cache_data
def cluster_summary(df):

    segmented = demand_segmentation(df)

    summary = (
        segmented.groupby("Demand Segment")
        .size()
        .reset_index(name="Sub-Categories")
    )

    return summary


# =====================================================
# High Demand Products
# =====================================================
@st.cache_data
def high_demand_products(df):

    segmented = demand_segmentation(df)

    return segmented[
        segmented["Demand Segment"] == "High Demand"
    ]


# =====================================================
# Medium Demand Products
# =====================================================
@st.cache_data
def medium_demand_products(df):

    segmented = demand_segmentation(df)

    return segmented[
        segmented["Demand Segment"] == "Medium Demand"
    ]


# =====================================================
# Low Demand Products
# =====================================================
@st.cache_data
def low_demand_products(df):

    segmented = demand_segmentation(df)

    return segmented[
        segmented["Demand Segment"] == "Low Demand"
    ]