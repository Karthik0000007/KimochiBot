import pandas as pd

def load_data(file="customer_service_interactions.csv"):
    try:
        df = pd.read_csv(file)
        # Clean the data - convert satisfaction to numeric, handle missing values
        df['satisfaction'] = pd.to_numeric(df['satisfaction'], errors='coerce')
        return df.dropna(subset=['satisfaction'])
    except Exception as e:
        print(f"Error loading data: {e}")
        return pd.DataFrame()

def total_queries(df):
    return len(df) if not df.empty else 0

def most_common_topics(df):
    if not df.empty and 'topic' in df.columns:
        return df['topic'].value_counts().head(5).to_dict()
    return {}

def average_satisfaction(df):
    if not df.empty and 'satisfaction' in df.columns:
        return round(df['satisfaction'].mean(), 2)
    return 0