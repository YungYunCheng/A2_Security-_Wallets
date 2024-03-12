from Crypto.Cipher import AES
import binascii
import struct
import mysql.connector

class SmartWalletSender:
    def __init__(self, wallet_id):
        self.wallet_id = wallet_id
        self.k_wallet = self.get_security_key(wallet_id)
        self.counter = 0

    def send_funds(self, receiver_id, amount):
        self.counter += 1
        data = struct.pack('>IIII', self.wallet_id, receiver_id, amount, self.counter)
        token = self.encrypt_data(data, self.k_wallet)
        self.save_transaction(self.wallet_id, receiver_id, amount, token)  # Save transaction in database
        return token

    def get_security_key(self, wallet_id):
        try:
            # Connect to your database and fetch the security key for the given wallet_id
            # Replace the connection details and query with your actual implementation
            db_connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Passwd",
                database="WalletDB"
            )
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
            # Connect to your database and save the transaction details
            # Replace the connection details and query with your actual implementation
            db_connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Passwd",
                database="WalletDB"
            )
            db_cursor = db_connection.cursor()
            db_cursor.execute("INSERT INTO transactions (sender_id, receiver_id, wallet_b_amount, token) VALUES (%s, %s, %s, %s)", (sender_id, receiver_id, amount, token))
            db_connection.commit()
        except mysql.connector.Error as e:
            print(f"Error while saving transaction in database: {e}")
        finally:
            if db_connection.is_connected():
                db_cursor.close()
                db_connection.close()

