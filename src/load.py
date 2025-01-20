from dotenv import load_dotenv
import os
import mysql.connector
from mysql.connector import Error

# Find .env-file
load_dotenv(dotenv_path=".config/.env")

# Database configuration
config = {
    'host': os.getenv('DB_HOST_LOCAL'),
    'user': os.getenv('DB_USER_LOCAL'),
    'password': os.getenv('DB_PASSWORD_LOCAL'),
    'database': os.getenv('DB_NAME_LOCAL'),
    'port': int(os.getenv('DEFAULT_PORT'))
}

# Connect to the database
try:
    connection = mysql.connector.connect(**config)
    if connection.is_connected():
        print("Connected to MySQL database")

        # Run a test query
        cursor = connection.cursor()
        cursor.execute("SELECT DATABASE();")
        record = cursor.fetchone()
        print("You're connected to:", record[0])

except Error as e:
    print("Error while connecting to MySQL", e)

finally:
    # Close the connection
    if 'connection' in locals() and connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")

# @@@ Write df to MySQL DB
