import mysql.connector

# Database configuration
config = {
    'user': 'patrick',
    'password': 'Bazinga27@',
    'host': 'localhost',
    'database': 'expenses_database'
}

# Connect to the database
try:
    connection = mysql.connector.connect(**config)
    if connection.is_connected():
        print("Connected to MySQL database")

except mysql.connector.Error as err:
    print(f"Error: {err}")

# @ Import dataframe (result of transform process)
# @@@ import transform.py, but enter path of bank data + categories.json as arguments
# -> Result will be a dataframe (categorized + adjusted)

# @ Write df to MySQL DB

# @ Create/Upload to online MySQL DB