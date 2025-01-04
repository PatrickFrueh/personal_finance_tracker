from src import transform

def main():
    # 1 - Extract: 

    # 2 - Transform: Transform the extracted data using categories (as DataFrame)
    categorized_data = transform.categorize_bank_transactions(
    bank_data_filepath="/home/pafr/repos/personal_finance_tracker/samples/Umsatzanzeige_DE23500105175435590236_20250104.csv",
    categories_filepath="/home/pafr/repos/personal_finance_tracker/.config/categories.json"
)

if __name__ == "__main__":
    main()