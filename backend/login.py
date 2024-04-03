import mysql.connector
from mysql.connector import Error
import hashlib

def create_db_connection():
    """Create and return a database connection."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='WalletDB',
            user='root',
            password='Passwd'  # Make sure to replace with your actual database password
        )
        return connection
    except Error as error:
        print(f"Failed to connect to the database: {error}")
        return None

def login_user(user_id, password):
    """Check if the user's hashed password matches the one in the database."""
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    
    connection = create_db_connection()
    if connection is not None:
        try:
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM users WHERE user_id = %s AND password = %s"
            cursor.execute(query, (user_id, hashed_password,))
            result = cursor.fetchone()
            cursor.close()
            connection.close()
            return bool(result), ""  # True if a user exists with these credentials, False otherwise
        except Error as error:
            print(f"Failed to query the database: {error}")
            return False, "Database error."
    else:
        return False, "No database connection."
