from flask import Flask, jsonify
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="../../.config/.env")

app = Flask(__name__)

# Database connection
def connect_to_db(**database_credentials):
    connection = mysql.connector.connect(**database_credentials)

    return connection

# Database credentials
database_credentials = {
'host': os.getenv('DB_HOST_LOCAL'),
'user': os.getenv('DB_USER_LOCAL'),
'password': os.getenv('DB_PASSWORD_LOCAL'),
'database': os.getenv('DB_NAME_LOCAL'),
'port': int(os.getenv('DEFAULT_PORT'))
}

@app.route('/api/spending-categories', methods=['GET'])
def get_spending_categories(**database_credentials):
    # Connect to the DB
    connector = connect_to_db(**database_credentials)
    cursor = connector.cursor(dictionary=True)
    
    # Query to fetch categorized spending data (sum of each category)
    cursor.execute("SELECT Kategorie, SUM(Betrag) as total_spent FROM transactions GROUP BY Kategorie")
    summary_result = cursor.fetchall()
    
    # Query to fetch all individual transactions
    cursor.execute("SELECT Buchung, Auftraggeber/Empfänger, Verwendungszweck, Betrag, Kategorie FROM transactions")
    transactions_result = cursor.fetchall()

    # Close DB connection
    cursor.close()
    connector.close()
    
    # Combine the results into a structured JSON response
    response = {
        'summary': summary_result,  # Aggregated spending per category
        'transactions': transactions_result  # Individual transaction details
    }

    # Return the combined data as a JSON response
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, port=5000)