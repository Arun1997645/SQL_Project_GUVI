import requests
import json
import pandas as pd
import pymysql
import urllib3

# Suppress only the single InsecureRequestWarning from urllib3 needed for local/dev
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# API endpoint and headers
url = "https://api.sportradar.com/tennis/trial/v3/en/complexes.json?api_key=y1FTs3L9jBrhvlEImxquFbulwlrKOTxly022vdkB"
headers = {"accept": "application/json"}

# Make the API request
response = requests.get(url, headers=headers, verify=False)
data = response.json()

# Extract the complexes data from the response
complexes = data.get('complexes', [])

# Prepare data for Complexes and Venues tables
complexes_set = set()  # To store unique complexes
venues_data = []       # To store venue details

# Loop through each complex and extract venue info
for complex_item in complexes:
    complex_id = complex_item['id']
    complex_name = complex_item['name']
    complexes_set.add((complex_id, complex_name))
    for venue in complex_item.get('venues', []):
        venues_data.append((
            venue['id'],
            venue['name'],
            venue.get('city_name', 'N/A'),
            venue.get('country_name', 'N/A'),
            venue.get('country_code', 'N/A'),
            venue.get('timezone', 'N/A'),
            complex_id
        ))

# Connect to MySQL database
connection = pymysql.connect(
    host="localhost",
    port=3306,
    user="root",
    password="ArunPavi*019",
    database="complexes"
)
cursor = connection.cursor()

# Create Complexes table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Complexes (
        complex_id VARCHAR(50) PRIMARY KEY,
        complex_name VARCHAR(100) NOT NULL
    );
""")

# Create Venues table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Venues (
        venue_id VARCHAR(50) PRIMARY KEY,
        venue_name VARCHAR(100) NOT NULL,
        city_name VARCHAR(100) NOT NULL,
        country_name VARCHAR(100) NOT NULL,
        country_code CHAR(3) NOT NULL,
        timezone VARCHAR(100) NOT NULL,
        complex_id VARCHAR(50),
        FOREIGN KEY (complex_id) REFERENCES Complexes(complex_id)
    );
""")

# Insert complexes into Complexes table
insert_complex = "INSERT IGNORE INTO Complexes (complex_id, complex_name) VALUES (%s, %s)"
for complex_row in complexes_set:
    cursor.execute(insert_complex, complex_row)

# Insert venues into Venues table
insert_venue = """
    INSERT IGNORE INTO Venues
    (venue_id, venue_name, city_name, country_name, country_code, timezone, complex_id)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
"""
for venue_row in venues_data:
    cursor.execute(insert_venue, venue_row)

# Commit the changes to the database
connection.commit()

# Close the cursor and connection
# cursor.close()
# connection.close()