import os
from dotenv import load_dotenv
import threading

from tools.flask_server import app as flask_app
from src import extract
from src import transform
from src import load

# Temporary mock function: To be replaced with the actual API implementation in the future
def run_flask_app():
    """
    Start the Flask app to access the mock API.
    """
    flask_app.run(port=5000)

def main():
    # 1 - Extract:
    # Start the Flask server in a separate thread
    flask_thread = threading.Thread(target=run_flask_app)
    flask_thread.daemon = True  # Exit even if the Flask server is still running
    flask_thread.start()

    # Download the CSV file from the mock API
    API_URL = "http://127.0.0.1:5000/download-transactions"  # Mock API URL
    transactions_filename = "downloaded_transactions.csv"
    csv_file_path = f"res/{transactions_filename}"  # Where to save the downloaded file
    extract.download_csv_file(save_path=csv_file_path)

    # 2 - Transform
    # Transform the extracted data using categories (as DataFrame)
    categorized_data = transform.categorize_bank_transactions(
    bank_data_filepath=f"/home/pafr/repos/personal_finance_tracker/res/{transactions_filename}",
    categories_filepath="/home/pafr/repos/personal_finance_tracker/.config/categories.json"
    )
    
    # Find .env-file
    load_dotenv(dotenv_path=".config/.env")

    # Database credentials
    database_credentials = {
    'host': os.getenv('DB_HOST_LOCAL'),
    'user': os.getenv('DB_USER_LOCAL'),
    'password': os.getenv('DB_PASSWORD_LOCAL'),
    'database': os.getenv('DB_NAME_LOCAL'),
    'port': int(os.getenv('DEFAULT_PORT'))
    }
    
    # Clean up unwanted columns - specified by bank
    filtered_categorized_bank_data = transform.cleanup_bank_dataframe(categorized_data, "/home/pafr/repos/personal_finance_tracker/.config/exclude_columns_bank.json", "ING DiBa")
    print(filtered_categorized_bank_data)

    # 3 - Load
    # Store data in the local database
    load.process_transactions(filtered_categorized_bank_data, database_credentials, auto_commit=False, overwrite_category=True)

if __name__ == "__main__":
    main()