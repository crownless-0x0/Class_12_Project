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
            cur.execute('SELECT * FROM accounts WHERE user_id = %s',(query_result[0],))
            data = cur.fetchone()
            if data is None:
                print('You have\'nt affiliated your account with this PRISM account. Please add an account to continue')
                user_in = input('Do you want to link your account?(y/n) : ')
                if user_in.lower() == 'y' or '':
                    datain = []
                    while True:
                        acc_no = input('Enter your acount number: ')
                        if len(acc_no) != 15:
                            print('Enter a valid account number (p.s. its a 15 char string)')
                            continue
                        else:
                            datain.append(acc_no)
                            break
                    balance = int(input('Enter the balance in you account:  '))
                    datain.append(balance)
                cur.execute('INSERT INTO accounts VALUES(%s,%s,%s)',tuple(datain))
                x.commit()
                continue
            else:
                print(f'You\'re transferring from {data[0]}')
                print(f'Balance: {data[2]}')
                print()
                cont = input('Do  you want to continue: ').lower()
                if cont == 'y' or '':
                    datain = []
                    while True:
                        acc_no = input('Enter your recipient account number: ')
                        if len(acc_no) != 15:
                            print('Enter a valid account number (p.s. its a 15 char string)')
                            continue
                        else:
                            datain.append(acc_no)
                            break
                    