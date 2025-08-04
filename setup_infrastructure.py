# setup_infrastructure.py
import os

import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER, DATA_DIR


def create_environment():
    """Sets up the necessary directories and database schema."""
    print("--- Setting up project environment ---")

    print("1. Checking for 'data' directory...")
    os.makedirs(DATA_DIR, exist_ok=True)
    print("   'data' directory is ready.")

    print("\n2. Checking for database...")
    conn = None
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            port=DB_PORT,
            dbname='postgres'
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()

        cur.execute(sql.SQL("SELECT 1 FROM pg_database WHERE datname = %s"), (DB_NAME,))
        if not cur.fetchone():
            print(f"   Database '{DB_NAME}' not found. Creating it now...")
            cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(DB_NAME)))
            print(f"   Database '{DB_NAME}' created.")
        else:
            print(f"   Database '{DB_NAME}' already exists.")
        cur.close()
    except Exception as e:
        print(f"   ERROR: Could not check or create database. {e}")
    finally:
        if conn:
            conn.close()

    print("\n3. Checking for 'sales' table...")
    conn = None
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            port=DB_PORT
        )
        cur = conn.cursor()

        create_table_query = """
        CREATE TABLE IF NOT EXISTS sales (
            order_id INT PRIMARY KEY,
            customer_id VARCHAR(50),
            product_name VARCHAR(255),
            quantity INT,
            price DECIMAL(10, 2),
            order_date DATE,
            total_sale DECIMAL(10, 2)
        );
        """
        cur.execute(create_table_query)
        conn.commit()
        print("   Table 'sales' is ready.")
        cur.close()
    except Exception as e:
        print(f"   ERROR: Could not create 'sales' table. {e}")
    finally:
        if conn:
            conn.close()

    print("\n--- Environment setup complete! ---")


if __name__ == "__main__":
    create_environment()
