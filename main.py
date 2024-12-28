from src import transform

def main():

    # 2 - Transform the extracted data using categories
    categorized_data = transform.categorize_bank_transactions(
    bank_data_filepath="/home/pafr/repos/personal_finance_tracker/samples/sample_bank_data.csv",
    categories_filepath="/home/pafr/repos/personal_finance_tracker/.config/categories.json"
)
    print(categorized_data)



if __name__ == "__main__":
    main()