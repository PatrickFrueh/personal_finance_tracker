import os
from dotenv import load_dotenv

from src import transform
from src import load

def main():
    # 1 - Extract: 

    # 2 - Transform
    # Transform the extracted data using categories (as DataFrame)
    categorized_data = transform.categorize_bank_transactions(
    bank_data_filepath="/home/pafr/repos/personal_finance_tracker/samples/Umsatzanzeige_DE23500105175435590236_20250104.csv",
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
    
    # 3 - Load
    # Store data in the local database
    load.process_transactions(filtered_categorized_bank_data, database_credentials, auto_commit=False, overwrite_category=True)

if __name__ == "__main__":
    main()