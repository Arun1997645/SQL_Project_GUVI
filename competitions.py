import requests
import json
import pandas as pd
import pymysql
import urllib3

# Suppress only the single InsecureRequestWarning from urllib3 needed for local/dev
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# API endpoint and headers
url = "https://api.sportradar.com/tennis/trial/v3/en/competitions.json?api_key=y1FTs3L9jBrhvlEImxquFbulwlrKOTxly022vdkB"
headers = {"accept": "application/json"}

# Make the API request
response = requests.get(url, headers=headers , verify=False)

# Parse the JSON response
data = response.json()

# Extract the competitions data from the response
competitions = data.get('competitions', [])

# Prepare data for both tables: Categories and Competitions
categories_set = set()  # To store unique categories
competitions_data = []  # To store competition details

# Loop through each competition and extract category and competition info
for competition in competitions:
    cat_id = competition.get('category', {}).get('id', 'N/A')
    cat_name = competition.get('category', {}).get('name', 'N/A')
    categories_set.add((cat_id, cat_name))
    competitions_data.append({
        'competition_id': competition.get('id', 'N/A'),
        'competition_name': competition.get('name', 'N/A'),
        'parent_id': competition.get('parent_id'),  # can be None
        'type': competition.get('type', 'N/A'),
        'gender': competition.get('gender', 'N/A'),
        'category_id': cat_id
    })

# Connect to MySQL database
connection = pymysql.connect(
    host="localhost",
    port=3306,
    user="root",
    password="ArunPavi*019",
    database="competitions"
)
cursor = connection.cursor()

# Create Categories table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Categories (
        category_id VARCHAR(50) PRIMARY KEY,
        category_name VARCHAR(100) NOT NULL
    );
""")

# Create Competitions table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Competitions (
        competition_id VARCHAR(50) PRIMARY KEY,
        competition_name VARCHAR(100) NOT NULL,
        parent_id VARCHAR(50) NULL,
        type VARCHAR(20) NOT NULL,
        gender VARCHAR(10) NOT NULL,
        category_id VARCHAR(50),
        FOREIGN KEY (category_id) REFERENCES Categories(category_id)
    );
""")

# Insert unique categories into Categories table
insert_cat = "INSERT IGNORE INTO Categories (category_id, category_name) VALUES (%s, %s)"
for cat in categories_set:
    cursor.execute(insert_cat, cat)

# Insert competitions into Competitions table
insert_comp = """
    INSERT IGNORE INTO Competitions
    (competition_id, competition_name, parent_id, type, gender, category_id)
    VALUES (%s, %s, %s, %s, %s, %s)
"""
for comp in competitions_data:
    cursor.execute(insert_comp, (
        comp['competition_id'],
        comp['competition_name'],
        comp['parent_id'],
        comp['type'],
        comp['gender'],
        comp['category_id']
    ))

# Commit the changes to the database
connection.commit()

# Close the cursor and connection
# cursor.close()
# connection.close()