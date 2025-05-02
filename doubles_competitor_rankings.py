import requests
import json
import pymysql
import urllib3

# Suppress only the single InsecureRequestWarning from urllib3 needed for local/dev
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# API endpoint and headers
url = "https://api.sportradar.com/tennis/trial/v3/en/double_competitors_rankings.json?api_key=y1FTs3L9jBrhvlEImxquFbulwlrKOTxly022vdkB"
headers = {"accept": "application/json"}

# Make the API request
response = requests.get(url, headers=headers, verify=False)
data = response.json()

# Extract the rankings data from the response
rankings = data.get('rankings', [])

# Prepare a list to store all ranking and competitor info
rankings_data = []

# Loop through each ranking and extract competitor info
for ranking_item in rankings:
    type_id = ranking_item['type_id']
    ranking_name = ranking_item['name']
    year = ranking_item['year']
    week = ranking_item['week']
    gender = ranking_item['gender']
    for competitor_ranking in ranking_item.get('competitor_rankings', []):
        competitor_info = {
            'type_id': type_id,
            'ranking_name': ranking_name,
            'year': year,
            'week': week,
            'gender': gender,
            'rank': competitor_ranking['rank'],
            'movement': competitor_ranking['movement'],
            'points': competitor_ranking['points'],
            'competitions_played': competitor_ranking['competitions_played'],
            'competitor_id': competitor_ranking['competitor']['id'],
            'competitor_name': competitor_ranking['competitor']['name'],
            'country': competitor_ranking['competitor'].get('country', 'N/A'),
            'country_code': competitor_ranking['competitor'].get('country_code', 'N/A'),
            'abbreviation': competitor_ranking['competitor'].get('abbreviation', 'N/A')
        }
        rankings_data.append(competitor_info)

# Connect to MySQL database
connection = pymysql.connect(
    host="localhost",
    port=3306,
    user="root",
    password="ArunPavi*019",
    database="rankings"
)
cursor = connection.cursor()

# Create Competitors table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Competitors (
        competitor_id VARCHAR(50) PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        country VARCHAR(100) NOT NULL,
        country_code CHAR(3) NOT NULL,
        abbreviation VARCHAR(10) NOT NULL
    );
""")

# Create Competitor_Rankings table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Competitor_Rankings (
        rank_id INT PRIMARY KEY AUTO_INCREMENT,
        `rank` INT NOT NULL,
        movement INT NOT NULL,
        points INT NOT NULL,
        competitions_played INT NOT NULL,
        week INT NOT NULL,
        competitor_id VARCHAR(50),
        FOREIGN KEY (competitor_id) REFERENCES Competitors(competitor_id)
    );
""")

# Prepare SQL for inserting competitors (avoid duplicates)
insert_competitor = """
    INSERT IGNORE INTO Competitors
    (competitor_id, name, country, country_code, abbreviation)
    VALUES (%s, %s, %s, %s, %s)
"""

# Prepare SQL for inserting rankings
insert_ranking = """
    INSERT INTO Competitor_Rankings
    (`rank`, movement, points, competitions_played, week, competitor_id)
    VALUES (%s, %s, %s, %s, %s, %s)
"""

# Insert data into both tables
for row in rankings_data:
    # Insert competitor info
    cursor.execute(insert_competitor, (
        row['competitor_id'],
        row['competitor_name'],
        row['country'],
        row['country_code'],
        row['abbreviation']
    ))
    # Insert ranking info
    cursor.execute(insert_ranking, (
        row['rank'],
        row['movement'],
        row['points'],
        row['competitions_played'],
        row['week'],
        row['competitor_id']
    ))

# Commit the changes to the database
connection.commit()

# Close the cursor and connection
# cursor.close()
# connection.close()