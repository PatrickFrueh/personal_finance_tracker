from flask import Flask, jsonify
from flask_cors import CORS

import mysql.connector
from mysql.connector import Error

from dotenv import load_dotenv
import os

# Find .env-file using the absolute path
load_dotenv(dotenv_path="/home/pafr/repos/personal_finance_tracker/.config/.env")

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])

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
def get_spending_categories():
    # Try to establish a connection to the MySQL database
    try:
        connection = mysql.connector.connect(**database_credentials)
        
        if connection.is_connected():
            print(f"Connected to MySQL database: {database_credentials['database']}")
            cursor = connection.cursor(dictionary=True)

            # Query to fetch categorized spending data (sum of each category)
            cursor.execute("SELECT Kategorie, SUM(Betrag) as total_spent FROM transactions GROUP BY Kategorie")
            summary_result = cursor.fetchall()

            # Query to fetch all individual transactions
            cursor.execute("SELECT Buchung, Auftraggeber/Empfänger, Verwendungszweck, Betrag, Kategorie FROM transactions")
            transactions_result = cursor.fetchall()

            # Close DB connection
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

            # Return the results as a structured JSON response
            return jsonify({
                'summary': summary_result,  # Aggregated spending per category
                'transactions': transactions_result  # Individual transaction details
            })
    
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return jsonify({'error': f"Error while connecting to MySQL: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)