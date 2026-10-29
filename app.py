
import streamlit as st

# Application configuration
st.set_page_config(
    page_title="Retail Sales Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Define the pages
pages = [
    st.Page(
        "home.py",
        title="Home",
        icon="🏠",
        default=True
    ),

    st.Page(
        "pages/1_Sales_Overview.py",
        title="Sales Overview",
        icon="📈"
    ),

    st.Page(
        "pages/2_Product_Performance.py",
        title="Product Performance",
        icon="🛍️"
    ),

    st.Page(
        "pages/3_Customer_Analytics.py",
        title="Customer Analytics",
        icon="👥"
    ),

    st.Page(
        "pages/4_Geographical_Analytics.py",
        title="Geographical Analytics",
        icon="🌍"
    ),

    st.Page(
        "pages/5_Methodology.py",
        title="Methodology",
        icon="📚"
    )
]

# Execute only the selected page
pg = st.navigation(pages)
pg.run()