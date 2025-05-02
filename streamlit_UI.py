import streamlit as st
import pymysql
import pandas as pd

# --- Streamlit UI setup ---
st.set_page_config(page_title="MySQL Query UI", layout="centered")  # Set the page title and layout
st.title("MySQL Database Query Tool")  # Display the main title at the top of the app

# --- Define available databases and tables ---
DATABASES = {
    "Competitions": "competitions",   # User-friendly name : actual database name
    "Complexes": "complexes",
    "Rankings": "rankings"
}

TABLES = {
    "competitions": ["Categories", "Competitions"],  # Tables in the 'competitions' database
    "complexes": ["Complexes", "Venues"],            # Tables in the 'complexes' database
    "rankings": ["Competitors", "Competitor_Rankings"]  # Tables in the 'rankings' database
}

# --- Sidebar for database and table selection ---
st.sidebar.header("Database & Table Selection")  # Sidebar section header
db_label = st.sidebar.selectbox(
    "Select Database", 
    list(DATABASES.keys())
)  # Dropdown for user to select the database (shows friendly names)
db_name = DATABASES[db_label]  # Get the actual database name from the selection

table_name = st.sidebar.selectbox(
    "Select Table",
    TABLES[db_name]  # Dropdown for user to select the table from the chosen database
)

# --- Show example query for selected table ---
example_queries = {
    "Categories": "SELECT * FROM Categories LIMIT 10;",
    "Competitions": "SELECT * FROM Competitions LIMIT 10;",
    "Complexes": "SELECT * FROM Complexes LIMIT 10;",
    "Venues": "SELECT * FROM Venues LIMIT 10;",
    "Competitors": "SELECT * FROM Competitors LIMIT 10;",
    "Competitor_Rankings": "SELECT * FROM Competitor_Rankings LIMIT 10;"
}
st.sidebar.markdown("**Example Query:**")  # Label for example query
st.sidebar.code(example_queries.get(table_name, ""))  # Show example SQL for the selected table

# --- SQL query input area ---
st.subheader("Enter your SQL query")  # Section header for SQL input
default_query = example_queries.get(table_name, "")  # Default query based on selected table
user_query = st.text_area(
    "SQL Query", 
    value=default_query, 
    height=100
)  # Text area for user to enter their SQL query

# --- Query execution and result display ---
if st.button("Run Query"):  # Button to execute the query
    try:
        # Connect to the selected database using pymysql
        connection = pymysql.connect(
            host="localhost",      # MySQL server address
            port=3306,             # MySQL port
            user="root",           # MySQL username
            password="ArunPavi*019",  # MySQL password
            database=db_name       # Database selected by the user
        )
        cursor = connection.cursor()  # Create a cursor object to execute SQL queries
        cursor.execute(user_query)    # Execute the user's SQL query

        # If the query is a SELECT, fetch and display results
        if user_query.strip().lower().startswith("select"):
            rows = cursor.fetchall()  # Fetch all rows from the result
            columns = [desc[0] for desc in cursor.description]  # Get column names
            df = pd.DataFrame(rows, columns=columns)  # Convert to pandas DataFrame for display
            st.success("Query executed successfully!")  # Show success message
            st.dataframe(df, use_container_width=True)  # Display the results as a table in Streamlit
        else:
            # For non-SELECT queries (INSERT, UPDATE, DELETE, etc.)
            connection.commit()  # Commit the transaction
            st.success("Query executed successfully (no results to display).")  # Show success message

        cursor.close()      # Close the cursor
        connection.close()  # Close the database connection

    except Exception as e:
        # If there is any error during connection or query execution, display it
        st.error(f"Error: {e}")

# --- Footer ---
st.markdown("---")  # Horizontal line for separation
st.caption("Developed with Streamlit • MySQL • Python")  # Footer note

# Note: Run the Streamlit app using streamlit run UI.py in your terminal