# Tennis Data Analysis Project

This project provides a complete workflow for ingesting, storing, analyzing, and visualizing tennis-related data using Python, MySQL, and Streamlit.  
It is designed for learning, interviews, and practical database/data analysis experience.

---

## Project Structure

```
First project/
│
├── competitions.py                # Loads competitions & categories data into MySQL
├── Complexes.py                   # Loads complexes & venues data into MySQL
├── doubles_competitor_rankings.py # Loads competitor rankings & competitors into MySQL
├── streamlit_UI.py                # Streamlit web app for querying and exploring your data
└── README.md                      # (This file)
```

---

## Prerequisites

- Python 3.x
- MySQL Server (running locally)
- Python packages: `pymysql`, `pandas`, `streamlit`, `requests`, `urllib3`

Install Python packages with:
```sh
pip install pymysql pandas streamlit requests urllib3
```

---

## Database Setup

You will need **three MySQL databases**:
- `competitions`
- `complexes`
- `rankings`

Create them in MySQL Workbench or CLI:
```sql
CREATE DATABASE competitions;
CREATE DATABASE complexes;
CREATE DATABASE rankings;
```

---

## Scripts Overview

### 1. `competitions.py`
- Fetches competitions and categories data from the API.
- Creates `Categories` and `Competitions` tables in the `competitions` database.
- Inserts the data.

### 2. `Complexes.py`
- Fetches complexes and venues data from the API.
- Creates `Complexes` and `Venues` tables in the `complexes` database.
- Inserts the data.

### 3. `doubles_competitor_rankings.py`
- Fetches competitor rankings and competitor details from the API.
- Creates `Competitors` and `Competitor_Rankings` tables in the `rankings` database.
- Inserts the data.

### 4. `streamlit_UI.py`
- Interactive Streamlit web app.
- Lets you select a database and table, enter custom SQL queries, and view results in a table.
- Provides example queries for each table.
- User-friendly interface for exploring your data.

---

## How to Use

1. **Run the Data Loader Scripts**
   - Run `competitions.py`, `Complexes.py`, and `doubles_competitor_rankings.py` to populate your MySQL databases.
   - Example:
     ```sh
     python competitions.py
     python Complexes.py
     python doubles_competitor_rankings.py
     ```

2. **Start the Streamlit App**
   - In your terminal, run:
     ```sh
     streamlit run streamlit_UI.py
     ```
   - Open the provided local URL in your browser.

3. **Explore Your Data**
   - Use the sidebar to select the database and table.
   - Enter your own SQL queries or use the provided examples.
   - View results as interactive tables.

---

## Example SQL Queries

- **List all competitions with their category name:**
  ```sql
  SELECT c.competition_id, c.competition_name, cat.category_name
  FROM Competitions c
  JOIN Categories cat ON c.category_id = cat.category_id;
  ```

- **List all venues with their complex name:**
  ```sql
  SELECT v.venue_id, v.venue_name, c.complex_name
  FROM Venues v
  JOIN Complexes c ON v.complex_id = c.complex_id;
  ```

- **Get all competitors with their rank and points:**
  ```sql
  SELECT c.competitor_id, c.name, cr.rank, cr.points
  FROM Competitors c
  JOIN Competitor_Rankings cr ON c.competitor_id = cr.competitor_id;
  ```

---

## Notes

- **Credentials:** The scripts use `user="root"` and `password="ArunPavi*019"`. Change these if your MySQL credentials are different.
- **API Keys:** The scripts use a demo API key. Replace with your own if needed.
- **Security:** Never share your real database credentials in production code.

---

## Author

Developed for learning and interview preparation.  
Feel free to extend or modify for your own use!