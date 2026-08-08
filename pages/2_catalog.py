import streamlit as st
from core.warehouse import get_all_tables, get_table_preview
from core.ai_engine import ai_generate_catalog

st.set_page_config(page_title="Catalog | DataForge AI",
                   page_icon="📋", layout="wide")

st.title("📋 Data Catalog")
st.caption("AI-generated data dictionary and business context")

tables = get_all_tables()

if tables.empty:
    st.info("No data in warehouse yet — go to Ingest first!")
else:
    selected_table = st.selectbox(
        "Select a dataset:",
        tables["table_name"].tolist()
    )
    selected_zone = tables[
        tables["table_name"] == selected_table
    ]["zone"].values[0]

    if selected_table:
        df = get_table_preview(selected_zone, selected_table)

        if df is not None:
            col1, col2, col3 = st.columns(3)
            col1.metric("Rows", f"{len(df):,}")
            col2.metric("Columns", len(df.columns))
            col3.metric("Zone", selected_zone.upper())

            st.subheader("📊 Data Preview")
            st.dataframe(df.head(5), use_container_width=True)

            st.divider()

            if st.button("🤖 Generate AI Catalog Entry",
                        use_container_width=True):
                with st.spinner("AI analyzing dataset..."):
                    df_info = f"""
                    Table: {selected_table}
                    Zone: {selected_zone}
                    Rows: {len(df)}
                    Columns: {list(df.columns)}
                    Data types: {df.dtypes.to_dict()}
                    Null counts: {df.isnull().sum().to_dict()}
                    """
                    sample = df.head(3).to_string()
                    catalog = ai_generate_catalog(df_info, sample)

                    st.subheader("📖 AI-Generated Catalog Entry")
                    st.write(catalog)

                    st.download_button(
                        "📥 Download Catalog Entry",
                        data=catalog,
                        file_name=f"{selected_table}_catalog.txt",
                        mime="text/plain"
                    )