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

        # Iterate over each row in the DataFrame and process
        for index, row in df.iterrows():
            # Step 1: Check if the transaction already exists and if its category is still "Unkategorisiert"
            select_query = """
            SELECT COUNT(*) FROM transactions
            WHERE buchung = %s AND auftraggeber_empfaenger = %s AND verwendungszweck = %s
            AND kategorie = 'Unkategorisiert'
            """
            cursor.execute(select_query, (row['Buchung'], row['Auftraggeber/Empfänger'], row['Verwendungszweck']))
            count = cursor.fetchone()[0]

            # Step 2: If the transaction exists and is uncategorized, update it with the new category
            if count > 0:
                update_query = """
                UPDATE transactions
                SET kategorie = %s
                WHERE buchung = %s AND auftraggeber_empfaenger = %s AND verwendungszweck = %s
                AND kategorie = 'Unkategorisiert'
                """
                cursor.execute(update_query, (row['Kategorie'], row['Buchung'], row['Auftraggeber/Empfänger'], row['Verwendungszweck']))
                print(f"Updated category for transaction: {row['Buchung']} - {row['Auftraggeber/Empfänger']}")

            # Step 3: If the transaction doesn't exist, insert it with 'Unkategorisiert' as the category
            else:
                insert_query = """
                INSERT INTO transactions (buchung, auftraggeber_empfaenger, verwendungszweck, betrag, kategorie)
                VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(insert_query, (row['Buchung'], row['Auftraggeber/Empfänger'], row['Verwendungszweck'], row['Betrag'], row['Kategorie']))
                print(f"Inserted new transaction: {row['Buchung']} - {row['Auftraggeber/Empfänger']}")

            # Commit the changes after each row has been processed
            connection.commit()
        
except Error as e:
    print("Error while connecting to MySQL", e)

finally:
    # Close the connection
    if 'connection' in locals() and connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")

# @@@ Write df to MySQL DB
