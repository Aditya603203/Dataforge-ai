import streamlit as st
import pandas as pd
from core.warehouse import get_all_tables, get_table_preview, query_warehouse, promote_to_gold

st.set_page_config(page_title="Warehouse | DataForge AI",
                   page_icon="🗄️", layout="wide")

st.title("🗄️ Data Warehouse")
st.caption("Browse your Bronze, Silver and Gold zones")

# Zone tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Overview",
    "🟤 Bronze",
    "⚪ Silver",
    "🟡 Gold"
])

with tab1:
    st.subheader("Warehouse Overview")
    tables = get_all_tables()

    if tables.empty:
        st.info("No data ingested yet — go to Ingest to upload your first dataset!")
    else:
        col1, col2, col3 = st.columns(3)
        bronze = tables[tables["zone"] == "bronze"]
        silver = tables[tables["zone"] == "silver"]
        gold = tables[tables["zone"] == "gold"]

        col1.metric("🟤 Bronze Tables", len(bronze))
        col2.metric("⚪ Silver Tables", len(silver))
        col3.metric("🟡 Gold Tables", len(gold))

        st.divider()
        st.subheader("All Tables")
        st.dataframe(tables[[
            "table_name", "zone", "source_file",
            "rows", "columns", "ingested_at"
        ]], use_container_width=True)

with tab2:
    st.subheader("🟤 Bronze Zone — Raw Data")
    tables = get_all_tables()
    bronze_tables = tables[
        tables["zone"] == "bronze"
    ]["table_name"].tolist() if not tables.empty else []

    if bronze_tables:
        selected = st.selectbox(
            "Select table:", 
            bronze_tables, 
            key="bronze_select"
        )
        if selected:
            df = get_table_preview("bronze", selected)
            if df is not None:
                col1, col2, col3 = st.columns(3)
                col1.metric("Rows", f"{len(df):,}")
                col2.metric("Columns", len(df.columns))
                col3.metric("Zone", "BRONZE")

                st.dataframe(df, use_container_width=True)

                st.divider()
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(
                        "🥇 Promote to Gold",
                        key="bronze_to_gold",
                        use_container_width=True
                    ):
                        msg = promote_to_gold(selected, df)
                        st.success(msg)
                with col2:
                    st.download_button(
                        "📥 Download CSV",
                        data=df.to_csv(index=False),
                        file_name=f"{selected}_bronze.csv",
                        mime="text/csv",
                        key="bronze_download",
                        use_container_width=True
                    )
    else:
        st.info("No bronze tables yet — go to Ingest to upload data")

with tab3:
    st.subheader("⚪ Silver Zone — Cleaned Data")
    tables = get_all_tables()
    silver_tables = tables[
        tables["zone"] == "silver"
    ]["table_name"].tolist() if not tables.empty else []

    if silver_tables:
        selected = st.selectbox(
            "Select table:",
            silver_tables,
            key="silver_select"
        )
        if selected:
            df = get_table_preview("silver", selected)
            if df is not None:
                col1, col2, col3 = st.columns(3)
                col1.metric("Rows", f"{len(df):,}")
                col2.metric("Columns", len(df.columns))
                col3.metric("Zone", "SILVER")

                st.dataframe(df, use_container_width=True)

                st.divider()
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(
                        "🥇 Promote to Gold",
                        key="silver_to_gold",
                        use_container_width=True
                    ):
                        msg = promote_to_gold(selected, df)
                        st.success(msg)
                with col2:
                    st.download_button(
                        "📥 Download CSV",
                        data=df.to_csv(index=False),
                        file_name=f"{selected}_silver.csv",
                        mime="text/csv",
                        key="silver_download",
                        use_container_width=True
                    )
    else:
        st.info("No silver tables yet — clean data from Bronze first")

with tab4:
    st.subheader("🟡 Gold Zone — Business Ready")
    tables = get_all_tables()
    gold_tables = tables[
        tables["zone"] == "gold"
    ]["table_name"].tolist() if not tables.empty else []

    if gold_tables:
        selected = st.selectbox(
            "Select table:",
            gold_tables,
            key="gold_select"
        )
        if selected:
            df = get_table_preview("gold", selected)
            if df is not None:
                col1, col2, col3 = st.columns(3)
                col1.metric("Rows", f"{len(df):,}")
                col2.metric("Columns", len(df.columns))
                col3.metric("Zone", "GOLD")

                st.dataframe(df, use_container_width=True)

                st.divider()
                st.download_button(
                    "📥 Download Gold Data",
                    data=df.to_csv(index=False),
                    file_name=f"{selected}_gold.csv",
                    mime="text/csv",
                    key="gold_download",
                    use_container_width=True
                )
    else:
        st.info(
            "No gold tables yet — promote data from "
            "Bronze or Silver zone"
        )