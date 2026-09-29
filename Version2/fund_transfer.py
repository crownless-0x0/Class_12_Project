import mysql.connector as ms
import login_page as lp

x = ms.connect(host = 'localhost', user = 'root', passwd = 'root', database = 'PRISM')
cur = x.cursor()

def send_funds(query_result):
    print('='*80)
    print('FUND TRANSFER'.center(67))
    print('='*80)
    print()
    tries = 5
    if tries == 0:
        print('You\'ve exhausted your tries. Sending you back to the login page.')
        lp.welcome()
        return

    while True:
        print(f'UserID: {query_result[0]}')
        passwd = input('Enter the password: ')
        if passwd != query_result[1]:
            print('Invalid password!')
            tries -= 1
            continue
        else:
            cur.execute('SELECT  ')