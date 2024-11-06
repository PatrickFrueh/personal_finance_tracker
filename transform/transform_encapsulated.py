import csv
import pandas as pd
import json

def categorize_bank_transactions(csv_filepath, json_filepath):
    # Define the DataFrame column names
    columns = ['Datum', 'Transaktionstyp', 'Begünstigter/Zahlungspflichtiger', 'IBAN', 'Betrag', 'Währung', 'Verwendungszweck', 'Kontostand nach Buchung']
    
    # Initialize an empty DataFrame with the appropriate columns
    df = pd.DataFrame(columns=columns)
    
    # Read and process the CSV file
    with open(csv_filepath, "r") as file:
        reader = csv.reader(file, delimiter="|")
        
        # Skip the first two lines
        next(reader)
        next(reader)
        
        # Append each cleaned line to the DataFrame
        for current_line_list in reader:
            stripped_line = [line.strip() for line in current_line_list]
            df.loc[len(df)] = stripped_line  # Append row to DataFrame
    
    # Load the categorization keywords from the JSON file
    with open(json_filepath, "r") as file:
        categories = json.load(file)
    
    # Separate the description and recipient keyword lists
    description_keywords = categories['beschreibung_schluesselwoerter']
    recipient_keywords = categories['empfaenger_schluesselwoerter']
    
    # Define an internal function for categorizing a transaction row
    def categorize_transaction(row):
        description = row['Verwendungszweck'].lower()
        recipient = row['Begünstigter/Zahlungspflichtiger'].lower()

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
