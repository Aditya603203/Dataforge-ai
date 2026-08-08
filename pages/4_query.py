import streamlit as st
import plotly.express as px
from core.warehouse import get_all_tables, query_warehouse

st.set_page_config(page_title="Query | DataForge AI",
                   page_icon="🔍", layout="wide")

st.title("🔍 Query Engine")
st.caption("Ask questions in plain English or write SQL")

tables = get_all_tables()

if tables.empty:
    st.info("No data in warehouse yet — go to Ingest first!")
else:
    # Schema info
    schema_info = tables[[
        "table_name", "zone", "rows", "columns"
    ]].to_string()

    tab1, tab2 = st.tabs(["🤖 Natural Language", "📝 SQL Editor"])

    with tab1:
        st.subheader("Ask in Plain English")
        st.caption("⚠️ Requires Gemini API quota")
        question = st.text_input(
            "Ask anything about your data:",
            placeholder="e.g. Show me all completed orders"
        )

        if st.button("🔍 Generate SQL", key="nl_search"):
            if question:
                try:
                    from core.ai_engine import nl_to_sql
                    with st.spinner("Converting to SQL..."):
                        sql = nl_to_sql(question, schema_info)
                        st.code(sql, language="sql")

                        result, error = query_warehouse(sql)
                        if error:
                            st.error(f"❌ {error}")
                        elif result is not None:
                            st.dataframe(
                                result, 
                                use_container_width=True
                            )
                            if len(result) > 1 and len(result.columns) >= 2:
                                try:
                                    fig = px.bar(
                                        result,
                                        x=result.columns[0],
                                        y=result.columns[1],
                                        title="Query Results"
                                    )
                                    st.plotly_chart(
                                        fig,
                                        use_container_width=True
                                    )
                                except:
                                    pass
                except Exception as e:
                    st.error(f"❌ {str(e)}")

    with tab2:
        st.subheader("📝 SQL Editor")
        st.caption(
            "Available zones: bronze.tablename, "
            "silver.tablename, gold.tablename"
        )

        # Show available tables
        st.write("**Available tables:**")
        for _, row in tables.iterrows():
            st.write(
                f"• `{row['zone']}.{row['table_name']}` "
                f"— {row['rows']} rows"
            )

        st.divider()

        sql_input = st.text_area(
            "Write your SQL:",
            height=150,
            placeholder="SELECT * FROM bronze.sales_data LIMIT 10"
        )

        if st.button("▶️ Run Query", key="run_sql"):
            if sql_input:
                result, error = query_warehouse(sql_input)
                if error:
                    st.error(f"❌ {error}")
                elif result is not None:
                    st.success(f"✅ {len(result)} rows returned")
                    st.dataframe(
                        result, 
                        use_container_width=True
                    )

                    # Chart if numeric
                    numeric_cols = result.select_dtypes(
                        include="number"
                    ).columns.tolist()
                    if len(numeric_cols) > 0 and len(result) > 1:
                        try:
                            fig = px.bar(
                                result,
                                x=result.columns[0],
                                y=numeric_cols[0],
                                title="Query Results"
                            )
                            st.plotly_chart(
                                fig,
                                use_container_width=True
                            )
                        except:
                            pass
            else:
                st.warning("Please enter a SQL query first")