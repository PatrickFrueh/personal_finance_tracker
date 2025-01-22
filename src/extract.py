import requests

API_URL = "http://127.0.0.1:5000/download-transactions"

def download_csv_file(save_path="/home/pafr/repos/personal_finance_tracker/samples/downloaded_transactions.csv"):
    """
    Fetches the CSV file from the API and saves it locally.
    """
    response = requests.get(API_URL)
    
    # Raise an error if the request fails
    response.raise_for_status()

    # Save the content of the response to a file
    with open(save_path, "wb") as file:
        file.write(response.content)

    print(f"CSV file downloaded and saved as {save_path}")

if __name__ == "__main__":
    download_csv_file()