# etl.py
import os
import pandas as pd
from datetime import date
from config import DATA_DIR
from sqlalchemy import create_engine
from config import DATABASE_URL

def extract_from_csv(file_path):
    """
    Extracts data from a CSV file into a pandas DataFrame.
    """
    print(f"Reading data from {file_path}...")
    try:
        dataframe = pd.read_csv(file_path)
        return dataframe
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return None

def transform_data(df):
    """
    Cleans, validates, and transforms the data.
    """
    if df is None:
        return None

    print("Transforming data...")
    
    # 1. Data Type Conversion & Validation
    # Convert 'order_date' to a proper datetime object
    df['order_date'] = pd.to_datetime(df['order_date'])

    # Ensure numeric columns are the correct type
    df['price'] = df['price'].astype(float)
    df['quantity'] = df['quantity'].astype(int)
    
    # 2. Handle Missing Values
    # For this project, we'll assume missing values are not allowed and drop them.
    # .dropna() returns a new DataFrame, so we must assign it back.
    original_rows = len(df)
    df.dropna(inplace=True)
    if len(df) < original_rows:
        print(f"Dropped {original_rows - len(df)} rows with missing values.")

    # 3. Business Logic / Enrichment
    # Calculate the 'total_sale' for each order
    df['total_sale'] = df['quantity'] * df['price']
    
    # 4. Remove Duplicates
    # Ensure that each order_id is unique
    df.drop_duplicates(subset=['order_id'], keep='first', inplace=True)

    print("Data transformation complete.")
    return df

def load_to_db(df):
    """
    Loads the transformed DataFrame into the PostgreSQL database.
    """
    if df is None:
        return

    print("Loading data into the database...")
    try:
        # Create a SQLAlchemy engine to connect to the database.
        # The DATABASE_URL is imported from our central config.py file.
        engine = create_engine(DATABASE_URL)
        
        # Write the DataFrame to the 'sales' table.
        # - 'if_exists="append"': If the table exists, add the new data. Don't drop it.
        # - 'index=False': Do not write the DataFrame's index as a column in the DB.
        df.to_sql('sales', con=engine, if_exists='append', index=False)
        
        print("Data loaded successfully.")

    except Exception as e:
        print(f"Error loading data to the database: {e}")

def run_etl():
    """
    Main function to run the ETL process.
    """
    print("--- Starting Sales Data ETL ---")

    # --- EXTRACT ---
    today_str = date.today().strftime('%Y_%m_%d')
    file_name = f"sales_data_{today_str}.csv"
    file_path = os.path.join(DATA_DIR, file_name)
    raw_sales_data = extract_from_csv(file_path)

    # --- TRANSFORM ---
    transformed_sales_data = transform_data(raw_sales_data)
    if transformed_sales_data is None:
        print("ETL process stopped due to transformation error.")
        return

    # --- LOAD ---
    load_to_db(transformed_sales_data)

    print("\n--- ETL Process Finished ---")

if __name__ == "__main__":
    run_etl()