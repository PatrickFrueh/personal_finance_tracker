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

if __name__ == '__main__':
    app.run(debug=True, port=5000)