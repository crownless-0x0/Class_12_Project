import os
import mysql.connector

def get_connected():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='root',
        database='Grade_12_Project'
    )

conn = get_connected()
cursor = conn.cursor()

sid = input("Enter the sid: ")
cursor.execute("""SELECT img_dir FROM Grade_12_Project WHERE sid = %s""", (sid,))
img_dir = cursor.fetchone()

os.system(img_dir)

if __name__ == '__main__':                  # Allows to run this program as a library in a seperate program without any headache
    cursor.close()
    conn.close()