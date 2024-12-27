from transform.transform_encapsulated import categorize_bank_transactions

# @@@ Load up the categorized data
df_categorized = categorize_bank_transactions(
    bank_data_filepath="/home/pafr/repos/personal_finance_tracker/transform/sample_output.csv",
    categories_filepath="/home/pafr/repos/personal_finance_tracker/transform/categories.json"
)

# Optionally, save the DataFrame to a new CSV if needed
df_categorized.to_csv("/path/to/output_categorized.csv", index=False)
print(df_categorized)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# from dotenv import load_dotenv
# import os
# import mysql.connector

# # Find .env-file
# load_dotenv()

# # Database configuration
# # Store the configuration in a dictionary
# config = {
#     'user': os.getenv('DB_USER'),
#     'password': os.getenv('DB_PASSWORD'),
#     'host': os.getenv('DB_HOST'),
#     'database': os.getenv('DB_NAME')
# }

# # Connect to the database
# try:
#     connection = mysql.connector.connect(**config)
#     if connection.is_connected():
#         print("Connected to MySQL database")

# except mysql.connector.Error as err:
#     print(f"Error: {err}")

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# @ Import dataframe (result of transform process)
# @@@ import transform.py, but enter path of bank data + categories.json as arguments
# -> Result will be a dataframe (categorized + adjusted)

# @ Write df to MySQL DB

# @ Create/Upload to online MySQL DB