import linear_regression as lr
import math
import mysql.connector

conn = lr.get_connected()
cursor = conn.cursor()

cursor.execute("""SELECT close FROM stocks""")

prices = [row[0] for row in cursor.fetchall()]

print(prices)