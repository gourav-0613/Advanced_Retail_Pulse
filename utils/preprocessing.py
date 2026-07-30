 
import pandas as pd
import streamlit as st


# ===========================
# Load Dataset
# ===========================
@st.cache_data
def load_data(file_path):
    """
    Load Superstore dataset.
    """
    df = pd.read_csv(file_path, encoding="latin1")

    # Convert Order Date
    df["Order Date"] = pd.to_datetime(
        df["Order Date"],
        dayfirst=True,
        errors="coerce"
    )

    # Remove invalid dates
    df = df.dropna(subset=["Order Date"])

    return df


# ===========================
# Clean Dataset
# ===========================
@st.cache_data
def clean_data(df):
    """
    Basic preprocessing.
    """

    data = df.copy()

    # Remove duplicates
    data = data.drop_duplicates()

    # Remove missing Sales
    data = data.dropna(subset=["Sales"])

    # Sales should be numeric
    data["Sales"] = pd.to_numeric(
        data["Sales"],
        errors="coerce"
    )

    data = data.dropna(subset=["Sales"])

    return data


# ===========================
# Feature Engineering
# ===========================
@st.cache_data
def create_features(df):
    """
    Create useful time features.
    """

    data = df.copy()

    data["Year"] = data["Order Date"].dt.year
    data["Month"] = data["Order Date"].dt.month
    data["Month Name"] = data["Order Date"].dt.strftime("%b")
    data["Quarter"] = data["Order Date"].dt.quarter

    return data


# ===========================
# Monthly Sales
# ===========================
@st.cache_data
def monthly_sales(df):
    """
    Aggregate monthly sales.
    """

    monthly = (
        df.groupby(
            pd.Grouper(
                key="Order Date",
                freq="ME"
            )
        )["Sales"]
        .sum()
        .reset_index()
    )

    monthly.columns = [
        "Order Date",
        "Sales"
    ]

    return monthly


# ===========================
# Yearly Sales
# ===========================
@st.cache_data
def yearly_sales(df):
    """
    Aggregate yearly sales.
    """

    yearly = (
        df.groupby("Year")["Sales"]
        .sum()
        .reset_index()
    )

    return yearly


# ===========================
# Filter Data
# ===========================
@st.cache_data
def filter_data(df, region="All", category="All"):
    """
    Filter dataframe.
    """

    data = df.copy()

    if region != "All":
        data = data[data["Region"] == region]

    if category != "All":
        data = data[data["Category"] == category]

    return data


# ===========================
# Dropdown Values
# ===========================
@st.cache_data
def get_regions(df):

    return sorted(df["Region"].dropna().unique())


@st.cache_data
def get_categories(df):

    return sorted(df["Category"].dropna().unique())


# ===========================
# KPI Metrics
# ===========================
@st.cache_data
def calculate_kpis(df):
    """
    Dashboard KPIs.
    """

    total_sales = df["Sales"].sum()

    average_sales = df["Sales"].mean()

    total_orders = df["Order ID"].nunique()

    total_customers = df["Customer ID"].nunique()

    return {
        "Total Sales": total_sales,
        "Average Sales": average_sales,
        "Total Orders": total_orders,
        "Total Customers": total_customers,
    }


# ===========================
# Date Filter
# ===========================
@st.cache_data
def filter_by_date(df, start_date, end_date):
    """
    Filter dataframe by date.
    """

    data = df.copy()

    mask = (
        (data["Order Date"] >= pd.to_datetime(start_date))
        &
        (data["Order Date"] <= pd.to_datetime(end_date))
    )

    return data.loc[mask]


# ===========================
# Top Categories
# ===========================
@st.cache_data
def top_categories(df, n=10):

    return (
        df.groupby("Category")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(n)
        .reset_index()
    )


# ===========================
# Top Sub Categories
# ===========================
@st.cache_data
def top_subcategories(df, n=10):

    return (
        df.groupby("Sub-Category")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(n)
        .reset_index()
    )


# ===========================
# Region Sales
# ===========================
@st.cache_data
def region_sales(df):

    return (
        df.groupby("Region")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )


# ===========================
# Category Sales
# ===========================
@st.cache_data
def category_sales(df):

    return (
        df.groupby("Category")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )