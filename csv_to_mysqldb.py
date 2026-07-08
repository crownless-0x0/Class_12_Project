#Made by @sudo_null. Totally human made. Feel free to use it for your own database collection
#This module imports csv files to MySQL DB, shaving off one of the headache 
#For this particular database for this project the following structure is used [id, symbol, marketdate, open, high, low, close]

import mysql.connector
import csv

def get_connected():                            # This function is used to connect to your database
    return mysql.connector.connect(
        host="localhost",
        user='root',
        passwd='root',
        database='esanth_shivesh_project'       # Replace the database with your own database
    )

conn = get_connected()
cursor = conn.cursor()

# Creating the database
cursor.execute("""
CREATE TABLE IF NOT EXISTS stocks(
    id INT AUTO_INCREMENT PRIMARY KEY,
    symbol VARCHAR(10),
    marketdate date,
    open float,
    high float,
    low float,
    close float
)
""")

def input_csv():                                # Initializing the csv input file
    location = input('Enter the csv file location: ')
    with open(location, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cursor.execute(
                """
                INSERT INTO stocks(symbol, marketdate, open, high, low, close)
                VALUES(%s,%s,%s,%s,%s,%s)
                """,
                (
                    row['symbol'],
                    row['marketdate'],
                    row['open'],
                    row['high'],
                    row['low'],
                    row['close']
                )
            )
    conn.commit()
    print('Imported the csv data to the SQL DB')

if __name__ == '__main__':                  # Allows to run this program as a library in a seperate program without any headache
    input_csv()
    cursor.close()
    conn.close()










