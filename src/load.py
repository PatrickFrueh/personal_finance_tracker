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

# @@@ Components for the function to come (...)
# df (categorized data from past step)
# env-path file (specified data)

# @@@ Test DataFrame
import pandas as pd
df = pd.DataFrame({
    'Buchung': ['2025-01-03', '2025-01-02'],
    'Auftraggeber/Empfänger': ['ING', 'Fabian Constantin Fruh'],
    'Verwendungszweck': ['GIROCARD 280000168540 MONATLICHES ENTGELT GIROCARD (DEBITKARTE)', 'Crunchyroll'],
    'Betrag': [-1.49, 2.5],
    'Kategorie': ['Unkategorisiert', 'Unkategorisiert']
    })

# Connect to the database
try:
    connection = mysql.connector.connect(**config)
    if connection.is_connected():
        print("Connected to MySQL database")
        cursor = connection.cursor()

        # Create table (if non existent)
        create_table_query = """
        CREATE TABLE IF NOT EXISTS transactions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            buchung DATE NOT NULL,
            auftraggeber_empfaenger VARCHAR(255) NOT NULL,
            verwendungszweck TEXT NOT NULL,
            betrag DECIMAL(10, 2) NOT NULL,
            kategorie VARCHAR(255) DEFAULT 'Unkategorisiert'
        );
        """
        cursor.execute(create_table_query)

except Error as e:
    print("Error while connecting to MySQL", e)

finally:
    # Close the connection
    if 'connection' in locals() and connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")

# @@@ Write df to MySQL DB
