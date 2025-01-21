import csv
import pandas as pd
import json

def categorize_bank_transactions(bank_data_filepath, categories_filepath):
    """
    Categorizes bank transactions based on description and recipient keywords.

    This function reads transaction data from a CSV file, cleans the data, and categorizes
    each transaction based on pre-defined keywords for descriptions and recipients. 
    The categorization is based on matching keywords from two sets: description and recipient keywords.
    
    Parameters:
    bank_data_filepath (str): 
        The path to the CSV file containing the bank transaction data. 
        The file should have transaction records with specific columns such as 'Verwendungszweck' and 'Auftraggeber/Empfänger'.
    categories_filepath (str): 
        The path to the JSON file containing categorization keywords. The JSON file should have two lists:
        - 'beschreibung_schluesselwoerter' for description-based keywords
        - 'empfaenger_schluesselwoerter' for recipient-based keywords

    Returns:
    pd.DataFrame: 
        A DataFrame with an additional column 'Kategorie', indicating the category for each transaction.

    Example:
    >>> categorized_df = categorize_bank_transactions('bank_data.csv', 'categories.json')
    """

    # Define the DataFrame column names
    # Initialize an empty DataFrame with the defined column names
    columns = ['Buchung', 'Valuta', 'Auftraggeber/Empfänger', 'Buchungstext', 'Verwendungszweck', 'Saldo', 'Währung', 'Betrag', 'Währung']
    df = pd.DataFrame(columns=columns)
    
    # Read and process the CSV file
    with open(bank_data_filepath, "r", encoding="ISO-8859-1") as file:
        reader = csv.reader(file, delimiter=";")
        
        # Skip the first 13 lines: header and irrelevant lines
        for _ in range(14):
            next(reader)
        
        # Append each cleaned line to the DataFrame
        for current_line_list in reader:
            stripped_line = [line.strip() for line in current_line_list]

            # Append row to DataFrame
            df.loc[len(df)] = stripped_line

    # Convert and validate date columns
    for date_col in ['Buchung', 'Valuta']:
        df[date_col] = pd.to_datetime(df[date_col], format='%d.%m.%Y', errors='coerce')  # Convert to datetime, invalid entries become NaT
        if df[date_col].isna().any():
            print(f"Warning: Invalid date entries found in column '{date_col}'")

    # Clean and validate numeric columns
    numeric_columns = ['Betrag', 'Saldo']
    for num_col in numeric_columns:
        if num_col in df.columns:  # Check column existence
            df[num_col] = df[num_col].str.replace(',', '.', regex=False)  # Replace commas with dots
            df[num_col] = pd.to_numeric(df[num_col], errors='coerce')  # Convert to numeric, invalid entries become NaN
            if df[num_col].isna().any():
                print(f"Warning: Invalid numeric entries found in column '{num_col}'")


    # Load the categorization keywords from the JSON file
    with open(categories_filepath, "r") as file:
        categories = json.load(file)
    
    # Separate the description and recipient keyword lists
    # Recipient-values override description-values in case of conflicts
    description_keywords = categories['beschreibung_schluesselwoerter']
    recipient_keywords = categories['empfaenger_schluesselwoerter']
    
    # Define an internal function for categorizing a transaction row
    def categorize_transaction(row):
        """
        Categorizes a single transaction row based on description and recipient keywords.

        Parameters:
        row (pd.Series): A row from the DataFrame representing a bank transaction.

        Returns:
        str: The category for the transaction.
        """

        description = row['Verwendungszweck'].lower()
        recipient = row['Auftraggeber/Empfänger'].lower()

        # Check for a match based on description keywords
        for category, keywords in description_keywords.items():
            if any(keyword in description for keyword in keywords):
                return category
        
        # Check for a match based on recipient keywords
        for category, keywords in recipient_keywords.items():
            if any(keyword in recipient for keyword in keywords):
                return category
        
        # Default category if no match is found
        return 'Unkategorisiert'
    
    # Apply categorization to each row in the DataFrame
    df['Kategorie'] = df.apply(categorize_transaction, axis=1)

    return df


def cleanup_bank_dataframe(categorized_bank_dataframe, columns_to_drop_filepath, bank_name):
    """
    Cleans up the given DataFrame by removing the columns specified for the given bank.

    This function removes the irrelevant columns from the provided DataFrame based on 
    a JSON configuration file. The columns to be removed are specific to each bank, 
    determined by the bank name provided.

    Parameters:
    categorized_bank_dataframe (pd.DataFrame): 
        The DataFrame containing the bank transaction data that needs to be cleaned.
    columns_to_drop_filepath (str): 
        The file path to the JSON file that specifies the columns to drop for each bank.
        The JSON file should map bank names to a list of column names to be removed.
    bank_name (str): 
        The name of the bank with corresponding columns that should be removed from the DataFrame.

    Returns:
    pd.DataFrame: 
        A cleaned DataFrame with the specified columns removed based on the provided bank name.

    Example:
    >>> df_cleaned = cleanup_bank_dataframe(categorized_df, 'columns_to_drop.json', 'ING DiBa')
    """

    # Dataframe to be cleaned up
    df = categorized_bank_dataframe

    # Open file to determine relevant columns to drop (dependent on bank)
    with open(columns_to_drop_filepath, "r") as file:
        columns_to_drop_data = json.load(file)

    # Extract column names to drop for the specified bank name
    columns_to_drop = columns_to_drop_data.get(bank_name, [])

    # Drop unwanted columns
    df = df.drop(columns=columns_to_drop)

    return df
