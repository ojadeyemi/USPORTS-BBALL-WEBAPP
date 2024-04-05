"""
USports Basketball Data Processing Script

This script is used to override the old tables with the new table containing the latest data fetched from the USports website. The usports_team_stats and usports_player_stats functions, which are imported from another Python file, are used to parse through the USports website and collect statistics into pandas DataFrame objects.

Dependencies:
- SQLAlchemy: Used for interacting with the MySQL database.

Usage:
- Before running the script, ensure that a MySQL database is set up and accessible.
- Modify the connection_string variable to specify the connection details for the MySQL database.
- Ensure that the necessary tables and schema are set up in the database.
- Execute the script to fetch, process, and store the basketball statistics data in the database.

Author:
OJ Adeyemi

Date:
March 10, 2024
"""

from sqlalchemy import create_engine, text
from functions import usports_team_stats, usports_player_stats

#DO NOT MODIFY UNLESS YOU ARE OJ ADEYEMI
connection_string = 'sqlite:///../database/usports_bball_test.sqlite'

try:
    # Create a SQLAlchemy engine
    engine = create_engine(connection_string)
    engine.connect()
    print("Connection successful!")
except Exception as e:
    print("Error connecting to the database:", e)


try:
    #dataframe for teams
    men_df = usports_team_stats('men')
    women_df = usports_team_stats('women')

    #datafram for players
    men_players_df = usports_player_stats('men')
    women_players_df = usports_player_stats('women')
except (ImportError, ValueError, TypeError) as e:
    # Handle specific types of errors
    print(f"Error creating DataFrame: {e}")
    raise
except Exception as e:
    # Handle any other unexpected errors
    print(f"Unexpected error: {e}")
    raise


# Convert the DataFrame to an SQL table
# Add a primary key column to the DataFrame
men_df['team_id'] = range(1, len(men_df) + 1)
women_df['team_id'] = range(1, len(men_df) + 1)
men_players_df['player_id'] = range(1, len(men_players_df) + 1)
women_players_df['player_id'] = range(1, len(women_players_df) + 1)

try:
    # Attempt to write men_df DataFrame to SQLite database
    men_df.to_sql('men_team_test', con=engine, if_exists='replace', index=False)
    print("Men's team data written to 'men_team_test' table successfully!")
except Exception as e:
    print("Error writing men's team data to database:", e)

try:
    # Attempt to write women_df DataFrame to SQLite database
    women_df.to_sql('women_team_test', con=engine, if_exists='replace', index=False)
    print("Women's team data written to 'women_team_test' table successfully!")
except Exception as e:
    print("Error writing women's team data to database:", e)

try:
    # Attempt to write men_players_df DataFrame to SQLite database
    men_players_df.to_sql('men_players_test', con=engine, if_exists='replace', index=False)
    print("Men's players data written to 'men_players_test' table successfully!")
except Exception as e:
    print("Error writing men's players data to database:", e)

try:
    # Attempt to write women_players_df DataFrame to SQLite database
    women_players_df.to_sql('women_players_test', con=engine, if_exists='replace', index=False)
    print("Women's players data written to 'women_players_test' table successfully!")
except Exception as e:
    print("Error writing women's players data to database:", e)


sql_queries =[ "ALTER TABLE men_players_test ADD COLUMN team_id INTEGER;",
    "UPDATE men_players_test SET team_id = ( SELECT team_id FROM men_team_test WHERE men_players_test.school = men_team_test.team_name);", 
    "ALTER TABLE women_players_test  ADD COLUMN team_id INTEGER; ",
    " UPDATE women_players_test SET team_id = (SELECT team_id  FROM women_team_test WHERE women_players_test.school = women_team_test.team_name  ); "]

try:
    # Connect to the database and execute SQL queries
    with engine.connect() as con:
        for idx, query in enumerate(sql_queries, start=1):
            print(f"Executing SQL Query {idx}:")
            con.execute(text(query))
            con.commit()
            print("Executed query:", query.strip(), '\n')
        print("All SQL queries executed successfully.")
except Exception as e:
    print("An error occurred while executing SQL queries:", e)


try:
    # SQL query to check if the table exists
    check_table_query = """
    SELECT name FROM sqlite_master WHERE type='table' AND name='feedback_test'
    """

    # Check if the table exists
    result = engine.connect().execute(text(check_table_query))
    table_exists = result.fetchone()

    # If the table does not exist, create it
    if not table_exists:
        create_table_query = """
        CREATE TABLE feedback_test (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            message TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """
        engine.connect().execute(text(create_table_query))
        print("Table 'feedback_test' created successfully.")
    else:
        print("Table 'feedback_test' already exists.")

except Exception as e:
    print("An error occurred while executing SQL queries for feedback table:", e)


# Close the database connection
result.close()