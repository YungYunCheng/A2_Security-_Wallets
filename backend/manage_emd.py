from flask import session, jsonify
import hashlib
import mysql.connector
from mysql.connector import Error

# Function to generate EDM and store data in the database
def generate_emd(student_id, amount):
    # Get the user_id of the logged-in user from the session
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "User not logged in."}), 401  # Unauthorized

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

        # Check if the wallet_id already exists
        db_cursor.execute("SELECT COUNT(*) FROM wallets WHERE wallet_id = %s", (student_id,))
        count = db_cursor.fetchone()[0]
        if count > 0:
            return jsonify({"error": f"Wallet ID {student_id} already exists."}), 400  # Bad Request

        # Insert the new wallet data
        sql_query = "INSERT INTO wallets (wallet_id, user_id, wallet_amount, wallet_B_amount, security_key, counter) VALUES (%s, %s, %s, %s, %s, %s)"
        data_to_insert = (student_id, user_id, amount_decimal, 0, secret_key, 0)
        db_cursor.execute(sql_query, data_to_insert)
        db_connection.commit()

        return jsonify({"message": f"EDM generated for student {student_id} with amount {amount}. Data stored successfully in the database."})

    except Error as e:
        return jsonify({"error": f"Error occurred while generating EDM and storing data in the database: {e}"}), 500  # Internal Server Error

    finally:
        if 'db_connection' in locals() and db_connection.is_connected():
            db_cursor.close()
            db_connection.close()
