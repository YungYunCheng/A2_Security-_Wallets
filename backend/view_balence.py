import mysql.connector
from mysql.connector import Error
from flask import session

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
            # Get the user_id of the logged-in user from the session
            user_id = session.get('user_id')
            if not user_id:
                print("User not logged in.")
                return None

            # Fetch balance data specific to the logged-in user
            cursor.execute("""
                SELECT w.* 
                FROM wallets w 
                JOIN users u ON w.user_id = u.user_id 
                WHERE u.user_id = %s
            """, (user_id,))
            
            rows = cursor.fetchall()
            return rows

    except Error as e:
        print(f'Error while connecting to MySQL: {e}')

    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == '__main__':
    balance_data = get_balance_data()
    if balance_data:
        for row in balance_data:
            print(row)
    else:
        print("No balance data retrieved.")
