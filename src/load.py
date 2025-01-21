from dotenv import load_dotenv
import os
import mysql.connector
from mysql.connector import Error

def process_transactions(transaction_data, database_credentials, table_name="transactions", auto_commit=True, overwrite_category=False):
    """
    Processes bank transactions by inserting or updating records in a MySQL database.

    This function takes categorized transaction data, connects to a specified MySQL database, 
    and ensures that the transactions are properly inserted or updated. If a transaction already 
    exists, its category can optionally be updated. If it does not exist, it will be inserted into 
    the database. The function also allows for automatic or manual commit control.

    Parameters:
    transaction_data (pd.DataFrame): 
        A DataFrame containing the transaction data to be processed. It must have the following columns:
        - 'Buchung' (DATE): Transaction date.
        - 'Auftraggeber/Empfänger' (VARCHAR): Transaction sender/recipient.
        - 'Verwendungszweck' (TEXT): Description of the transaction.
        - 'Betrag' (DECIMAL): Transaction amount.
        - 'Kategorie' (VARCHAR): Category of the transaction.
    database_credentials (dict): 
        A dictionary containing the MySQL database configuration values. The keys must include:
        - 'host': The hostname or IP address of the MySQL server.
        - 'user': The username to connect to the database.
        - 'password': The password for the given username.
        - 'database': The name of the database to connect to.
        - 'port' (optional): The port number for the MySQL server (default is 3306).
    table_name (str): 
        The name of the table in the database to interact with. Defaults to 'transactions'.
    auto_commit (bool): 
        A flag indicating whether to commit changes after each processed transaction. Defaults to True.
    overwrite_category (bool): 
        A flag to decide whether to update the category of existing transactions. If False, only 
        transactions with the category 'Unkategorisiert' will be updated. Defaults to False.

    Returns:
    None

    Example:
    >>> from dotenv import load_dotenv
    >>> import pandas as pd
    >>> import os
    >>> load_dotenv()  # Load environment variables from .env file
    >>> db_credentials = {
    >>>     "host": os.getenv("DB_HOST"),
    >>>     "user": os.getenv("DB_USER"),
    >>>     "password": os.getenv("DB_PASSWORD"),
    >>>     "database": os.getenv("DB_NAME"),
    >>>     "port": int(os.getenv("DB_PORT", 3306))
    >>> }
    >>> # Example DataFrame
    >>> transactions = pd.DataFrame({
    >>>     "Buchung": ["2025-01-01", "2025-01-02"],
    >>>     "Auftraggeber/Empfänger": ["John Doe", "Acme Corp"],
    >>>     "Verwendungszweck": ["Payment for invoice #123", "Subscription fee"],
    >>>     "Betrag": [100.50, 49.99],
    >>>     "Kategorie": ["Invoices", "Subscriptions"]
    >>> })
    >>> process_transactions(transactions, db_credentials, auto_commit=True)
    """

    # Establish a connection to the MySQL database and initialize a cursor if successful.
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