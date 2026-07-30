 
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

brand1, brand2 = st.sidebar.columns([1, 4], gap="small")

with brand1:
    st.image(
        "assets/retailpulse-logo.png",
        width=48
    )

with brand2:
    st.markdown(
        """
        <div style="padding-top:10px;">
            <h2 style="margin:0;font-size:24px;font-weight:700;color:white;">
                Retail Pulse
            </h2>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.sidebar.markdown("---")


# ----------------------------------------------------
# LOAD DATA
# ----------------------------------------------------

df = load_data("data/train.csv")

df = clean_data(df)

df = create_features(df)

# ----------------------------------------------------
# SIDEBAR
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
# TITLE
# ----------------------------------------------------

col1, col2 = st.columns([0.6, 9])

with col1:
    st.image(
        "assets/icons/icon-dashboard.svg",
        width=45,
    )

with col2:
    st.markdown(
        "<h1 style='margin-top:8px;'>Sales Overview Dashboard</h1>",
        unsafe_allow_html=True,
    )

st.caption(
    "Analyze historical retail sales using interactive visualizations."
)

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
    text_auto=True
)

fig.update_layout(
    template="plotly_dark",
    height=450,
    margin=dict(
        l=20,
        r=20,
        t=60,
        b=20
    ),
    title_x=0.02,
)

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

fig2.update_layout(
    template="plotly_dark",
    height=450,
    title_x=0.02,
    margin=dict(
        l=20,
        r=20,
        t=60,
        b=20
    )
)

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

    fig3.update_layout(
    template="plotly_dark",
    height=420,
    title_x=0.02,
    )

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

    fig4.update_layout(
    template="plotly_dark",
    height=420,
    title_x=0.02,
    )

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
    text_auto=True
)

fig5.update_layout(
    template="plotly_dark",
    height=450,
    title_x=0.02,
)

st.plotly_chart(
    fig5,
    use_container_width=True
)

# ----------------------------------------------------
# DATA
# ----------------------------------------------------

with st.expander("View Dataset Preview"):

    st.dataframe(
        filtered_df,
        use_container_width=True,
        height=400,
    )