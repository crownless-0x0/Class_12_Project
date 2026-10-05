import time
import csv_to_sql_importer
import mysql.connector as ms
import fund_transfer as fd
import monte_carlo as mc
import output_handling as oh
import tabulate as tb
import csv

x = ms.connect(host='localhost', user='root', passwd='root', database='PRISM')
cur = x.cursor()


def home_page(query_result):
  while True:
    print('⌈HOME PAGE⌋'.center(100, '-'))
    print()
    print('1 ======> Portfolio'.center(95))
    print('2 ======> Stock Prediction'.center(101))
    print('3 ======> Fund Transfer'.center(99))
    print('4 ======> Import Stock csv Data'.center(107))
    print('5 ======> Export Portfolio'.center(101))
    print('6 ======> Exit'.center(89))

    try:
      query = int(input('Enter your choice: '))
    except ValueError:
      print('Please enter a valid number.')
      continue

    if query == 1:
      portfolio(query_result)
    elif query == 2:
      stock_prediction(query_result)
    elif query == 3:
      fd.send_funds(query_result)
    elif query == 4:
      csv_to_sql_importer.input_csv()
    elif query == 5:
      export_portfolio(query_result)
    elif query == 6:
      print('Exiting to login...')
      break
    else:
      print('Invalid choice. Try again.')


def stock_prediction(query_result):
  while True:
    print('=' * 80)
    cur.execute('SHOW TABLES')
    tables = cur.fetchall()
    reserved = ['accounts', 'login_creds', 'transactions', 'user_details', 'user_port']
    stocks = []
    for t in tables:
      if t[0].lower() not in reserved:
        stocks.append(t[0])
    if len(stocks) > 0:
      print('Available stocks: ' + ', '.join(stocks))
    else:
      print('No stock data imported yet. Use option 4 on the home page first.')

    stock = input("Enter the stock name (or type 'back' to return to menu): ").lower()
    if stock == 'back':
      break

    print('Select which model you want to use for the prediction'.center(10))
    print('=' * 80)
    print('1 ===> Simple Monte Carlo'.center(90))
    print('2 ===> GBM Monte Carlo'.center(86))
    opt = input('Enter your choice: ')

    if opt == '1':
      out = mc.monte_carlo_simple(stock)
    elif opt == '2':
      out = mc.monte_carlo_log(stock)
    else:
      print('Invalid choice')
      continue

    if out is None:
      cont = input('Do you want to try another stock?: y/n    ').lower()
      if cont != 'y':
        break
      continue

    oh.output(out, stock)

    cont = input('Do you want to try another stock?: y/n    ').lower()
    if cont != 'y':
      break


def portfolio(query_result):
  user_id = query_result[0]
  cur.execute('SELECT * FROM user_port WHERE user_id = %s', (user_id,))
  result = cur.fetchone()

  if result is None:
    print("Seems like you haven't initialised your portfolio. Lets add some details")
    print()
    print('=' * 80)
    total = int(input('Whats the total amount you have spent? : '))
    print('Lets insert the stocks you have owned')
    stock = ''

    while True:
      stock_name = input('Enter the stock name: ')
      stock = stock + stock_name + ', '
      cont = input('Continue? y/n: ').lower()
      if cont == 'n':
        print('Exiting')
        cur.execute('INSERT INTO user_port VALUES (%s, %s, %s, 0, %s)', (user_id, total, stock.rstrip(', '), '0'))
        x.commit()
        print('Portfolio created successfully!')
        break
      elif cont == 'y':
        continue
  else:
    oh.portflio_out(result)


def export_portfolio(query_result):
  user_id = query_result[0]
  cur.execute('SELECT * FROM user_port WHERE user_id = %s', (user_id,))
  user_port = cur.fetchone()
  if user_port is None:
    print('No portfolio found. Create one from the Portfolio menu first.')
    return
  print('='*80)
  print('Export your portfolio'.center(59))
  print('='*80)
  while True:
    type = input('Which format do you want? .txt or .csv (1/2): ')
    if type not in ['1','2']:
      print('Enter a valid option: ')
      continue
    elif type == '1':
      print('Exporting your details as a .txt file', end = '')
      for i in range(8):
        print('.', end = '')
        time.sleep(0.2)
      print()
      with open(f'{user_id}_portfolio.txt', 'w') as f:
        f.write('PRISM Portfolio\n')
        data = [[query_result[0], user_port[1], user_port[2], user_port[3], user_port[4]]]
        headers = ['UserID','Total Amount Spent','Stocks Owned','Last Trade','Profit/Loss']
        f.write(tb.tabulate(data, headers=headers, tablefmt='grid'))
      print(f'Saved as {user_id}_portfolio.txt')
      break
    elif type == '2':
      print('Exporting your portfolio as a .csv file', end = '')
      for i in range(8):
        print('.', end = '')
        time.sleep(0.2)
      print()
      with open(f'{user_id}_portfolio.csv', 'w', newline='') as f:
        writer =  csv.writer(f)
        writer.writerow(['Name','Total Amount Spent','Stocks owned','Last Trade','Profit/Loss'])
        writer.writerow([query_result[0], user_port[1], user_port[2], user_port[3], user_port[4]])
      print(f'Saved as {user_id}_portfolio.csv')
      break
