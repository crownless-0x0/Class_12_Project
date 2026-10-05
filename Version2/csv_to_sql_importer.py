import csv
import mysql.connector as ms
import time

x = ms.connect(host='localhost', user='root', passwd='root', database='PRISM')
cur = x.cursor()


def input_csv():
    print('=' * 80)
    print('IMPORT STOCK CSV DATA'.center(70))
    print('=' * 80)
    print()
    print('CSV must have headers: Date,Open,High,Low,Close,Volume')
    print()

    while True:
        stock = input('Enter the stock name for this data (or type back): ').lower().strip()
        if stock == 'back':
            return
        if stock == '' or not stock.isalnum():
            print('Enter a valid stock name (letters/numbers only).')
            continue
        break

    while True:
        path = input('Enter the CSV file path: ').strip().strip('"')
        if path == '':
            print('Path cannot be blank.')
            continue
        try:
            f = open(path, 'r')
            f.close()
            break
        except FileNotFoundError:
            print('File not found. Try again.')
            continue

    cur.execute('SHOW TABLES LIKE %s', (stock,))
    exists = cur.fetchone()
    if exists is not None:
        overwrite = input(f'Table "{stock}" already exists. Overwrite? y/n: ').lower()
        if overwrite != 'y':
            print('Import cancelled.')
            return
        cur.execute(f'DROP TABLE `{stock}`')
        x.commit()

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
    x.commit()

    print('Importing data', end='')
    for i in range(8):
        print('.', end='')
        time.sleep(0.1)
    print()

    count = 0
    with open(path, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        header_lower = []
        for h in header:
            header_lower.append(h.strip().lower())

        try:
            date_i = header_lower.index('date')
            open_i = header_lower.index('open')
            high_i = header_lower.index('high')
            low_i = header_lower.index('low')
            close_i = header_lower.index('close')
            volume_i = header_lower.index('volume')
        except ValueError:
            print('CSV headers must include Date, Open, High, Low, Close, Volume')
            cur.execute(f'DROP TABLE `{stock}`')
            x.commit()
            return

        for row in reader:
            if len(row) == 0:
                continue
            try:
                cur.execute(
                    f'INSERT INTO `{stock}` (Date, Open, High, Low, Close, Volume) VALUES (%s, %s, %s, %s, %s, %s)',
                    (row[date_i], float(row[open_i]), float(row[high_i]), float(row[low_i]), float(row[close_i]), float(row[volume_i]))
                )
                count += 1
            except Exception as e:
                print(f'Skipping row due to error: {e}')
                continue

    x.commit()
    print(f'Imported {count} rows into table "{stock}".')
    print('=' * 80)
