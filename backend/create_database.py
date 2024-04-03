import mysql.connector
from mysql.connector import Error

def create_database():
    try:
        # Connection to MySQL Server without specifying a database
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Passwd'
        )

        if connection.is_connected():
            cursor = connection.cursor()
            # Create a new database named WalletDB
            cursor.execute("CREATE DATABASE IF NOT EXISTS WalletDB")
            print("Database WalletDB created successfully")

    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

def create_table():
    try:
        # Connection to the WalletDB database
        connection = mysql.connector.connect(
            host='localhost',
            database='WalletDB',
            user='root',  # Replace with your actual username
            password='Passwd'  # Replace with your actual password
        )

        if connection.is_connected():
            cursor = connection.cursor()
            # Create the wallets table
            wallets_table_query = """
            CREATE TABLE wallets (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id VARCHAR(255) NOT NULL,
                wallet_id VARCHAR(255) NOT NULL,
                wallet_amount DECIMAL(10, 2) NOT NULL,
                wallet_B_amount DECIMAL(10, 2) NOT NULL,
                security_key VARCHAR(255) NOT NULL,
                counter INT NOT NULL
                );
            """
            cursor.execute(wallets_table_query)
            print("Table wallets created successfully")

            # Create the transactions table
            transactions_table_query = """
            CREATE TABLE IF NOT EXISTS transactions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                sender_id INT NOT NULL,
                receiver_id INT NOT NULL,
                wallet_b_amount DECIMAL(10, 2) NOT NULL,
                token VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
            cursor.execute(transactions_table_query)
            print("Table transactions created successfully")

            # Create the users table
            users_table_query = """
            CREATE TABLE IF NOT EXISTS users (
                    uuid INT AUTO_INCREMENT PRIMARY KEY,
                    user_id VARCHAR(255) NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    security_key VARCHAR(255) NOT NULL
                )
            """
            cursor.execute(users_table_query)
            print("Table users created successfully")


    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

# Creating the database
create_database()

# Creating the tables within the database
create_table()

