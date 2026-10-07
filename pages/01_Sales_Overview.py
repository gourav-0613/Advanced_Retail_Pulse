# pyrefly: ignore [missing-import]
import streamlit as st
# pyrefly: ignore [missing-import]
import plotly.express as px
# pyrefly: ignore [missing-import]
import plotly.graph_objects as go

from utils.preprocessing import (
    load_data,
    clean_data,
    create_features,
    calculate_kpis,
    yearly_sales,
    monthly_sales,
    region_sales,
    category_sales,
    top_subcategories,
    filter_data,
    get_regions,
    get_categories
)

from components.ui import sidebar_brand, page_header, style_fig

# ----------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------

st.set_page_config(
    page_title="RetailPulse | Sales Overview",
    page_icon="assets/retailpulse-logo.png",
    layout="wide"
)

# ----------------------------------------------------
# LOAD CSS
# ----------------------------------------------------

with open("assets/css.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

# =====================================================
# Sidebar Branding
# =====================================================

sidebar_brand()

# ----------------------------------------------------
# LOAD DATA
# ----------------------------------------------------

df = load_data("data/train.csv")
df = clean_data(df)
df = create_features(df)

# ----------------------------------------------------
# SIDEBAR FILTERS
# ----------------------------------------------------

st.sidebar.title("Dashboard Filters")

region = st.sidebar.selectbox(
    "Region",
    ["All"] + get_regions(df)
)

category = st.sidebar.selectbox(
    "Category",
    ["All"] + get_categories(df)
)

filtered_df = filter_data(
    df,
    region,
    category
)

# ----------------------------------------------------
# TITLE & HEADER
# ----------------------------------------------------

page_header("dashboard", "Sales Overview Dashboard", "Analyze historical retail sales using interactive visualizations.")

st.markdown("---")

# ----------------------------------------------------
# KPI
# ----------------------------------------------------

kpi = calculate_kpis(filtered_df)
st.subheader("Business KPIs")
c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Total Sales",
    f"${kpi['Total Sales']:,.0f}"
)

c2.metric(
    "Average Sales",
    f"${kpi['Average Sales']:,.2f}"
)

c3.metric(
    "Orders",
    kpi["Total Orders"]
)

c4.metric(
    "Customers",
    kpi["Total Customers"]
)

st.markdown("---")

# ----------------------------------------------------
# YEARLY SALES
# ----------------------------------------------------

year_df = yearly_sales(filtered_df)

fig = px.bar(
    year_df,
    x="Year",
    y="Sales",
    title="Yearly Sales",
)

fig.update_traces(
    texttemplate="$%{y:,.0f}",
    textposition="outside",
    cliponaxis=False,
)

fig.update_xaxes(dtick=1, tickformat="d")
fig.update_yaxes(tickprefix="$", tickformat="~s")

fig = style_fig(fig, height=450, margin_r=20)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ----------------------------------------------------
# MONTHLY SALES
# ----------------------------------------------------

month_df = monthly_sales(filtered_df)

fig2 = px.line(
    month_df,
    x="Order Date",
    y="Sales",
    markers=True,
    title="Monthly Sales Trend"
)

fig2 = style_fig(fig2, height=450, margin_r=20)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# ----------------------------------------------------
# REGION & CATEGORY
# ----------------------------------------------------

left, right = st.columns(2)

with left:
    reg = region_sales(filtered_df)

    fig3 = px.bar(
        reg,
        x="Region",
        y="Sales",
        title="Region Wise Sales"
    )

    fig3 = style_fig(fig3, height=420, margin_r=20)

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

with right:
    cat = category_sales(filtered_df)

    fig4 = px.pie(
        cat,
        names="Category",
        values="Sales",
        title="Category Share"
    )

    fig4.update_traces(
        textposition="inside",
        textinfo="percent+label"
    )

    fig4 = style_fig(fig4, height=420, margin_r=20)

    st.plotly_chart(
        fig4,
        use_container_width=True
    )

# ----------------------------------------------------
# TOP SUB CATEGORIES
# ----------------------------------------------------

top = top_subcategories(filtered_df)

fig5 = px.bar(
    top,
    x="Sales",
    y="Sub-Category",
    orientation="h",
    title="Top Selling Sub Categories",
)

fig5.update_traces(
    texttemplate="$%{x:,.0f}",
    textposition="outside",
    cliponaxis=False,
)

fig5 = style_fig(fig5, height=450, margin_r=70)

st.plotly_chart(
    fig5,
    use_container_width=True
)

# ----------------------------------------------------
# DATA PREVIEW
# ----------------------------------------------------

with st.expander("View Dataset Preview"):
    st.dataframe(
        filtered_df,
        use_container_width=True,
        height=400,
    )