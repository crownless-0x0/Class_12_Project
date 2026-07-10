# Made by @sudo_null. Totally human made. Feel free to use it for your own database collection
# This module imports csv files to MySQL DB, shaving off one of the headache
# Table structure: [id, marketdate, open, high, low, close, volume]
import mysql.connector
import csv

def get_connected():
    return mysql.connector.connect(
        host="localhost",
        user='root',
        passwd='root',
        database='grade_12_project'
    )

conn = get_connected()
cursor = conn.cursor()

# Creating the table
cursor.execute("""
CREATE TABLE IF NOT EXISTS stocks(
    id INT AUTO_INCREMENT PRIMARY KEY,
    `Date` DATE,
    Open FLOAT,
    High FLOAT,
    Low FLOAT,
    Close FLOAT,
    Volume FLOAT
)
""")

def input_csv():
    location = input('Enter the csv file location: ')

    inserted = 0
    failed = 0

    with open(location, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                cursor.execute(
                    """
                    INSERT INTO stocks(`Date`, Open, High, Low, Close, Volume)
                    VALUES(%s,%s,%s,%s,%s,%s)
                    """,
                    (
                        row['Date'],
                        row['Open'],
                        row['High'],
                        row['Low'],
                        row['Close'],
                        row['Volume']
                    )
                )
                inserted += 1
            except mysql.connector.Error as e:
                failed += 1
                print(f"Skipped a row due to error: {e}")

    conn.commit()
    print(f'Imported {inserted} rows to the SQL DB ({failed} skipped)')

if __name__ == '__main__':
    input_csv()
    cursor.close()
    conn.close()