import csv
import pandas as pd
import json

# # Read bank logs
# Define the DataFrame column names
columns = ['Datum', 'Transaktionstyp', 'Begünstigter/Zahlungspflichtiger', 'IBAN', 'Betrag', 'Währung', 'Verwendungszweck', 'Kontostand nach Buchung']

# Initialize an empty DataFrame with the appropriate columns
df = pd.DataFrame(columns=columns)

# Open and read the file progressively
with open("/home/pafr/repos/personal_finance_tracker/transform/sample_output.csv", "r") as file:
    reader = csv.reader(file, delimiter="|")

    # Skip the first two lines
    next(reader)
    next(reader)

    for current_line_list in reader:
        # Removing leading and trailing space
        stripped_line = [line.strip() for line in current_line_list]
        
        # Append the cleaned data to the DataFrame
        df.loc[len(df)] = stripped_line  # Appends row to the DataFrame


# # Categorize transactions
# Load the keywords from the JSON file
with open("/home/pafr/repos/personal_finance_tracker/transform/categories.json", "r") as file:
    categories = json.load(file)

# Separate the description and recipient keyword lists
description_keywords = categories['beschreibung_schluesselwoerter']
recipient_keywords = categories['empfaenger_schluesselwoerter']

def categorize_transaction(row):
    description = row['Verwendungszweck'].lower()  # Convert the description to lowercase for comparison
    recipient = row['Begünstigter/Zahlungspflichtiger'].lower()  # Convert the recipient to lowercase for comparison

    # Description-based categorization
    for category, keywords in description_keywords.items():
        # Check if any keyword from the description_keywords list is in the 'Verwendungszweck' field
        if any(keyword in description for keyword in keywords): # 1st: for keyword in keywords -> keyword in description
            return category  # Return the category if a match is found

    # Recipient-based categorization
    for category, keywords in recipient_keywords.items():
        # Check if any keyword from the recipient_keywords list is in the 'Empfänger' field
        if any(keyword in recipient for keyword in keywords):
            return category  # Return the category if a match is found

    # If no category is matched, return 'Unkategorisiert'
    return 'Unkategorisiert'

# Apply the *new* categorization function to each row of the DataFrame
df['Kategorie'] = df.apply(categorize_transaction, axis=1)

# @ Future features: Add categories using chatgpt / matain every X weeks: collect "Unkategorisiert"
