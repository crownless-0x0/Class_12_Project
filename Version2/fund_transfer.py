import mysql.connector as ms
import login_page as lp
import random
import time

x = ms.connect(host = 'localhost', user = 'root', passwd = 'root', database = 'PRISM')
cur = x.cursor()

def send_funds(query_result):
    print('='*80)
    print('FUND TRANSFER'.center(67))
    print('='*80)
    print()
    tries = 5

    while True:
        if tries == 0:
            print('You\'ve exhausted your tries. Sending you back to the login page.')
            lp.welcome()
            return

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
                if user_in.lower() in ('y', ''):
                    datain = []
                    while True:
                        acc_no = input('Enter your acount number: ')
                        if len(acc_no) != 15 and len(acc_no) != 16:
                            print('Enter a valid account number (p.s. its a 15/16 char string)')
                            continue
                        else:
                            datain.append(acc_no)
                            break
                    datain.append(query_result[0])
                    balance = int(input('Enter the balance in you account:  '))
                    datain.append(balance)
                    cur.execute('INSERT INTO accounts VALUES(%s,%s,%s)',tuple(datain))
                    x.commit()
                    print('Account linked successfully!')
                    continue
                else:
                    print('Returning to home page.')
                    return
            else:
                print(f'You\'re transferring from {data[0]}')
                print(f'Balance: {data[2]}')
                print()
                cont = input('Do  you want to continue: ').lower()
                if cont in ('y', ''):
                    while True:
                        acc_no = input('Enter your recipient account number: ')
                        if len(acc_no) != 15 and len(acc_no) != 16:
                            print('Enter a valid account number (p.s. its a 15/16 char string)')
                            continue
                        else:
                            break
                    cur.execute('SELECT * FROM accounts WHERE account_id = %s', (acc_no,))
                    recipient = cur.fetchone()
                    if recipient is None:
                        print('Recipient account does not exist.')
                        return
                    if recipient[0] == data[0]:
                        print('You cannot transfer to your own account.')
                        return

                    while True:
                        try:
                            amount = int(input('Enter the amount to transfer: '))
                            if amount <= 0:
                                print('Amount must be greater than 0.')
                                continue
                            if amount > data[2]:
                                print('Insufficient balance.')
                                continue
                            break
                        except ValueError:
                            print('Enter a valid amount.')
                            continue

                    print('Processing transfer', end='')
                    for i in range(8):
                        print('.', end='')
                        time.sleep(0.15)
                    print()

                    new_bal = data[2] - amount
                    rec_bal = recipient[2] + amount
                    cur.execute('UPDATE accounts SET balance = %s WHERE account_id = %s', (new_bal, data[0]))
                    cur.execute('UPDATE accounts SET balance = %s WHERE account_id = %s', (rec_bal, recipient[0]))

                    txn_id = 'TXN' + str(random.randint(1000000000, 9999999999))
                    cur.execute(
                        'INSERT INTO transactions VALUES (%s, %s, %s, %s, %s, NOW(), %s)',
                        (txn_id, query_result[0], 'TRANSFER', amount, recipient[1], 'SUCCESS')
                    )
                    x.commit()
                    print(f'Transfer successful! Transaction ID: {txn_id}')
                    print(f'New Balance: {new_bal}')
                    print('='*80)
                    return
                else:
                    print('Transfer cancelled.')
                    return
