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

        


# @ cluster table into proper format
# -> Remove first 2 lines
# -> Delimiter: Pipe

# @ assign expense to corresponding category