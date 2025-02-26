import streamlit as st
import pandas as pd
import numpy as np
from google.colab import files

# Function to clean data
def clean_data(df):
    # Fill missing values
    for col in df.columns:
        if df[col].dtype == np.number:
            df[col].fillna(df[col].mean(), inplace=True)  # Fill numeric columns with mean
        else:
            df[col].fillna("Unknown", inplace=True)  # Fill text columns with "Unknown"

    # Remove duplicates
    df.drop_duplicates(inplace=True)

    # Convert date columns to proper format
    for col in df.columns:
        if "date" in col.lower():
            df[col] = pd.to_datetime(df[col], errors="coerce")

    return df

# Web App UI
st.title("📊 AI-Powered Data Cleaning & Insights")

# File upload
uploaded_file = st.file_uploader("Upload a CSV File", type=["csv"])

if uploaded_file:
    # Read uploaded file
    df = pd.read_csv(uploaded_file)
    st.subheader("🔍 Original Data Preview")
    st.write(df.head())

    # Clean Data
    cleaned_df = clean_data(df)
    st.subheader("✅ Cleaned Data Preview")
    st.write(cleaned_df.head())

    # Download Cleaned File
    cleaned_csv = cleaned_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Cleaned Data",
        data=cleaned_csv,
        file_name="cleaned_data.csv",
        mime="text/csv"
    )