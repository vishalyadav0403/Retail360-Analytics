import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# Ensure data folder exists
os.makedirs("data", exist_ok=True)

# --- Generate dim_item data ---
num_items = 30
items = pd.DataFrame({
    "item_id": range(1, num_items + 1),
    "name": [f"Item_{i}" for i in range(1, num_items + 1)],
    "category": np.random.choice(["Beverages", "Snacks", "Dairy", "Produce"], num_items),
    "subcategory": np.random.choice(["TypeA", "TypeB", "TypeC"], num_items),
    "price": np.round(np.random.uniform(10, 500, num_items), 2),
    "unit": np.random.choice(["kg", "litre", "piece"], num_items)
})
items.to_csv("data/items.csv", index=False)

# --- Generate dim_outlet data ---
num_outlets = 10
outlets = pd.DataFrame({
    "outlet_id": range(1, num_outlets + 1),
    "name": [f"Outlet_{i}" for i in range(1, num_outlets + 1)],
    "tier": np.random.choice(["Tier 1", "Tier 2", "Tier 3"], num_outlets),
    "location_city": np.random.choice(["Delhi", "Mumbai", "Bangalore", "Chennai"], num_outlets),
    "location_state": np.random.choice(["MH", "KA", "TN", "DL"], num_outlets),
    "size": np.random.choice(["Small", "Medium", "Large"], num_outlets),
    "outlet_type": np.random.choice(["Supermarket", "Grocery", "Convenience"], num_outlets)
})
outlets.to_csv("data/outlets.csv", index=False)

# --- Generate dim_customer data ---
num_customers = 200
customers = pd.DataFrame({
    "customer_id": range(1, num_customers + 1),
    "gender": np.random.choice(["Male", "Female"], num_customers),
    "age_group": np.random.choice(["18-25", "26-35", "36-50", "50+"], num_customers),
    "loyalty_level": np.random.choice(["Bronze", "Silver", "Gold"], num_customers)
})
customers.to_csv("data/customers.csv", index=False)

# --- Generate fact_sales data ---
start_date = datetime(2023, 1, 1)
num_days = 400

sales_rows = []
sale_id = 1

for i in range(num_days):
    current_date = start_date + timedelta(days=i)
    date_key = int(current_date.strftime("%Y%m%d"))

    for _ in range(np.random.randint(20, 60)):  # number of sales per day
        item_id = np.random.randint(1, num_items + 1)
        outlet_id = np.random.randint(1, num_outlets + 1)
        customer_id = np.random.randint(1, num_customers + 1)
        quantity = np.random.randint(1, 10)
        price = items.loc[items["item_id"] == item_id, "price"].values[0]
        revenue = round(price * quantity, 2)
        avg_rating = round(np.random.uniform(1, 5), 2)
        discount_pct = round(np.random.uniform(0, 30), 2)

        sales_rows.append([
            sale_id, date_key, outlet_id, item_id, customer_id,
            quantity, revenue, avg_rating, discount_pct
        ])
        sale_id += 1

sales = pd.DataFrame(sales_rows, columns=[
    "sale_id", "date_key", "outlet_id", "item_id", "customer_id",
    "quantity", "revenue", "avg_rating", "discount_pct"
])
sales.to_csv("data/sales.csv", index=False)

print("CSV files generated successfully inside /data folder!")
