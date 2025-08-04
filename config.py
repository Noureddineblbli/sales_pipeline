# config.py
import os
from dotenv import load_dotenv

# Load environment variables from the .env file (make sure .env is in the same directory)
load_dotenv()

# --- Database Configuration ---
# Retrieve database credentials from environment variables set in .env
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
DB_PORT = os.getenv('DB_PORT', '5432') # Default to 5432 if not explicitly set in .env

# Construct the database connection string for SQLAlchemy/psycopg2
# This string is used by Python libraries to connect to your PostgreSQL database
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# --- File Paths ---
# Define the root of our project (the directory where config.py resides)
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
# Define a dedicated directory for our data files (CSV, reports, etc.)
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')