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
import logging
from sqlalchemy import create_engine, text, types
from sqlalchemy.exc import SQLAlchemyError
from usports_basketball import usports_team_stats, usports_player_stats


def update_usports_bball_db(mysql_password: str):
    # Configure logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    team_dtypes = {'team_name':types.NVARCHAR(length=255), 'conference':types.NVARCHAR(length=50),
                   'last_ten_games':types.NVARCHAR(length=50), 'streak':types.NVARCHAR(length=50)}
    player_dtypes={'lastname_initials':types.NVARCHAR(length=5), 'first_name':types.NVARCHAR(length=255),
                    'school':types.NVARCHAR(length=50)}

    mysqldatabase = f"mysql+pymysql://root:{mysql_password}@localhost/usports_bball"

    try:
        # Create a SQLAlchemy engine
        engine = create_engine(mysqldatabase)
        with engine.begin() as conn:
            logging.info("Connection successful!")

            try:
                # dataframe for teams
                men_df = usports_team_stats('men')
                women_df = usports_team_stats('women')

                # datafram for players
                men_players_df = usports_player_stats('men')
                women_players_df = usports_player_stats('women')
            except (ImportError, ValueError, TypeError) as e:
                # Handle specific types of errors
                logging.error("Error creating DataFrame: %s", e)
                raise
            except Exception as e:
                # Handle any other unexpected errors
                logging.error("Unexpected error: %s", e)
                raise

            # Convert the DataFrame to an SQL table
            # Add a primary key column to the DataFrame
            men_df['team_id'] = range(1, len(men_df) + 1)
            women_df['team_id'] = range(1, len(men_df) + 1)
            men_players_df['player_id'] = range(1, len(men_players_df) + 1)
            women_players_df['player_id'] = range(1, len(women_players_df) + 1)

            try:
                # Attempt to write men_df DataFrame to SQLite database
                men_df.to_sql(name='men_team', con=conn, if_exists='replace', 
                              index=False,dtype=team_dtypes)
                logging.info("Men's team data written to 'men_team' table successfully!")
            except Exception as e:
                logging.error("Error writing men's team data to database: %s", e)

            try:
                # Attempt to write women_df DataFrame to SQLite database
                women_df.to_sql(name='women_team', con=conn, if_exists='replace', 
                                index=False,dtype=team_dtypes)
                logging.info("Women's team data written to 'women_team' table successfully!")
            except Exception as e:
                logging.error("Error writing women's team data to database: %s", e)

            try:
                # Attempt to write men_players_df DataFrame to SQLite database
                men_players_df.to_sql(name='men_players', con=conn,if_exists='replace', 
                                      index=False,dtype=player_dtypes)
                logging.info("Men's players data written to 'men_players' table successfully!")
            except Exception as e:
                logging.error("Error writing men's players data to database: %s", e)

            try:
                # Attempt to write women_players_df DataFrame to SQLite database
                women_players_df.to_sql(name='women_players', con=conn, if_exists='replace', 
                                        index=False, dtype=player_dtypes)
                logging.info("Women's players data written to 'women_players' table successfully!")
            except Exception as e:
                logging.error("Error writing women's players data to database: %s", e)

            sql_queries = [
                "ALTER TABLE men_players ADD PRIMARY KEY (player_id);",
                "ALTER TABLE women_players ADD PRIMARY KEY (player_id);",
                "ALTER TABLE men_team ADD PRIMARY KEY (team_id);",
                "ALTER TABLE women_team ADD PRIMARY KEY (team_id);",
                "ALTER TABLE men_players ADD COLUMN team_id INTEGER;",
                "UPDATE men_players SET team_id = ( SELECT team_id FROM men_team WHERE men_players.school = men_team.team_name);",
                "ALTER TABLE women_players  ADD COLUMN team_id INTEGER; ",
                "UPDATE women_players SET team_id = (SELECT team_id  FROM women_team WHERE women_players.school = women_team.team_name  );"
            ]

            try:
                # Execute SQL queries
                for idx, query in enumerate(sql_queries, start=1):
                    logging.info(f"Executing SQL Query {idx}:")
                    conn.execute(text(query))
                    logging.info("Executed query: %s\n", query.strip())
                logging.info("All SQL queries executed successfully. \n")
            except SQLAlchemyError as e:
                logging.error("\nAn error occurred while executing SQL queries: %s", e)

            try:
                # CHANGE TO MATCH MYSQL QUERY
                check_table_query = """
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'usports_bball' 
                AND table_name = 'feedback';
                """

                # Check if the table exists
                result = conn.execute(text(check_table_query))
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
                    conn.execute(text(create_table_query))
                    logging.info("Table 'feedback' created successfully.")
                else:
                    logging.info("Table 'feedback' already exists.")

                # Close the database connection
                result.close()

            except SQLAlchemyError as e:
                logging.error("An error occurred while executing SQL queries for feedback table: %s", e)

    except SQLAlchemyError as e:
        logging.error("An error occurred with the database transaction: %s", e)

# Example usage:
if __name__ == "__main__":
    mysql_password = os.environ.get('USPORT_BBALL_PASSWORD')
    update_usports_bball_db(mysql_password)
