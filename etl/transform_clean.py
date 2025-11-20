import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# Ensure output folder exists
os.makedirs("cleaned", exist_ok=True)

print("Starting cleaning and transformation...")

# -----------------------------
# 1. Load raw CSVs
# -----------------------------
items = pd.read_csv("./data/items.csv")
outlets = pd.read_csv("./data/outlets.csv")
customers = pd.read_csv("./data/customers.csv")
sales = pd.read_csv("./data/sales.csv")

# -----------------------------
# 2. Clean items
# -----------------------------
items["category"] = items["category"].str.title()
items["subcategory"] = items["subcategory"].str.title()
items["unit"] = items["unit"].str.lower()

# Remove negative or zero prices (if exist)
items = items[items["price"] > 0]

# -----------------------------
# 3. Clean outlets
# -----------------------------
outlets["tier"] = outlets["tier"].str.upper()
outlets["location_city"] = outlets["location_city"].str.title()
outlets["location_state"] = outlets["location_state"].str.upper()

# -----------------------------
# 4. Clean customers
# -----------------------------
customers["gender"] = customers["gender"].str.capitalize()
customers["loyalty_level"] = customers["loyalty_level"].str.upper()

# -----------------------------
# 5. Clean fact_sales
# -----------------------------
sales = sales[sales["quantity"] > 0]          # remove bad rows
sales = sales[sales["revenue"] > 0]           # remove invalid revenue
sales = sales[sales["avg_rating"] <= 5]       # ratings max is 5
sales["avg_rating"] = sales["avg_rating"].clip(1, 5)

# Remove rows with foreign key mismatch (in real systems this happens a lot)
sales = sales[sales["item_id"].isin(items["item_id"])]
sales = sales[sales["outlet_id"].isin(outlets["outlet_id"])]
sales = sales[sales["customer_id"].isin(customers["customer_id"])]

# -----------------------------
# 6. Build dim_date dynamically
# -----------------------------
min_date = pd.to_datetime(sales["date_key"].astype(str), format="%Y%m%d").min()
max_date = pd.to_datetime(sales["date_key"].astype(str), format="%Y%m%d").max()

date_range = pd.date_range(min_date, max_date)

dim_date = pd.DataFrame({
    "date": date_range
})
dim_date["date_key"] = dim_date["date"].dt.strftime("%Y%m%d").astype(int)
dim_date["year"] = dim_date["date"].dt.year
dim_date["quarter"] = dim_date["date"].dt.quarter
dim_date["month"] = dim_date["date"].dt.month
dim_date["day"] = dim_date["date"].dt.day
dim_date["weekday"] = dim_date["date"].dt.weekday
dim_date["is_weekend"] = dim_date["weekday"] >= 5

# -----------------------------
# 7. Save cleaned versions
# -----------------------------
items.to_csv("./cleaned/items_clean.csv", index=False)
outlets.to_csv("./cleaned/outlets_clean.csv", index=False)
customers.to_csv("./cleaned/customers_clean.csv", index=False)
sales.to_csv("./cleaned/sales_clean.csv", index=False)
dim_date.to_csv("./cleaned/dim_date_clean.csv", index=False)

print("Cleaning complete! Cleaned CSVs stored in /cleaned folder.")
