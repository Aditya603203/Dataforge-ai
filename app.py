import streamlit as st
from core.warehouse import init_warehouse

# Page config
st.set_page_config(
    page_title="DataForge AI",
    page_icon="🔥",
    layout="wide"
)

# Initialize warehouse on startup
init_warehouse()

# Main landing page
st.title("🔥 DataForge AI")
st.subheader("AI-Powered Data Engineering Platform")

st.markdown("""
Welcome to **DataForge AI** — your intelligent data 
engineering platform combining enterprise-grade data 
warehousing with AI-powered insights.
""")

# Feature cards
col1, col2, col3 = st.columns(3)

with col1:
    st.info("""
    ### 📥 Ingest
    Upload CSV, Excel, JSON files directly 
    into your Bronze data warehouse zone.
    """)
    st.info("""
    ### 🗄️ Warehouse
    Browse Bronze, Silver and Gold zones. 
    Preview any dataset instantly.
    """)
    st.info("""
    ### 📋 Catalog
    AI-generated data dictionary and 
    business context for every dataset.
    """)

with col2:
    st.success("""
    ### 🔍 Query
    Ask questions in plain English or 
    write SQL directly against your warehouse.
    """)
    st.success("""
    ### 🤖 AI Clean
    Automatically detect and fix data 
    quality issues with AI recommendations.
    """)
    st.success("""
    ### 📊 Reports
    AI-generated executive summaries and 
    data quality scorecards.
    """)

with col3:
    st.warning("""
    ### 🗺️ Lineage
    Visual data flow mapping across all 
    your warehouse zones.
    *(Coming soon)*
    """)
    st.warning("""
    ### ✅ Contracts
    Validate data against contracts and 
    detect breaches automatically.
    *(Coming soon)*
    """)
    st.warning("""
    ### ⚡ Pipelines
    AI-powered ETL pipeline builder 
    with natural language instructions.
    *(Coming soon)*
    """)

# Warehouse stats
st.divider()
st.subheader("📊 Warehouse Overview")

from core.warehouse import get_all_tables
tables = get_all_tables()

if tables.empty:
    st.info("No data ingested yet — go to **Ingest** to upload your first dataset!")
else:
    col1, col2, col3, col4 = st.columns(4)
    bronze = tables[tables["zone"] == "bronze"]
    silver = tables[tables["zone"] == "silver"]
    gold = tables[tables["zone"] == "gold"]

    col1.metric("Total Datasets", len(tables))
    col2.metric("Bronze Tables", len(bronze))
    col3.metric("Silver Tables", len(silver))
    col4.metric("Gold Tables", len(gold))

    st.dataframe(tables, use_container_width=True)