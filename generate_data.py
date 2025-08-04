# generate_data.py

import pandas as pd
from faker import Faker
import random
from datetime import date

# Initialize the Faker library to generate fake data
fake = Faker()

def create_fake_sales_data(num_records):
    """Generates a DataFrame with fake sales records."""
    data = []
    # Create a set to ensure order_ids are unique
    order_ids = set()

    for _ in range(num_records):
        # Generate a unique order ID
        order_id = fake.unique.random_number(digits=6)
        order_ids.add(order_id)
        
        data.append({
            'order_id': order_id,
            'customer_id': f'CUS_{fake.random_number(digits=4)}',
            'product_name': random.choice(['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'USB-C Hub']),
            'quantity': random.randint(1, 5),
            'price': round(random.uniform(20.0, 1500.0), 2),
            'order_date': date.today().strftime('%Y-%m-%d') # Use today's date
        })
    
    # Use a pandas DataFrame for easy handling
    return pd.DataFrame(data)

# This block ensures the code runs only when the script is executed directly
if __name__ == "__main__":
    # Let's create 100 fake sales records for today
    num_records = 100
    daily_data = create_fake_sales_data(num_records)
    
    # Create a filename that includes today's date for organization
    filename = f"sales_data_{date.today().strftime('%Y_%m_%d')}.csv"
    
    # Save the DataFrame to a CSV file. index=False prevents pandas from writing row numbers.
    daily_data.to_csv(filename, index=False)
    
    print(f"Successfully generated {num_records} records in '{filename}'")