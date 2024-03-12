import mysql.connector

try:
    conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Passwd",
    database="WalletDB"  # Specify the database name here
    )
    print("Connected to the database successfully!")

except mysql.connector.Error as e:
    print(f"Error connecting to MySQL: {e}")

else:
    # Ensure conn is defined before checking if it's connected
    if conn.is_connected():
        conn.close()
        print("MySQL connection is closed")