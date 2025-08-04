# generate_data.py
import os
import random
from datetime import date

import pandas as pd
from faker import Faker

from config import DATA_DIR

fake = Faker()


def create_fake_sales_data(num_records):
    """Generates a DataFrame with fake sales records."""
    data = []
    for _ in range(num_records):
        data.append({
            'order_id': fake.unique.random_number(digits=6),
            'customer_id': f'CUS_{fake.random_number(digits=4)}',
            'product_name': random.choice(['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'USB-C Hub']),
            'quantity': random.randint(1, 5),
            'price': round(random.uniform(20.0, 1500.0), 2),
            'order_date': date.today().strftime('%Y-%m-%d')
        })
    return pd.DataFrame(data)


if __name__ == "__main__":
    num_records = 100
    daily_data = create_fake_sales_data(num_records)

    filename = f"sales_data_{date.today().strftime('%Y_%m_%d')}.csv"
    filepath = os.path.join(DATA_DIR, filename)

    daily_data.to_csv(filepath, index=False)

    print(f"Successfully generated {num_records} records in '{filepath}'")
