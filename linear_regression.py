import mysql.connector
import math

def get_connected():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='root',
        database='grade_12_project'
    )

conn = get_connected()
cursor = conn.cursor()

# Removed the symbol input since our table stores the stock data directly
cursor.execute("""SELECT Close FROM stocks""")

close_values = [row[0] for row in cursor.fetchall()]

def close_indices(values):
    return list(range(1, len(values) + 1))

def compute_slope(x, y):
    n = len(x)
    x_mean = sum(x) / n
    y_mean = sum(y) / n

    numerator = 0
    denominator = 0
    for i in range(n):
        numerator += (x[i] - x_mean) * (y[i] - y_mean)
        denominator += (x[i] - x_mean) ** 2

    slope = numerator / denominator
    return slope, y_mean, x_mean

def compute_intercept(slope, y_mean, x_mean):
    return y_mean - slope * x_mean

# --- Run the model ---

y = close_values
x = close_indices(y)

m, y_mean, x_mean = compute_slope(x, y)
b = compute_intercept(m, y_mean, x_mean)

print(f"Slope: {m}")
print(f"Intercept: {b}")

next_index = len(x) + 1
predicted_close = m * next_index + b
print(f"Predicted next close price: {predicted_close}")

if __name__ == '__main__':              # Allows to run this program as a library in a seperate program without any headache
    cursor.close()
    conn.close()