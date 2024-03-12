import mysql.connector
from mysql.connector import Error

def get_balance_data():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='WalletDB',
            user='root',
            password='Passwd'
        )

        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            cursor.execute('SELECT * FROM wallets')  # Replace YourTableName with the actual table name
            rows = cursor.fetchall()
            return rows

    except Error as e:
        print(f'Error while connecting to MySQL: {e}')

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == '__main__':
    balance_data = get_balance_data()
    for row in balance_data:
        print(row)
