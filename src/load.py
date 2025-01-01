from transform import categorize_bank_transactions

# # Load up the categorized data
# df_categorized = categorize_bank_transactions(
#     bank_data_filepath="/home/pafr/repos/personal_finance_tracker/samples/sample_bank_data.csv",
#     categories_filepath="/home/pafr/repos/personal_finance_tracker/.config/categories.json"
# )

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
from dotenv import load_dotenv
import os
import mysql.connector
from mysql.connector import Error

# Find .env-file
load_dotenv(dotenv_path=".config/.env")

# Database configuration
# Store the configuration in a dictionary
config = {
    'host': os.getenv('RDS_ENDPOINT'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME'),
    'port': os.getenv('DEFAULT_PORT')
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

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# @ Import dataframe (result of transform process)
# @@@ import transform.py, but enter path of bank data + categories.json as arguments
# -> Result will be a dataframe (categorized + adjusted)

# @ Write df to MySQL DB

# @ Create/Upload to online MySQL DB