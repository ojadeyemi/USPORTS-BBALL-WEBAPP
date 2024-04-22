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
import os
import sys
from sqlalchemy import create_engine, text
from usports_webscraper import usports_team_stats, usports_player_stats


mysqldatabase = f"mysql+pymysql://root:{os.environ.get('USPORT_BBALL_PASSWORD')}@localhost/usports_bball"


# DO NOT MODIFY UNLESS YOU ARE OJ ADEYEMI
connection_string = mysqldatabase

try:
    # Create a SQLAlchemy engine
    engine = create_engine(connection_string)
    engine.connect()
    print("Connection successful!")
except Exception as e:
    print("Error connecting to the database:", e)
    sys.exit(1)  # Exit the script with a non-zero exit code indicating failure

try:
    # dataframe for teams
    men_df = usports_team_stats('men')
    women_df = usports_team_stats('women')

    # datafram for players
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
    men_df.to_sql(name='men_team', con=engine,
                  if_exists='replace', index=False)
    print("Men's team data written to 'men_team' table successfully!")
except Exception as e:
    print("Error writing men's team data to database:", e)

try:
    # Attempt to write women_df DataFrame to SQLite database
    women_df.to_sql(name='women_team', con=engine,
                    if_exists='replace', index=False)
    print("\nWomen's team data written to 'women_team' table successfully!")
except Exception as e:
    print("\nError writing women's team data to database:", e)

try:
    # Attempt to write men_players_df DataFrame to SQLite database
    men_players_df.to_sql(name='men_players', con=engine,
                          if_exists='replace', index=False)
    print("\nMen's players data written to 'men_players' table successfully!")
except Exception as e:
    print("\nError writing men's players data to database:", e)

try:
    # Attempt to write women_players_df DataFrame to SQLite database
    women_players_df.to_sql(name='women_players',
                            con=engine, if_exists='replace', index=False)
    print("\nWomen's players data written to 'women_players' table successfully!")
except Exception as e:
    print("\nError writing women's players data to database:", e)


sql_queries = ["ALTER TABLE men_players ADD COLUMN team_id INTEGER;",
               "UPDATE men_players SET team_id = ( SELECT team_id FROM men_team WHERE men_players.school = men_team.team_name);",
               "ALTER TABLE women_players  ADD COLUMN team_id INTEGER; ",
               " UPDATE women_players SET team_id = (SELECT team_id  FROM women_team WHERE women_players.school = women_team.team_name  ); "]

try:
    # Connect to the database and execute SQL queries
    with engine.connect() as con:
        for idx, query in enumerate(sql_queries, start=1):
            print(f"Executing SQL Query {idx}:")
            con.execute(text(query))
            con.commit()
            print("\nExecuted query:", query.strip(), '\n')
        print("All SQL queries executed successfully. \n")
except Exception as e:
    print("\nAn error occurred while executing SQL queries:", e)


try:
    # CHANGE TO MATCH MYSQL QUERY
    check_table_query = """
    SELECT table_name
    FROM information_schema.tables
    WHERE table_schema = 'usports_bball' 
    AND table_name = 'feedback';
    """

    # Check if the table exists
    result = engine.connect().execute(text(check_table_query))
    table_exists = result.fetchone()

    # If the table does not exist, create it
    if not table_exists:
        create_table_query = """
        CREATE TABLE feedback (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255),
            message TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        engine.connect().execute(text(create_table_query))
        print("Table 'feedback' created successfully.")
    else:
        print("Table 'feedback' already exists.")

    # Close the database connection
    result.close()

except Exception as e:
    print("An error occurred while executing SQL queries for feedback table:", e)
