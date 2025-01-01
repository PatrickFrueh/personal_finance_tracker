from src import transform

def main():
    # 1 - Extract: 

    # 2 - Transform: Transform the extracted data using categories (as DataFrame)
    categorized_data = transform.categorize_bank_transactions(
    bank_data_filepath="/home/pafr/repos/personal_finance_tracker/samples/sample_bank_data.csv",
    categories_filepath="/home/pafr/repos/personal_finance_tracker/.config/categories.json"
)


if __name__ == "__main__":
    main()