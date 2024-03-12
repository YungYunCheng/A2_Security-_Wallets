import mysql.connector
from mysql.connector import Error
import struct
import binascii
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import hashlib
from flask import jsonify

# Function to get the security key from the database
def get_security_key(wallet_id):
    try:
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
            print(f"Security key not found for Wallet ID: {wallet_id}")
            return None
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None
    finally:
        if 'db_connection' in locals() and db_connection.is_connected():
            db_cursor.close()
            db_connection.close()

# AES-256 encryption and decryption functions
def aes_256_encrypt(data, key):
    key = binascii.unhexlify(key)
    cipher = Cipher(algorithms.AES(key), modes.CBC(b'\x00' * 16), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted = encryptor.update(data) + encryptor.finalize()
    return binascii.hexlify(encrypted).decode('ascii')

def aes_256_decrypt(data, key):
    key = binascii.unhexlify(key)
    ct = binascii.unhexlify(data)
    cipher = Cipher(algorithms.AES(key), modes.CBC(b'\x00' * 16), backend=default_backend())
    decryptor = cipher.decryptor()
    return decryptor.update(ct) + decryptor.finalize()

# Function to generate EDM and store data in the database
def generate_emd(student_id, amount):
    amount_int = int(amount)
    amount_hex = '{:032x}'.format(amount_int)
    secret_key = hashlib.sha256(str(student_id[-4:]).encode('ascii')).hexdigest()  # Last 4 digits of student ID
    
    try:
        db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Passwd",
            database="WalletDB"
        )
        db_cursor = db_connection.cursor()

        # Convert hexadecimal amount back to decimal
        amount_decimal = int(amount_hex, 16)

        sql_query = "INSERT INTO wallets (wallet_id, wallet_amount, wallet_B_amount, security_key, counter) VALUES (%s, %s, %s, %s, %s)"
        data_to_insert = (student_id, amount_decimal, 0, secret_key, 0)
        db_cursor.execute(sql_query, data_to_insert)
        db_connection.commit()

        return jsonify({"message": f"EDM generated for student {student_id} with amount {amount}. Data stored successfully in the database."})

    except Error as e:
        return jsonify({"error": f"Error occurred while generating EDM and storing data in the database: {e}"})

    finally:
        if 'db_connection' in locals() and db_connection.is_connected():
            db_cursor.close()
            db_connection.close()


