import mysql.connector
import pandas as pd

# -----------------------------
# 1. Connect to MySQL
# -----------------------------
connection = mysql.connector.connect(
    host="127.0.0.1",
    user="root",               # change if using another user
    password="vishalyadav33.",   # your MySQL password
    database="retail360"
)

cursor = connection.cursor()

# -----------------------------
# 2. Load dimension tables
# -----------------------------

# dim_item
items = pd.read_csv("./data/items.csv")
for _, row in items.iterrows():
    cursor.execute("""
        INSERT INTO dim_item (item_id, name, category, subcategory, price, unit)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, tuple(row))
connection.commit()

# dim_outlet
outlets = pd.read_csv("./data/outlets.csv")
for _, row in outlets.iterrows():
    cursor.execute("""
        INSERT INTO dim_outlet (outlet_id, name, tier, location_city, location_state, size, outlet_type)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, tuple(row))
connection.commit()

# dim_customer
customers = pd.read_csv("./data/customers.csv")
for _, row in customers.iterrows():
    cursor.execute("""
        INSERT INTO dim_customer (customer_id, gender, age_group, loyalty_level)
        VALUES (%s, %s, %s, %s)
    """, tuple(row))
connection.commit()

# -----------------------------
# 3. Load fact_sales
# -----------------------------
sales = pd.read_csv("./data/sales.csv")
for _, row in sales.iterrows():
    cursor.execute("""
        INSERT INTO fact_sales
        (sale_id, date_key, outlet_id, item_id, customer_id, quantity, revenue, avg_rating, discount_pct)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, tuple(row))
connection.commit()

print("All CSV data loaded into MySQL successfully!")

cursor.close()
connection.close()
