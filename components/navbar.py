import streamlit as st


def load_css():
    st.markdown("""
    <style>

    .main{
        padding-top:1rem;
    }

    .sidebar-logo{
        text-align:center;
        padding-bottom:15px;
    }

    .sidebar-logo h2{
        color:#4CAF50;
        margin-bottom:0px;
    }

    .sidebar-logo p{
        color:gray;
        font-size:14px;
    }

    </style>
    """, unsafe_allow_html=True)


def render_sidebar():

    load_css()

    with st.sidebar:

        st.markdown("""
        <div class="sidebar-logo">

        <h2>📊 Smart Sales Dashboard</h2>

        <p>Week 3 & Week 4 Project</p>

        </div>

        """, unsafe_allow_html=True)

        st.divider()

        st.markdown("### Navigation")