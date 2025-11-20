import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

# ----------------------------------------
# 1. Connect to MySQL
# ----------------------------------------
connection = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="vishalyadav33.",
    database="retail360"
)

print("Connected to MySQL")

# ----------------------------------------
# 2. Load full fact table into pandas
# ----------------------------------------
query = """
SELECT 
    fs.sale_id,
    d.date,
    d.year,
    d.month,
    d.day,
    d.weekday,
    o.name AS outlet,
    o.tier,
    i.category,
    i.subcategory,
    fs.quantity,
    fs.revenue,
    fs.discount_pct,
    fs.avg_rating
FROM fact_sales fs
JOIN dim_date d ON fs.date_key = d.date_key
JOIN dim_item i ON fs.item_id = i.item_id
JOIN dim_outlet o ON fs.outlet_id = o.outlet_id;
"""

df = pd.read_sql(query, connection)
print("Data Loaded for EDA")

print("\nBasic Info:")
print(df.info())

print("\nSummary Stats:")
print(df.describe())

# ----------------------------------------
# 3. Plot: Monthly Total Revenue
# ----------------------------------------
monthly_rev = df.groupby(["year", "month"])["revenue"].sum()

monthly_rev.plot(kind="line", figsize=(10,5), title="Monthly Revenue Trend")
plt.xlabel("Year-Month")
plt.ylabel("Revenue")
plt.tight_layout()
plt.show()

# ----------------------------------------
# 4. Plot: Top 10 Selling Categories
# ----------------------------------------
cat_sales = df.groupby("category")["quantity"].sum().sort_values(ascending=False).head(10)

cat_sales.plot(kind="bar", figsize=(10,5), title="Top 10 Selling Categories")
plt.ylabel("Total Quantity Sold")
plt.tight_layout()
plt.show()

# ----------------------------------------
# 5. Plot: Outlet Revenue Comparison
# ----------------------------------------
outlet_rev = df.groupby("outlet")["revenue"].sum().sort_values(ascending=False)

outlet_rev.plot(kind="bar", figsize=(10,5), title="Revenue by Outlet")
plt.ylabel("Revenue")
plt.tight_layout()
plt.show()

# ----------------------------------------
# 6. Rating Distribution
# ----------------------------------------
df["avg_rating"].plot(kind="hist", bins=20, figsize=(8,4), title="Rating Distribution")
plt.xlabel("Rating")
plt.tight_layout()
plt.show()

# ----------------------------------------
# 7. Export for Tableau
# ----------------------------------------
df.to_csv("tableau_data.csv", index=False)
print("tableau_data.csv exported for Tableau.")

connection.close()
