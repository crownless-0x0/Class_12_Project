import linear_regression as lr
import math
import mysql.connector

conn = lr.get_connected()
cursor = conn.cursor()

def import_close_values():
    cursor.execute("""SELECT `Close` FROM stocks ORDER BY `Date`""")
    prices = [row[0] for row in cursor.fetchall()]
    return prices

def calculate_daily_return():
    prices = import_close_values()
    d_return = []
    for i in range(1, len(prices)):
        d_return.append((prices[i] - prices[i-1]) / prices[i-1])
    return d_return

def mean_return():
    d_return = calculate_daily_return()
    return sum(d_return) / len(d_return)

def volatility():
    daily_return = calculate_daily_return()
    meu = mean_return()   # a single scalar mean, not a list
    n = len(daily_return)

    sum_return_diff_meu = 0
    for r in daily_return:
        sum_return_diff_meu += (r - meu) ** 2

    var = sum_return_diff_meu / (n - 1)   # sample variance
    return math.sqrt(var)                  # volatility = standard deviation