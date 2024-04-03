import binascii
import logging
import mysql.connector
from Crypto.Cipher import AES
import struct
from flask import session

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SmartWalletReceiver:
    def __init__(self, wallet_id):
        self.wallet_id = int(wallet_id)
        self.k_wallet = self.get_security_key(wallet_id)

    def receive_funds(self, token):
        # Get the wallet_id of the logged-in user
        receiver_id = get_logged_in_user_wallet_id()
        if not receiver_id:
            return "Error: Receiver ID not found."
        
        if self.verify_token_in_transactions(token, receiver_id):
            self.process_transaction(token)
            self.delete_transaction(token)
            return "Transaction processed and record deleted successfully"
        else:
            return "Token verification failed. Token not found in transactions."

    def verify_token_in_transactions(self, token, receiver_id):
        try:
            db_connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Passwd",
                database="WalletDB"
            )
            cursor = db_connection.cursor()
            cursor.execute("SELECT * FROM transactions WHERE receiver_id = %s AND token = %s", (receiver_id, token))
            transaction = cursor.fetchone()
            return bool(transaction)
        except mysql.connector.Error as e:
            logging.error(f"Database error: {e}")
            return False
        finally:
            cursor.close()
            db_connection.close()

    def process_transaction(self, token):
        try:
            db_connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Passwd",
                database="WalletDB"
            )
            cursor = db_connection.cursor()
            
            cursor.execute("SELECT sender_id, wallet_b_amount FROM transactions WHERE token = %s", (token,))
            sender_id, wallet_b_amount = cursor.fetchone()
            
            cursor.execute("UPDATE wallets SET counter = counter + 1, wallet_b_amount = wallet_b_amount - %s, wallet_amount = wallet_amount - %s WHERE wallet_id = %s", (wallet_b_amount, wallet_b_amount, sender_id))
            
            cursor.execute("UPDATE wallets SET counter = counter + 1, wallet_b_amount = wallet_b_amount + %s, wallet_amount = wallet_amount + %s WHERE wallet_id = %s", (wallet_b_amount, wallet_b_amount, self.wallet_id))
            
            db_connection.commit()
            logging.info("Transaction processed successfully.")
        except mysql.connector.Error as e:
            logging.error(f"Failed to process transaction: {e}")
        finally:
            cursor.close()
            db_connection.close()

    def delete_transaction(self, token):
        try:
            db_connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Passwd",
                database="WalletDB"
            )
            cursor = db_connection.cursor()
            
            cursor.execute("DELETE FROM transactions WHERE receiver_id = %s AND token = %s", (self.wallet_id, token))
            
            db_connection.commit()
            logging.info("Transaction record deleted successfully.")
        except mysql.connector.Error as e:
            logging.error(f"Failed to delete transaction record: {e}")
        finally:
            cursor.close()
            db_connection.close()

    def get_security_key(self, wallet_id):
        try:
            db_connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Passwd",
                database="WalletDB"
            )
            cursor = db_connection.cursor()
            
            cursor.execute("SELECT security_key FROM wallets WHERE wallet_id = %s", (wallet_id,))
            security_key = cursor.fetchone()
            
            if security_key:
                return binascii.unhexlify(security_key[0])
            else:
                logging.error("No security key found for the given wallet ID.")
                return None
        except mysql.connector.Error as e:
            logging.error(f"Database error: {e}")
            return None
        finally:
            cursor.close()
            db_connection.close()

def get_logged_in_user_wallet_id():
    return session.get('user_id')
