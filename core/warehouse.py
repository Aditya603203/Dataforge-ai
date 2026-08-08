import duckdb
import pandas as pd
import os
from datetime import datetime

DB_PATH = "warehouse/dataforge.db"

def get_connection():
    return duckdb.connect(DB_PATH)

def init_warehouse():
    """Initialize warehouse zones as schemas"""
    con = get_connection()
    con.execute("CREATE SCHEMA IF NOT EXISTS bronze")
    con.execute("CREATE SCHEMA IF NOT EXISTS silver")
    con.execute("CREATE SCHEMA IF NOT EXISTS gold")
    con.execute("CREATE SCHEMA IF NOT EXISTS archive")
    
    # Metadata table
    con.execute("""
        CREATE TABLE IF NOT EXISTS main.metadata (
            table_name VARCHAR,
            zone VARCHAR,
            source_file VARCHAR,
            rows INTEGER,
            columns INTEGER,
            ingested_at TIMESTAMP,
            description VARCHAR
        )
    """)
    con.close()
    print("✅ Warehouse initialized")

def ingest_to_bronze(df, table_name, source_file):
    """Load raw data into bronze zone"""
    con = get_connection()
    
    # Add metadata columns
    df["_ingested_at"] = datetime.now()
    df["_source_file"] = source_file
    df["_zone"] = "bronze"
    
    # Save to bronze
    con.execute(f"DROP TABLE IF EXISTS bronze.{table_name}")
    con.execute(
        f"CREATE TABLE bronze.{table_name} AS SELECT * FROM df"
    )
    
    # Log metadata
    con.execute("""
        INSERT INTO main.metadata VALUES (?, ?, ?, ?, ?, ?, ?)
    """, [
        table_name, "bronze", source_file,
        len(df), len(df.columns), datetime.now(), ""
    ])
    
    con.close()
    return f"✅ Loaded {len(df)} rows into bronze.{table_name}"

def promote_to_silver(table_name, df_cleaned):
    """Promote cleaned data to silver zone"""
    con = get_connection()
    df_cleaned["_zone"] = "silver"
    df_cleaned["_promoted_at"] = datetime.now()
    con.execute(f"DROP TABLE IF EXISTS silver.{table_name}")
    con.execute(
        f"CREATE TABLE silver.{table_name} AS SELECT * FROM df_cleaned"
    )
    con.execute("""
        INSERT INTO main.metadata VALUES (?, ?, ?, ?, ?, ?, ?)
    """, [
        table_name, "silver", "", len(df_cleaned),
        len(df_cleaned.columns), datetime.now(), "AI Cleaned"
    ])
    con.close()
    return f"✅ Promoted to silver.{table_name}"

def promote_to_gold(table_name, df_gold):
    """Promote business-ready data to gold zone"""
    con = get_connection()
    df_gold["_zone"] = "gold"
    df_gold["_promoted_at"] = datetime.now()
    con.execute(f"DROP TABLE IF EXISTS gold.{table_name}")
    con.execute(
        f"CREATE TABLE gold.{table_name} AS SELECT * FROM df_gold"
    )
    con.execute("""
        INSERT INTO main.metadata VALUES (?, ?, ?, ?, ?, ?, ?)
    """, [
        table_name, "gold", "", len(df_gold),
        len(df_gold.columns), datetime.now(), "Business Ready"
    ])
    con.close()
    return f"✅ Promoted to gold.{table_name}"

def get_all_tables():
    """Get all tables across all zones"""
    con = get_connection()
    try:
        result = con.execute(
            "SELECT * FROM main.metadata ORDER BY ingested_at DESC"
        ).df()
    except:
        result = pd.DataFrame()
    con.close()
    return result

def query_warehouse(sql):
    """Run any SQL query against warehouse"""
    con = get_connection()
    try:
        result = con.execute(sql).df()
        con.close()
        return result, None
    except Exception as e:
        con.close()
        return None, str(e)

def get_table_preview(zone, table_name, limit=100):
    """Preview any table from any zone"""
    con = get_connection()
    try:
        result = con.execute(
            f"SELECT * FROM {zone}.{table_name} LIMIT {limit}"
        ).df()
        con.close()
        return result
    except Exception as e:
        con.close()
        return None