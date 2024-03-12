import os
import mysql.connector
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import db_connection

class WalletSyncProtocol:
    def __init__(self):
        self.db_connection = db_connection

    def generate_token(self, wallet_A_id, wallet_B_id):
        key = os.urandom(32)  # Generate a random key for AES-256
        cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
        encryptor = cipher.encryptor()
        plaintext = f"{wallet_A_id}{wallet_B_id}0{self.counter}".encode('utf-8')
        ciphertext = encryptor.update(plaintext) + encryptor.finalize()
        return binascii.hexlify(ciphertext).decode()

    def add_sync_record(self, wallet_A_id, wallet_B_id):
        cursor = self.db_connection.cursor()
        query = "INSERT INTO synchronization_records (wallet_id_A, wallet_id_B, counter) VALUES (%s, %s, %s)"
        cursor.execute(query, (wallet_A_id, wallet_B_id, self.counter))
        self.db_connection.commit()
        cursor.close()
