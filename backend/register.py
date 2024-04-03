import mysql.connector
from mysql.connector import Error
import hashlib
import os

def create_connection():
    """Create a database connection."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='WalletDB',
            user='root',
            password='Passwd'  # Make sure to use your actual password
        )
        return connection
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")

def register_user(user_id, password):
    """Registers a new user with a hashed password."""
    hashed_password = hashlib.sha256(str(password).encode('utf-8')).hexdigest()
    security_key = hashlib.sha256(str(os.urandom(24)).encode('utf-8')).hexdigest()
    try:
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO users (user_id, password, security_key) 
            VALUES (%s, %s, %s)
        """, (user_id, hashed_password, security_key))
        connection.commit()
        print("User registered successfully.")
        return "User registered successfully.", True
    except Error as e:
        print(f"Failed to register user: {e}")
        return f"Failed to register user: {e}", False
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    # If this script is run as a standalone program, prompt the user for their details
    user_id = input("Enter user ID: ")
    password = input("Enter password: ")
    register_user(user_id, password)
