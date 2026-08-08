import streamlit as st
from core.warehouse import get_all_tables
from core.ai_engine import ai_generate_report

st.set_page_config(page_title="Reports | DataForge AI",
                   page_icon="📊", layout="wide")

st.title("📊 AI Reports")
st.caption("AI-generated executive summaries and data quality scorecards")

tables = get_all_tables()

if tables.empty:
    st.info("No data in warehouse yet — go to Ingest first!")
else:
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Datasets", len(tables))
    col2.metric("Total Rows", f"{tables['rows'].sum():,}")
    col3.metric("Bronze Tables", len(tables[tables["zone"]=="bronze"]))
    col4.metric("Gold Tables", len(tables[tables["zone"]=="gold"]))

    st.divider()

    if st.button("🤖 Generate Executive Report", 
                use_container_width=True):
        with st.spinner("AI generating report..."):
            metadata = tables.to_string()
            quality_stats = f"""
            Total datasets: {len(tables)}
            Total rows: {tables['rows'].sum()}
            Bronze tables: {len(tables[tables['zone']=='bronze'])}
            Silver tables: {len(tables[tables['zone']=='silver'])}
            Gold tables: {len(tables[tables['zone']=='gold'])}
            """
            report = ai_generate_report(metadata, quality_stats)

            st.subheader("📋 Executive Report")
            st.write(report)

            # Download button
            st.download_button(
                "📥 Download Report",
                data=report,
                file_name="dataforge_report.txt",
                mime="text/plain"
            )