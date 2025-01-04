import csv
import pandas as pd
import json

def categorize_bank_transactions(bank_data_filepath, categories_filepath):
    # Define the DataFrame column names
    columns = ['Buchung', 'Valuta', 'Auftraggeber/Empfänger', 'Buchungstext', 'Verwendungszweck', 'Saldo', 'Währung', 'Betrag', 'Währung']
    
    # Initialize an empty DataFrame with the appropriate columns
    df = pd.DataFrame(columns=columns)
    
    # Read and process the CSV file
    with open(bank_data_filepath, "r", encoding="ISO-8859-1") as file:
        reader = csv.reader(file, delimiter=";")
        
        # Skip the first 13 lines
        for _ in range(13):
            next(reader)
        
        # Append each cleaned line to the DataFrame
        for current_line_list in reader:
            stripped_line = [line.strip() for line in current_line_list]
            df.loc[len(df)] = stripped_line  # Append row to DataFrame
    
    # Load the categorization keywords from the JSON file
    with open(categories_filepath, "r") as file:
        categories = json.load(file)
    
    # Separate the description and recipient keyword lists
    description_keywords = categories['beschreibung_schluesselwoerter']
    recipient_keywords = categories['empfaenger_schluesselwoerter']
    
    # Define an internal function for categorizing a transaction row
    def categorize_transaction(row):
        description = row['Verwendungszweck'].lower()
        recipient = row['Auftraggeber/Empfänger'].lower()

        # Check description-based keywords
        for category, keywords in description_keywords.items():
            if any(keyword in description for keyword in keywords):
                return category
        
        # Check recipient-based keywords
        for category, keywords in recipient_keywords.items():
            if any(keyword in recipient for keyword in keywords):
                return category
        
        # Default category if no match is found
        return 'Unkategorisiert'
    
    # Apply categorization to each row in the DataFrame
    df['Kategorie'] = df.apply(categorize_transaction, axis=1)
    
    # Return the categorized DataFrame for further use
    return df
