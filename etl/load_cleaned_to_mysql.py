import mysql.connector
import pandas as pd

# -----------------------------
# 1. Connect to MySQL
# -----------------------------
connection = mysql.connector.connect(
    host="127.0.0.1",
    user="root",             
    password="vishalyadav33.",   # your MySQL password
    database="retail360"
)

cursor = connection.cursor()

print("Connected to MySQL. Starting load...")

# -----------------------------
# 2. TRUNCATE old data
# -----------------------------
cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
cursor.execute("TRUNCATE TABLE fact_sales;")
cursor.execute("TRUNCATE TABLE dim_date;")
cursor.execute("TRUNCATE TABLE dim_item;")
cursor.execute("TRUNCATE TABLE dim_outlet;")
cursor.execute("TRUNCATE TABLE dim_customer;")
cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")

connection.commit()
print("Old data truncated.")

# -----------------------------
# 3. Load DIMENSION TABLES
# -----------------------------

# dim_item
items = pd.read_csv("./cleaned/items_clean.csv")
for _, row in items.iterrows():
    cursor.execute("""
        INSERT INTO dim_item (item_id, name, category, subcategory, price, unit)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, tuple(row))
connection.commit()
print("dim_item loaded.")

# dim_outlet
outlets = pd.read_csv("./cleaned/outlets_clean.csv")
for _, row in outlets.iterrows():
    cursor.execute("""
        INSERT INTO dim_outlet (outlet_id, name, tier, location_city, location_state, size, outlet_type)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, tuple(row))
connection.commit()
print("dim_outlet loaded.")

# dim_customer
customers = pd.read_csv("./cleaned/customers_clean.csv")
for _, row in customers.iterrows():
    cursor.execute("""
        INSERT INTO dim_customer (customer_id, gender, age_group, loyalty_level)
        VALUES (%s, %s, %s, %s)
    """, tuple(row))
connection.commit()
print("dim_customer loaded.")

# -----------------------------
# FIXED dim_date LOADING
# -----------------------------
dim_date = pd.read_csv("./cleaned/dim_date_clean.csv")

# Fix data types
dim_date["date_key"] = dim_date["date_key"].astype(int)
dim_date["date"] = pd.to_datetime(dim_date["date"]).dt.strftime("%Y-%m-%d")

for _, row in dim_date.iterrows():
    cursor.execute("""
        INSERT INTO dim_date 
        (date_key, date, year, quarter, month, day, weekday, is_weekend)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        int(row["date_key"]),
        row["date"],
        int(row["year"]),
        int(row["quarter"]),
        int(row["month"]),
        int(row["day"]),
        int(row["weekday"]),
        int(row["is_weekend"])
    ))
connection.commit()
print("dim_date loaded.")

# -----------------------------
# 4. Load FACT TABLE
# -----------------------------
sales = pd.read_csv("./cleaned/sales_clean.csv")
for _, row in sales.iterrows():
    cursor.execute("""
        INSERT INTO fact_sales 
        (sale_id, date_key, outlet_id, item_id, customer_id, quantity, revenue, avg_rating, discount_pct)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, tuple(row))
connection.commit()

print("fact_sales loaded successfully!")

cursor.close()
connection.close()
print("Load complete! All CLEANED data inserted into MySQL.")
