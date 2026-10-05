import random
import mysql.connector as ms

x = ms.connect(host='localhost', user='root', passwd='root', database='PRISM')
cur = x.cursor()


def exp_approx(val):
    n = 200
    return (1 + val / n) ** n


def get_closes(stock):
    stock = stock.lower().strip()
    if not stock.isalnum():
        print('Invalid stock name.')
        return None

    cur.execute('SHOW TABLES LIKE %s', (stock,))
    if cur.fetchone() is None:
        print(f'No data found for stock "{stock}". Import a CSV first.')
        return None

    cur.execute(f'SELECT Close FROM `{stock}` ORDER BY Date')
    rows = cur.fetchall()
    if rows is None or len(rows) < 2:
        print('Not enough closing price data for this stock.')
        return None

    closes = []
    for r in rows:
        closes.append(r[0])
    return closes


def daily_returns(closes):
    returns = []
    for i in range(1, len(closes)):
        returns.append((closes[i] - closes[i - 1]) / closes[i - 1])
    return returns


def mean_val(data):
    return sum(data) / len(data)


def std_val(data):
    m = mean_val(data)
    total = 0
    for i in data:
        total += (i - m) ** 2
    return (total / len(data)) ** 0.5


def monte_carlo_simple(stock):
    closes = get_closes(stock)
    if closes is None:
        return None

    last_close = closes[-1]
    returns = daily_returns(closes)
    predictions = []

    print('Running Simple Monte Carlo', end='')
    for i in range(8):
        print('.', end='')
    print()

    for i in range(10000):
        r = random.choice(returns)
        predictions.append(last_close * (1 + r))

    return [last_close, predictions]


def monte_carlo_log(stock):
    closes = get_closes(stock)
    if closes is None:
        return None

    last_close = closes[-1]
    returns = daily_returns(closes)
    mu = mean_val(returns)
    sigma = std_val(returns)
    predictions = []
    days = 30

    print('Running GBM Monte Carlo', end='')
    for i in range(8):
        print('.', end='')
    print()

    for i in range(10000):
        price = last_close
        for d in range(days):
            z = random.gauss(0, 1)
            drift = (mu - 0.5 * (sigma ** 2))
            shock = sigma * z
            price = price * exp_approx(drift + shock)
        predictions.append(price)

    return [last_close, predictions]
