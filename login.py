import mysql.connector as ms
import time
import main

x = ms.connect(host = 'localhost', user = 'root', passwd = 'root', database = 'PRISM')
cur = x.cursor()

def welcome():
    while True:
        print('='*80)
        print('Welcome To PRISM'.center(65))
        print('='*80)
        print('1 ==> Login')
        print('2 ==> Create Account')
        print('3 ==> Admin Login')
        print('4 ==> Reset password')
        print('5 ==> Exit')
        opt = input('\nEnter your preferred option: ')
        if opt.isdigit() and int(opt) in [1,2,3,4,5]:
            if opt == '1':
                login()
                break
            elif opt == '2':
                acc_create()
                break
            elif opt == '3':
                admin_login()
                break
            elif opt == '4':
                passwd_rec()
                break
            elif opt == '5':
                print('Exiting.....')
                time.sleep(2)
                break
        else:
            print('Enter a valid option')
            continue

def login():
    attempt = 0
    while True:
        if attempt > 3:
            ques = input('Try resetting the password? (y/n): ').lower()
            if ques == 'y':
                passwd_rec(result)
                continue
            else:
                attempt = 0
                continue
            
        print('\n\n')
        user_id = input('Enter the user ID: ')
        cur.execute('SELECT * FROM user_creds WHERE user_id = %s',(user_id,))
        result = cur.fetchone()
        if result is None:
            print('Sorry the user ID is invalid.')
            opt = input('Try creating an account? (y/n) : ').lower()
            if opt == 'y':
                acc_create()
                continue
            else:
                break
        else:
            passwd = input('Enter the password: ')
            if passwd == result[1]:
                print('Login successful. Redirecting to homepage')
                for i in range(8):
                    print('█', end = '')
                    time.sleep(0.8)
                main.homepage(result)
            else:
                attempt += 1
                continue
        return

def acc_create():
    print('='*80)
    print('You are creating an account'.center(80-len('You are creating an account')))
    print('='*80)
    user_id = input('Enter your preferred user ID: ')
    cur.execute('SELECT * FROM user_cred WHERE user_id = %s',(user_id,))
    result = cur.fetchone()
    if result is None:
        while True:
            email = input('Enter your email ID: ')
            e_check = email.partition('@')
            if e_check[1] == '@' and email[-1:-4] == 'moc.':
                pass
            else:
                print('Enter a valid email')
                continue
            break
        
