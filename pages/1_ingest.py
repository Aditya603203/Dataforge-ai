import streamlit as st
import pandas as pd
import json
from core.warehouse import ingest_to_bronze, promote_to_silver
from core.ai_engine import ai_clean_data

st.set_page_config(page_title="Ingest | DataForge AI",
                   page_icon="📥", layout="wide")

st.title("📥 Data Ingest")
st.caption("Upload files into your Bronze warehouse zone")

# Upload section
uploaded_file = st.file_uploader(
    "Upload your data file",
    type=["csv", "xlsx", "json"],
    help="Supported: CSV, Excel, JSON"
)

if uploaded_file:
    # Read file
    file_name = uploaded_file.name
    table_name = file_name.split(".")[0].lower().replace(" ", "_")

    st.subheader("📋 Data Preview")

    try:
        if file_name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        elif file_name.endswith(".xlsx"):
            df = pd.read_excel(uploaded_file)
        elif file_name.endswith(".json"):
            df = pd.DataFrame(json.load(uploaded_file))

        # Show preview
        st.dataframe(df.head(10), use_container_width=True)

        # Basic stats
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Rows", f"{len(df):,}")
        col2.metric("Columns", len(df.columns))
        col3.metric("Missing Values", df.isnull().sum().sum())
        col4.metric("Duplicates", df.duplicated().sum())

        st.divider()

        # Data Quality Check
        st.subheader("🔍 Data Quality Analysis")

        issues = []
        col1, col2 = st.columns(2)

        with col1:
            st.write("**Column Analysis:**")
            for col in df.columns:
                nulls = df[col].isnull().sum()
                dtype = df[col].dtype
                if nulls > 0:
                    pct = round(nulls/len(df)*100, 1)
                    st.warning(f"⚠️ {col}: {nulls} nulls ({pct}%)")
                    issues.append(
                        f"{col} has {nulls} missing values ({pct}%)"
                    )
                else:
                    st.success(f"✅ {col}: No nulls | Type: {dtype}")

        with col2:
            st.write("**Summary Statistics:**")
            st.dataframe(
                df.describe(),
                use_container_width=True
            )

        st.divider()

        # AI Recommendations
        if issues:
            st.subheader("🤖 AI Cleaning Recommendations")
            with st.spinner("Analyzing data quality issues..."):
                df_info = f"""
                Table: {table_name}
                Rows: {len(df)}
                Columns: {list(df.columns)}
                Data types: {df.dtypes.to_dict()}
                """
                recommendations = ai_clean_data(
                    df_info,
                    "\n".join(issues)
                )
                st.write(recommendations)

        st.divider()

        # Ingest Actions
        st.subheader("🚀 Ingest to Warehouse")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.info("**Bronze Zone**\nRaw data as-is")
            if st.button("📥 Load to Bronze",
                        use_container_width=True):
                with st.spinner("Loading to Bronze..."):
                    msg = ingest_to_bronze(
                        df.copy(), table_name, file_name
                    )
                    st.success(msg)
                    st.session_state["last_table"] = table_name
                    st.session_state["last_df"] = df

        with col2:
            st.success("**Silver Zone**\nAI-cleaned data")
            if st.button("✨ Clean & Load to Silver",
                        use_container_width=True):
                with st.spinner("AI cleaning data..."):
                    df_clean = df.copy()

                    # Auto-clean nulls
                    for col in df_clean.columns:
                        if df_clean[col].dtype == "object":
                            df_clean[col] = df_clean[col].fillna("Unknown")
                        elif df_clean[col].dtype in ["int64", "float64"]:
                            df_clean[col] = df_clean[col].fillna(
                                df_clean[col].median()
                            )
                        else:
                            df_clean[col] = df_clean[col].fillna("Unknown")

                    # Remove duplicates
                    df_clean = df_clean.drop_duplicates()

                    # Load to bronze first then silver
                    ingest_to_bronze(
                        df.copy(), table_name, file_name
                    )
                    msg = promote_to_silver(table_name, df_clean)
                    st.success(
                        f"✅ Cleaned {df.duplicated().sum()} duplicates"
                    )
                    st.success(
                        f"✅ Handled {df.isnull().sum().sum()} null values"
                    )
                    st.success(msg)

        with col3:
            st.warning("**Direct to Gold**\nBusiness-ready")
            if st.button("🥇 Load to Gold",
                        use_container_width=True):
                st.info(
                    "First clean data in Silver zone, "
                    "then promote to Gold from the Warehouse page."
                )

    except Exception as e:
        st.error(f"❌ Error reading file: {str(e)}")

else:
    st.info(
        "👆 Upload a CSV, Excel or JSON file to get started"
    )

    # Sample data suggestion
    st.subheader("💡 Don't have a file? Try these:")
    st.markdown("""
    - **Kaggle.com** → Search any dataset (sales, finance, HR)
    - **data.gov.in** → Indian government open datasets
    - **sebi.gov.in** → Financial regulatory data
    - Create a sample CSV with your own data
    """)