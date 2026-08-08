import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

def get_llm():
    return ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=st.secrets["GOOGLE_API_KEY"],
        temperature=0
    )

def ai_clean_data(df_info, issues):
    """Get AI recommendations for cleaning data"""
    llm = get_llm()
    prompt = PromptTemplate.from_template("""
    You are a data engineering expert.
    
    Dataset info:
    {df_info}
    
    Issues found:
    {issues}
    
    Provide specific cleaning recommendations in this format:
    1. Issue: [issue name]
       Fix: [exact fix to apply]
       Priority: [Critical/High/Medium/Low]
    
    Be specific and actionable.
    """)
    chain = prompt | llm | StrOutputParser()
    return chain.invoke({"df_info": df_info, "issues": issues})

def ai_generate_catalog(df_info, sample_data):
    """Auto-generate data catalog entry"""
    llm = get_llm()
    prompt = PromptTemplate.from_template("""
    You are a data catalog expert.
    
    Dataset info:
    {df_info}
    
    Sample data:
    {sample_data}
    
    Generate a data catalog entry with:
    1. Dataset description (2-3 sentences)
    2. Column descriptions (for each column)
    3. Suggested business use cases
    4. Data quality observations
    5. Suggested tags
    
    Be specific and business-focused.
    """)
    chain = prompt | llm | StrOutputParser()
    return chain.invoke({
        "df_info": df_info,
        "sample_data": sample_data
    })

def nl_to_sql(question, schema_info):
    """Convert natural language to SQL"""
    llm = get_llm()
    prompt = PromptTemplate.from_template("""
    You are a SQL expert working with DuckDB.
    
    Available tables and schemas:
    {schema_info}
    
    Convert this question to a DuckDB SQL query:
    {question}
    
    Rules:
    - Use exact table names with zone prefix 
      (e.g. bronze.tablename, silver.tablename)
    - Return ONLY the SQL query, nothing else
    - No markdown, no explanation, just SQL
    """)
    chain = prompt | llm | StrOutputParser()
    return chain.invoke({
        "question": question,
        "schema_info": schema_info
    })

def ai_generate_report(metadata, quality_stats):
    """Generate executive data report"""
    llm = get_llm()
    prompt = PromptTemplate.from_template("""
    You are a Chief Data Officer writing an executive report.
    
    Warehouse metadata:
    {metadata}
    
    Quality statistics:
    {quality_stats}
    
    Write a concise executive summary covering:
    1. Overall data warehouse health
    2. Key metrics and highlights
    3. Data quality assessment
    4. Top 3 recommendations
    5. Risk areas to watch
    
    Keep it professional and business-focused.
    """)
    chain = prompt | llm | StrOutputParser()
    return chain.invoke({
        "metadata": metadata,
        "quality_stats": quality_stats
    })