import random
import mysql.connector
import time
import main

def get_connected():
    return mysql.connector.connect(
        host="localhost",
        user='root',
        passwd='root',
        database='esanth_shivesh_project'
    )

conn = get_connected()
cursor = conn.cursor()

def welcome():
    quotes = [
        "Exploring thousands of futures, one simulation at a time.",
        "One prediction is a guess. Ten thousand form a distribution.",
        "Randomness reveals possibility.",
        "Every simulation is another possible tomorrow.",
        "Probability is the language of uncertainty."
    ]

    text = '⌈Probabilistic Stock Price Prediction Model⌋'
    randseed = random.randrange(0, len(quotes))

    print(text.center(100,'-'))

    wel_quote = quotes[randseed]
    print()
    print(wel_quote.center(100))
    print()

    while True:
        print('1 ===> Login'.center(90))
        print('2 ===> Admin Login'.center(95))
        print('3 ===> Create Account'.center(100))
        print('4 ===> Exit'.center(90))

        try:
            query = int(input('Enter your choice: '))
            if query not in range(1,5):
                print('Enter a valid option: ')
        except Exception as e:
            print(e)
            continue

        if query == 1:
            login()
            break
        elif query == 2:
            admin_login()
            break
        elif query == 3:
            acc_creation()
            continue
        elif query == 4:
            print('Exiting the program')
            break

def login():
    a = 0
    while True:
        if a >= 2:
            ques = input('Try resetting the password? y/n (Default = n): ')
            if ques.lower() == 'y':
                passwd_recovery(query_result)
                a = 0
                continue
            elif ques.lower() in ('n',''):
                continue
            
        confirm = input('Do you want to go to the home page? (y/n, default n):  ')
        if confirm.lower() == 'y':
            welcome()
            break
        elif confirm.lower() in ('n',''):
            while True:
                user_id = input('Enter the user ID: ')
                if user_id.strip() == '' :
                    print('User ID cannot be blank')
                    continue
                else:
                    cursor.execute("SELECT * FROM login_creds WHERE user_id = %s", (user_id,))
                    query_result = cursor.fetchone()
                    if query_result is None:
                        print('User does not exist. Try creating an account?')
                        ques = input('Create a new Account? (y/n, default = n): ')
                        if ques.lower() == 'y':
                            acc_creation()
                            continue
                        elif ques.lower() in ('n',''):
                            continue 
                    break
            password = input('Enter the password: ')
            if query_result[1] != password:
                print('Invalid Password!')
                a += 1
                continue
                
            else:
                print('Login Successful. Redirecting to Main Page.')
                dots = ['■', '■', '■', '■', '■', '■', '■', '■', '■', '■']

            while True:
                for d in dots:
                    print(f"{d} ", end="")
                    time.sleep(0.1)
                print()
                break
            main.home_page(query_result)
            return
        else:
            print('Enter a valid option!')
            continue

def admin_login():
    while True:
        admin_id_pass = {'admin': 'admin@DB01', 'sudoadmin': '102476'}
        admin_id = input('Enter your admin ID: ')
        password = input('Enter the password: ')

        if admin_id in admin_id_pass:
            if admin_id_pass[admin_id] == password:
                print('Admin login successful. Redirecting to admin page')
                dots = ['■', '■', '■', '■', '■', '■', '■', '■', '■', '■']
                while True:
                    for d in dots:
                        print(f"{d} ", end="")
                        time.sleep(0.1)
                    print()
                    break
                # Insert admin's main.py definition here and a break here
                break
            else:
                print('The admin ID or the password is invalid')
                continue

def acc_creation():
    while True:
        print('='*80)
        print('You are creating a new account'.center(40))
        print('='*80)
        user_id = input('Enter your preferred user ID: ')
        cursor.execute('SELECT user_id FROM login_creds WHERE user_id = %s',(user_id,))
        result = cursor.fetchone()
        if result is not None:
            print('Sorry!, the user ID you entered is already taken')
            continue
        else:
            password = input('Enter the password: ')
            print('='*80)
        while True:
            print('Lets continue by getting some information about you')
            user_name = input('Enter your name: ')
            try:
                user_mobile = int(input('Enter your mobile number: '))
                if len(str(user_mobile)) != 10:
                    print('Enter a valid number!')
                    continue
                else:
                    while True:
                        try:
                            user_acc = int(input('Enter your account number: '))
                            if len(str(user_acc)) != 15:
                                print('Enter a valid account number!')
                                continue
                            else:
                                break
                        except ValueError:
                            print('This is not a bank account number!')
                            continue
                    print('='*80)
                    print('Fill in these security questions in case you lose the password')
                    sq1 = input('Whats your mother name?: ')
                    sq2 = input('Whats your favourite movie?: ')
                    sq3 = input('Whats your dream job?: ')
                    print('='*80)
                    cursor.execute("INSERT INTO login_creds(user_id, password, sques1, sques2, sques3) VALUES(%s, %s, %s, %s, %s)", (user_id, password, sq1, sq2, sq3))
                    conn.commit()
                    break
            except ValueError:
                print('Enter a valid number!')
                continue
                    
        cursor.execute("INSERT INTO user_details(user_id, user_name, user_mobile, acc_no) VALUES(%s, %s, %s, %s)", (user_id, user_name, user_mobile, user_acc))
        conn.commit()
        print('Account Created Successfully! Redirecting')
        dots = ['■', '■', '■', '■', '■', '■', '■', '■', '■', '■']

        while True:
            for d in dots:
                print(f"{d} ", end="")
                time.sleep(0.1)
            break
        print()
        welcome()
        break

def passwd_recovery(a):
    print('='*80)
    print('You are in the password recovery page'.center(80))
    print('='*80)
    print(f'You are recovering the password for the account {a[0]}')
    user_in = input('Do you wish to continue(y/n): ').lower()
    if user_in == 'y':
        result = a
    else:
        while True:
            user_id = input('Enter your user ID: ').lower()
            cursor.execute('select * from login_creds where user_id = %s',(user_id,))
            result = cursor.fetchone()
            if result is None:
                print('User does not exist')
                continue
            else:
                break
    while True:
        print('='*80)
        print('Lets start by asking some security questions')
        sq1 = input('Whats your mother name?: ').lower()
        sq2 = input('Whats your favourite movie?: ').lower()
        sq3 = input('Whats your dream job?: ').lower()
        if sq1 == result[2].lower() and sq2 == result[3].lower() and sq3 == result[4].lower():
            print('Security Questions passed! Enter the new password')
            print('='*80)
            newpwd = input('New Password: ')
            print('='*80)
            cursor.execute('UPDATE login_creds set password = %s where user_id = %s',(newpwd,result[0]))
            conn.commit()
            break
        else:
            print('='*80)
            print('Security check failed. Please try again')
            print('='*80)
            continue
welcome()
