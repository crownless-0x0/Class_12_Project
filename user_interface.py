import random
import mysql.connector

def get_connected():
    return mysql.connector.connect(
        host="localhost",
        user='root',
        passwd='root',
        database='grade_12_project'
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

    text = 'Probabilistic Stock Price Prediction Model'
    randseed = random.randrange(0, len(quotes))

    print(text.center(60,'-'))

    wel_quote = quotes[randseed]
    print(wel_quote.center(100))

    while True:
        print('1. Login')
        print('2. Admin Login')
        print('3. Create Account')
        print('4. Exit')

        try:
            query = int(input('Enter your choice: '))
            if query not in range(1,5):
                print('Enter a valid option: ')
        except Exception as e:
            print(e)
            continue

        if query == 1:
            login()
        elif query == 2:
            admin_login()
        elif query == 3:
            acc_creation()
        elif query == 4:
            print('Exiting the program')
            break

def login():
    while True:
        confirm = input('Do you want to go to the home page?: y/n')
        if confirm.lower() == 'y':
            return
        elif confirm.lower() == 'n':
            while True:
                user_id = input('Enter the user ID: ')
                password = input('Enter the password: ')
                cursor.execute("""SELECT user_name FROM user_details WHERE user_id = %s""", (user_id,))

                query_result = cursor.fetchone()

                if query_result is None:
                    print('User does not exist. Try creating an account?')
                    continue
                
                cursor.execute("""SELECT user_id FROM login_creds WHERE password = %s""", (password,))
                query_result = cursor.fetchone()

                if query_result == None or query_result[0] != user_id:
                    print('Invalid Password!')
                    continue
                else:
                    #Insert a main.py definition here
                    pass
                break

        else:
            print('Enter a valid option!')
            continue
        break

def admin_login():
    while True:
        admin_id_pass = {'admin': 'admin@DB01', 'sudoadmin': '102476'}
        admin_id = input('Enter your admin ID: ')
        password = input('Enter the password: ')

        if admin_id in admin_id_pass:
            if admin_id_pass[admin_id] == password:
                # Insert admin's main.py definition here and a break here
                pass
            else:
                print('The admin ID or the password is invalid')
                continue
        break

def acc_creation():
    while True:
        cursor.execute("""SELECT user_id FROM user_details""")
        users = cursor.fetchall()
        user_id = input('Enter your preferred user ID: ')

        existing_ids = [i[0] for i in users]

        if user_id in existing_ids or user_id.strip() == '':
            print('Sorry!, the user ID you entered is already taken')
            continue
        else:
            password = input('Enter the password: ')
            cursor.execute("""INSERT INTO login_creds(user_id,password) VALUES(%s,%s)""",(user_id, password))
            conn.commit()

        while True:
            print('Lets continue by getting some information about you')
            user_name = input('Enter your name: ')
            try:
                user_mobile = int(input('Enter your mobile number: '))
                if len(str(user_mobile)) != 10:
                    print('Enter a valid number!')
                    continue
            except ValueError:
                print('Enter a valid number!')
                continue
            a = 1
            cursor.execute("""INSERT INTO user_details(user_id, user_name, user_mobile) VALUES(%s, %s, %s)""", (user_id, user_name, str(user_mobile)))
            conn.commit()
            break
        break
            
# Testing
welcome()