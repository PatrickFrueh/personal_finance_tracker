from flask import Flask, jsonify, request
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
    """
    Fetches categorized spending data and individual transaction details from the database.

    This endpoint retrieves two sets of data from the MySQL database:
    1. A summary of spending per category, showing the total amount spent in each category.
    2. A list of individual transactions, including details such as the transaction description, 
       amount, and category.

    This data is intended to be used by a frontend application for visualization purposes. 
    The frontend will use the aggregated spending data and individual transaction details to present 
    a comprehensive view of the user's financial data.

    It connects to a MySQL database, executes queries to fetch the necessary data, and 
    returns the results in a structured JSON format. If any error occurs during the database 
    connection or query execution, an error message will be returned.

    Returns:
    JSON: 
        A JSON object containing two keys:
        - 'summary': A list of dictionaries with the total amount spent per category.
        - 'transactions': A list of dictionaries with individual transaction details.
        
    Example response:
    {
        "summary": [
            {"Kategorie": "Groceries", "total_spent": 150.75},
            {"Kategorie": "Entertainment", "total_spent": 50.00}
        ],
        "transactions": [
            {"buchung": "2025-01-01", "auftraggeber_empfaenger": "John Doe", "verwendungszweck": "Grocery store", "betrag": 50.00, "kategorie": "Groceries"},
            {"buchung": "2025-01-02", "auftraggeber_empfaenger": "Netflix", "verwendungszweck": "Subscription fee", "betrag": 15.00, "kategorie": "Entertainment"}
        ]
    }

    Error Response:
    If the database connection fails or any error occurs, the response will contain an 
    error message:
    {
        "error": "Error while connecting to MySQL: <error-details>"
    }

    Example:
    >>> from flask import Flask, jsonify
    >>> app = Flask(__name__)
    >>> @app.route('/api/spending-categories', methods=['GET'])
    >>> def get_spending_categories():
    >>>     # function implementation
    >>>     return jsonify({"summary": summary_result, "transactions": transactions_result})
    """

    start_date = request.args.get('startDate')  # 'startDate' from query params
    end_date = request.args.get('endDate')  # 'endDate' from query params
    print(f"Querying for transactions from {start_date} to {end_date}")

    # Try to establish a connection to the MySQL database
    try:
        connection = mysql.connector.connect(**database_credentials)
        
        if connection.is_connected():
            print(f"Connected to MySQL database: {database_credentials['database']}")
            cursor = connection.cursor(dictionary=True)

            # Query to fetch categorized spending data (sum of each category)
            query_sum = """
                SELECT Kategorie, SUM(ABS(Betrag)) AS total_spent 
                FROM transactions 
                WHERE Betrag < 0 
                AND buchung BETWEEN %s AND %s
                GROUP BY Kategorie
            """
            cursor.execute(query_sum, (start_date, end_date))  # Pass the start_date and end_date
            summary_result = cursor.fetchall()

            # Query to fetch all individual transactions
            query_transactions = """
                SELECT buchung, auftraggeber_empfaenger, verwendungszweck, ABS(Betrag) as betrag, kategorie 
                FROM transactions 
                WHERE Betrag < 0 
                AND buchung BETWEEN %s AND %s
            """
            cursor.execute(query_transactions, (start_date, end_date))  # Pass the start_date and end_date
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