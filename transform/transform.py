import csv
import pandas as pd

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


# @@@ assign expense to corresponding category

# check for keywords
# -> assign relevant keywords: use an external file to keep it maintable, even for non-coding people
# yaml? easy to read, first in contact with file type

# -> flag keywords that aren't assigned and need to be added
# ??? later on: add ai categorization