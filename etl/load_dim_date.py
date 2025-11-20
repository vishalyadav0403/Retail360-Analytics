import mysql.connector
from datetime import datetime, timedelta

connection = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="vishalyadav33.",     # <-- use your working password
    database="retail360"
)

cursor = connection.cursor()

start_date = datetime(2023, 1, 1)
end_date = datetime(2024, 12, 31)

current = start_date

while current <= end_date:
    date_key = int(current.strftime("%Y%m%d"))
    year = current.year
    quarter = (current.month - 1) // 3 + 1
    month = current.month
    day = current.day
    weekday = current.weekday()
    is_weekend = weekday >= 5

    cursor.execute("""
        INSERT INTO dim_date
        (date_key, date, year, quarter, month, day, weekday, is_weekend)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (date_key, current.date(), year, quarter, month, day, weekday, is_weekend))

    current += timedelta(days=1)

connection.commit()
cursor.close()
connection.close()

print("dim_date populated successfully!")
