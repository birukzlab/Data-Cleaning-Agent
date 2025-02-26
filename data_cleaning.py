import pandas as pd
import numpy as np
import subprocess

# Load OpenAI API Key (Replace 'your-api-key' with your actual key)
import pandas as pd
import numpy as np
import subprocess

def run_ollama(prompt, model="llama2"):
    """
    Sends a prompt to Ollama's locally running AI model and returns the response.
    """
    result = subprocess.run(
        ["ollama", "run", model, prompt],
        capture_output=True,
        text=True
    )
    return result.stdout.strip()

def clean_data(file_path):
    """
    Reads a CSV/Excel file, cleans missing values, removes duplicates,
    and formats columns properly.
    """
    try:
        # Read CSV or Excel file
        df = pd.read_csv(file_path) if file_path.endswith(".csv") else pd.read_excel(file_path)

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

    except Exception as e:
        return f"Error processing file: {str(e)}"

def generate_insights(df):
    """
    Uses Llama 2 AI to analyze the cleaned dataset and provide insights.
    """
    prompt = f"""
    Here is a dataset with {df.shape[0]} rows and {df.shape[1]} columns.
    Provide insights such as:
    - Trends or patterns
    - Columns with unusual data
    - Suggestions for further analysis

    Data preview:
    {df.head(10).to_string()}
    """

    response = run_ollama(prompt, model="llama2")
    return response

# Example Usage
if __name__ == "__main__":
    file_path = "sample_data/sample_data.csv"  # Change this if using an Excel file

    # Clean Data
    cleaned_df = clean_data(file_path)
    print("✅ Cleaned Data:\n", cleaned_df.head())

    # AI-Generated Insights
    insights = generate_insights(cleaned_df)
    print("📊 AI-Generated Insights:\n", insights)