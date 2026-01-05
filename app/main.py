import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd
from utils.text_processing import clean_text
from services.llm_service import analyze_email
from config.env import AZURE_OPENAI_DEPLOYMENT

CATEGORY_WEIGHTS = {
    "Market Manipulation/Misconduct": 5,
    "Bribery": 4,
    "Secrecy": 3,
    "Change in Communication": 2,
    "Employee Ethics": 1,
}

def assign_priority(score):
    if score >= 3:
        return "High"
    elif score >= 1.5:
        return "Medium"
    return "Low"

st.set_page_config(page_title="AI Communication Surveillance", layout="wide")
st.markdown("""
<h2 style='text-align: center; color: #4F8BF9;'>Welcome to the AI Communication Surveillance App!</h2>
<p style='text-align: center;'>Easily upload your Excel files and analyze communications for compliance and risk.</p>
<hr>
""", unsafe_allow_html=True)
st.title("\U0001F4E7 AI-Driven Communication Surveillance")

uploaded_file = st.file_uploader(
    "Upload Excel file (max 50 rows)",
    type=["xlsx"]
)

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    required_cols = {"From", "To", "Subject", "Body"}
    if not required_cols.issubset(df.columns):
        st.error("Excel must contain: From, To, Subject, Body")
        st.stop()

    df = df.head(50)
    results = []

    with st.spinner("Analyzing emails using Azure OpenAI..."):
        for _, row in df.iterrows():
            subject = row["Subject"]
            body = row["Body"]
            processed_body = clean_text(body)
            try:
                llm_output = analyze_email(subject, processed_body)
                categories = []
                risky_lines = []
                category_score = 0.5
                confidence = 0.7
                for cat in CATEGORY_WEIGHTS.keys():
                    if cat.lower() in llm_output.lower():
                        categories.append(cat)
                if not categories:
                    categories.append("Employee Ethics")
                max_weight = max(CATEGORY_WEIGHTS[c] for c in categories)
                risk_score = max_weight * category_score
                priority = assign_priority(risk_score)
                results.append({
                    "Subject": subject,
                    "Category": ", ".join(categories),
                    "Risky Lines": llm_output[:200],
                    "Risk Score": round(risk_score, 2),
                    "Priority": priority,
                    "Confidence": round(confidence, 2)
                })
            except Exception as e:
                st.error(f"Error processing email: {e}")
    result_df = pd.DataFrame(results)
    # Sort by Risk Score descending so higher risk appears first
    result_df = result_df.sort_values(by="Risk Score", ascending=False)
    st.subheader("\U0001F4CA Compliance Analysis Results")
    st.dataframe(result_df, use_container_width=True)
    st.success("Analysis completed successfully \u2705")
