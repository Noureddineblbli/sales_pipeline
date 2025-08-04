# report.py
import os
from datetime import date

import pandas as pd
from sqlalchemy import create_engine

# Import our centralized config variables
from config import DATABASE_URL, DATA_DIR


def generate_daily_sales_report():
    """
    Connects to the DB, queries for daily sales summary, and saves it as CSV and HTML.
    """
    print("--- Starting Daily Sales Report Generation ---")

    try:
        # Create a database engine
        engine = create_engine(DATABASE_URL)

        # Define the SQL query to get a summary of today's sales
        # NOTE: We use CURRENT_DATE which is a feature of PostgreSQL
        query = """
        SELECT
            product_name,
            SUM(quantity) AS total_quantity_sold,
            SUM(total_sale) AS total_revenue
        FROM sales
        WHERE order_date = CURRENT_DATE
        GROUP BY product_name
        ORDER BY total_revenue DESC;
        """

        # Execute the query and load the result into a pandas DataFrame
        print("Querying the database for today's sales summary...")
        daily_summary_df = pd.read_sql(query, engine)

        if daily_summary_df.empty:
            print("No sales data found for today. Report not generated.")
            return

        print("Query successful. Generating reports...")

        # --- Generate Reports ---
        report_date_str = date.today().strftime('%Y_%m_%d')

        # Define file paths within the 'data' directory
        csv_report_path = os.path.join(DATA_DIR, f"daily_sales_summary_{report_date_str}.csv")
        html_report_path = os.path.join(DATA_DIR, f"daily_sales_summary_{report_date_str}.html")

        # Save the DataFrame to a CSV file
        daily_summary_df.to_csv(csv_report_path, index=False)
        print(f"CSV report saved to: {csv_report_path}")

        # Save the DataFrame to a simple HTML file
        daily_summary_df.to_html(html_report_path, index=False, justify='center')
        print(f"HTML report saved to: {html_report_path}")

    except Exception as e:
        print(f"An error occurred during report generation: {e}")

    print("\n--- Report Generation Finished ---")


if __name__ == "__main__":
    generate_daily_sales_report()
