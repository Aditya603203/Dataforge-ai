if st.button("🤖 Generate AI Catalog Entry",
            use_container_width=True):
    try:
        from core.ai_engine import ai_generate_catalog
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
    except Exception as e:
        st.error(f"❌ {str(e)}")