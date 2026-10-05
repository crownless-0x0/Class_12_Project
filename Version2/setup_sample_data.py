import csv
import mysql.connector as ms

x = ms.connect(host='localhost', user='root', passwd='root', database='PRISM')
cur = x.cursor()

for stock in ['aapl', 'tcs', 'reliance']:
    cur.execute('SHOW TABLES LIKE %s', (stock,))
    if cur.fetchone():
        cur.execute(f'DROP TABLE `{stock}`')
    cur.execute(f'''
        CREATE TABLE `{stock}` (
            id INT PRIMARY KEY AUTO_INCREMENT,
            Date DATE,
            Open FLOAT,
            High FLOAT,
            Low FLOAT,
            Close FLOAT,
            Volume FLOAT
        )
    ''')
    with open(f'stock_data/{stock}.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            cur.execute(
                f'INSERT INTO `{stock}` (Date, Open, High, Low, Close, Volume) VALUES (%s,%s,%s,%s,%s,%s)',
                (row[0], float(row[1]), float(row[2]), float(row[3]), float(row[4]), float(row[5]))
            )
    print(stock, 'imported')

for uid in ['demo', 'recv']:
    cur.execute('DELETE FROM transactions WHERE user_id=%s OR recipient_id=%s', (uid, uid))
    cur.execute('DELETE FROM accounts WHERE user_id=%s', (uid,))
    cur.execute('DELETE FROM user_port WHERE user_id=%s', (uid,))
    cur.execute('DELETE FROM user_details WHERE user_id=%s', (uid,))
    cur.execute('DELETE FROM login_creds WHERE user_id=%s', (uid,))

cur.execute("INSERT INTO login_creds VALUES ('demo','demo123','jane','inception','engineer')")
cur.execute("INSERT INTO user_details VALUES ('demo','Demo User',1234567890,'123456789012345')")
cur.execute("INSERT INTO user_port VALUES ('demo',50000,'aapl, tcs',0,'0')")
cur.execute("INSERT INTO accounts VALUES ('123456789012345','demo',100000)")

cur.execute("INSERT INTO login_creds VALUES ('recv','recv123','mary','avatar','doctor')")
cur.execute("INSERT INTO user_details VALUES ('recv','Recv User',1987654321,'987654321098765')")
cur.execute("INSERT INTO accounts VALUES ('987654321098765','recv',25000)")

x.commit()
print('demo users ready')
print('Login with user_id=demo password=demo123')
