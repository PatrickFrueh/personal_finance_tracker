from dotenv import load_dotenv
import os
import mysql.connector
from mysql.connector import Error





# @@@ Components for the function to come (...)
# df (categorized data from past step)
# env-path file (specified data)

def process_transactions(transaction_data, database_credentials, table_name="transactions", auto_commit=True, overwrite_category=False):
    """
    Function to insert or update transactions in a MySQL database.

    Parameters:
    transaction_data (pd.DataFrame): DataFrame containing the transaction data to be processed.
    database_credentials (dict): Dictionary containing database configuration values (host, user, password, database, port).
    table_name (str): Name of the table in the database to interact with. Defaults to 'transactions'.
    auto_commit (bool): Flag to control whether to commit after each row. Defaults to True.
    overwrite_category (bool): Flag to decide if categories should be updated even if not 'Unkategorisiert'. Defaults to False.
    """

    try:
        connection = mysql.connector.connect(**database_credentials)
        
        if connection.is_connected():
            print(f"Connected to MySQL database: {database_credentials['database']}")
            cursor = connection.cursor()

            # Create table (if non-existent)
            create_table_query = f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INT AUTO_INCREMENT PRIMARY KEY,
                buchung DATE NOT NULL,
                auftraggeber_empfaenger VARCHAR(255) NOT NULL,
                verwendungszweck TEXT NOT NULL,
                betrag DECIMAL(10, 2) NOT NULL,
                kategorie VARCHAR(255)
            );
            """
            cursor.execute(create_table_query)

            # Iterate over each row in the DataFrame and process
            for index, row in transaction_data.iterrows():
                # Step 1: Check if the transaction already exists
                select_query = f"""
                SELECT COUNT(*) FROM {table_name}
                WHERE buchung = %s AND auftraggeber_empfaenger = %s AND verwendungszweck = %s
                """
                cursor.execute(select_query, (row['Buchung'], row['Auftraggeber/Empfänger'], row['Verwendungszweck']))
                count = cursor.fetchone()[0]

                if count > 0:
                    # Step 2: If the transaction exists, update its category (if needed)
                    if overwrite_category or row['Kategorie'] == 'Unkategorisiert':
                        update_query = f"""
                        UPDATE {table_name}
                        SET kategorie = %s
                        WHERE buchung = %s AND auftraggeber_empfaenger = %s AND verwendungszweck = %s
                        """
                        cursor.execute(update_query, (row['Kategorie'], row['Buchung'], row['Auftraggeber/Empfänger'], row['Verwendungszweck']))
                        print(f"Updated category for transaction: {row['Buchung']} - {row['Auftraggeber/Empfänger']}")
                else:
                    # Step 3: If the transaction doesn't exist, insert it
                    insert_query = f"""
                    INSERT INTO {table_name} (buchung, auftraggeber_empfaenger, verwendungszweck, betrag, kategorie)
                    VALUES (%s, %s, %s, %s, %s)
                    """
                    cursor.execute(insert_query, (row['Buchung'], row['Auftraggeber/Empfänger'], row['Verwendungszweck'], row['Betrag'], row['Kategorie']))
                    print(f"Inserted new transaction: {row['Buchung']} - {row['Auftraggeber/Empfänger']}")

                # Step 4: Commit the changes
                if auto_commit:
                    connection.commit()

            # If auto_commit is False, commit once after all rows
            if not auto_commit:
                connection.commit()

    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
    
    finally:
        # Close the connection
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")