from Crypto.Cipher import AES
import binascii
import struct
import mysql.connector
from flask import Flask, session

app = Flask(__name__)

class SmartWalletSender:
    def __init__(self, sender_id, receiver_id, amount):
        self.sender_id = int(sender_id)
        self.k_wallet = self.get_security_key(sender_id)
        self.receiver_id = int(receiver_id)
        self.amount = int(amount)
        self.counter = 0

    def send_funds(self):
        if self.sender_id is None:
            raise ValueError("Sender ID cannot be None")
        
        self.counter += 1
        data = struct.pack('>IIII', self.sender_id, self.receiver_id, self.amount, self.counter)
        token = self.encrypt_data(data, self.k_wallet)
        self.save_transaction(self.sender_id, self.receiver_id, self.amount, token)  # Save transaction in database
        return token

    def get_security_key(self, wallet_id):
        try:
            db_connection = create_connection()
            db_cursor = db_connection.cursor()
            db_cursor.execute("SELECT security_key FROM wallets WHERE wallet_id = %s", (wallet_id,))
            security_key = db_cursor.fetchone()
            if security_key:
                return security_key[0]
            else:
                print("Security key not found for Wallet ID:", wallet_id)
                return None
        except mysql.connector.Error as e:
            print(f"Error while fetching security key from database: {e}")
            return None
        finally:
            if db_connection.is_connected():
                db_cursor.close()
                db_connection.close()

    def encrypt_data(self, data, key):
        cipher = AES.new(binascii.unhexlify(key), AES.MODE_ECB)
        return binascii.hexlify(cipher.encrypt(data)).decode()

    def save_transaction(self, sender_id, receiver_id, amount, token):
        try:
            db_connection = create_connection()
            db_cursor = db_connection.cursor()
            db_cursor.execute("INSERT INTO transactions (sender_id, receiver_id, wallet_b_amount, token) VALUES (%s, %s, %s, %s)", (sender_id, receiver_id, amount, token))
            db_connection.commit()
        except mysql.connector.Error as e:
            print(f"Error while saving transaction in database: {e}")
        finally:
            if db_connection.is_connected():
                db_cursor.close()
                db_connection.close()

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
    except mysql.connector.Error as e:
        print(f"Error while connecting to MySQL: {e}")


def get_logged_in_user_wallet_id():
    user_id = session.get('user_id')
    if not user_id:
        return None  # Or handle the case where the user is not logged in
    
    # Fetch the wallet ID associated with the user ID from the database
    wallet_id = None
    try:
        db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Passwd",
            database="WalletDB"
        )
        cursor = db_connection.cursor()
        
        # Execute the query to fetch the wallet ID
        cursor.execute("SELECT wallet_id FROM wallets WHERE user_id = %s", (user_id,))
        
        # Fetch the result
        result = cursor.fetchone()
        if result:
            wallet_id = result[0]  # Extract the wallet ID from the result
        
    except mysql.connector.Error as e:
        print(f"Error: {e}")
    finally:
        # Close the cursor and database connection
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'db_connection' in locals() and db_connection and db_connection.is_connected():
            db_connection.close()
    
    return wallet_id

if __name__ == "__main__":
    app.run(debug=True)
