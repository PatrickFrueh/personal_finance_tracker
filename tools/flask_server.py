from flask import Flask, send_file

# Initialize Flask web application
app = Flask(__name__)

# Decorator to request specific endpoint, e.g. http://127.0.0.1:5000/download-transactions
@app.route('/download-transactions', methods=['GET'])
def download_transactions():
    """
    Endpoint to simulate downloading a CSV file.
    """

    # Specify path to sample bank data and mock return from server
    file_path = "/home/pafr/repos/personal_finance_tracker/samples/Umsatzanzeige_DE23500105175435590236_20250104.csv"
    return send_file(file_path, as_attachment=True)

if __name__ == "__main__":
    app.run(port=5000)