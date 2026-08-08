# 🔥 DataForge AI
### AI-Powered Data Engineering Platform

A production-grade data engineering platform combining 
enterprise data warehousing with AI-powered insights — 
built to productize real-world experience from American Express.

## 🎯 Problem
Data engineering teams spend hours manually ingesting, 
cleaning, cataloging and querying data across multiple 
systems with no unified intelligence layer.

## 💡 Solution
DataForge AI provides a unified platform with:
- 4-zone data warehouse (Bronze/Silver/Gold/Archive)
- AI-powered data cleaning and quality analysis
- Natural language to SQL query engine
- Auto-generated data catalog and executive reports

## 🏗️ Architecture
Raw Data (CSV/Excel/JSON)
↓
Bronze Zone (Raw)
↓
Silver Zone (AI Cleaned)
↓
Gold Zone (Business Ready)
↓
Query / Catalog / Reports

## ✨ Features
- **📥 Ingest** — Upload CSV, Excel, JSON into warehouse
- **🗄️ Warehouse** — Browse Bronze, Silver, Gold zones
- **🔍 Query** — Natural language + SQL editor with charts
- **📋 Catalog** — AI-generated data dictionary
- **📊 Reports** — AI executive summaries + PDF export
- **✨ AI Clean** — Auto detect and fix data quality issues

## 🛠️ Tech Stack
- **Frontend:** Streamlit
- **Warehouse:** DuckDB (4-zone architecture)
- **AI/LLM:** Google Gemini 2.0 Flash
- **Data Processing:** Pandas, SQLAlchemy
- **Visualization:** Plotly
- **Framework:** LangChain

## 🚀 Live Demo
[Coming soon — Streamlit Cloud]

## 💼 Inspiration
Built to productize enterprise data engineering patterns 
from 3+ years at American Express — including:
- Data quality monitoring across 300+ feeds
- GenAI-powered root cause analysis
- Scalable data onboarding architecture
- API governance and lineage tracking

## 🏃 How to Run Locally
1. Clone the repo
```bash
   git clone https://github.com/Aditya603203/dataforge-ai.git
   cd dataforge-ai
```
2. Create virtual environment
```bash
   python -m venv venv
   venv\Scripts\activate
```
3. Install dependencies
```bash
   pip install -r requirements.txt
```
4. Add your Gemini API key to `.streamlit/secrets.toml`
```toml
   GOOGLE_API_KEY="your-key-here"
```
5. Run the app
```bash
   streamlit run app.py
```

## 📁 Project Structure
dataforge-ai/
├── app.py ← Main entry + homepage
├── pages/
│ ├── 1_ingest.py ← Data upload + quality check
│ ├── 2_catalog.py ← AI data catalog
│ ├── 3_warehouse.py ← Zone browser + promotion
│ ├── 4_query.py ← NL + SQL query engine
│ └── 5_reports.py ← AI executive reports
├── core/
│ ├── warehouse.py ← DuckDB operations
│ └── ai_engine.py ← Gemini AI functions
└── warehouse/ ← DuckDB database file

## 📊 Results
- Full Bronze → Silver → Gold pipeline working
- Sub-second SQL queries via DuckDB
- AI cleaning handles nulls, duplicates, type mismatches
- Natural language queries converted to DuckDB SQL