import streamlit as st
from core.warehouse import get_all_tables

st.set_page_config(page_title="Reports | DataForge AI",
                   page_icon="📊", layout="wide")

st.title("📊 AI Reports")
st.caption("AI-generated executive summaries and data quality scorecards")

tables = get_all_tables()

if tables.empty:
    st.info("No data in warehouse yet — go to Ingest first!")
else:
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Datasets", len(tables))
    col2.metric("Total Rows", f"{tables['rows'].sum():,}")
    col3.metric("Bronze Tables", len(tables[tables["zone"]=="bronze"]))
    col4.metric("Gold Tables", len(tables[tables["zone"]=="gold"]))

    st.divider()

    # Show warehouse summary without AI
    st.subheader("📋 Warehouse Summary")
    st.dataframe(tables[[
        "table_name", "zone", "rows", 
        "columns", "ingested_at"
    ]], use_container_width=True)

    st.divider()

    # AI Report — only on button click
    st.subheader("🤖 AI Executive Report")
    st.caption("⚠️ Requires Gemini API quota")

    if st.button("🤖 Generate Executive Report",
                use_container_width=True):
        try:
            from core.ai_engine import ai_generate_report
            with st.spinner("AI generating report..."):
                metadata = tables.to_string()
                quality_stats = f"""
                Total datasets: {len(tables)}
                Total rows: {tables['rows'].sum()}
                Bronze tables: {len(tables[tables['zone']=='bronze'])}
                Silver tables: {len(tables[tables['zone']=='silver'])}
                Gold tables: {len(tables[tables['zone']=='gold'])}
                """
                report = ai_generate_report(
                    metadata, quality_stats
                )
                st.subheader("📋 Executive Report")
                st.write(report)

                st.download_button(
                    "📥 Download Report",
                    data=report,
                    file_name="dataforge_report.txt",
                    mime="text/plain"
                )
        except Exception as e:
            st.error(f"❌ {str(e)}")