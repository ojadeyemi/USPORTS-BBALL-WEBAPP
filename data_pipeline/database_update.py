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

import logging
import time

from sqlalchemy import create_engine, text, types
from sqlalchemy.exc import SQLAlchemyError
from usports_basketball import usport_players_stats, usport_teams_stats


def update_usports_bball_db(datbase_url: str):
    """
    Updates the usports_bball database with team and player statistics.
    """
    # Configure logging
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    # Determine database type from URL
    if "mysql" in datbase_url:
        db_type = "mysql"
        team_dtypes = {
            "team_name": types.NVARCHAR(length=255),
            "conference": types.NVARCHAR(length=50),
            "streak": types.NVARCHAR(length=50),
            "home": types.NVARCHAR(length=50),  # update to home and away record
            "away": types.NVARCHAR(length=50),
        }
        player_dtypes = {
            "lastname_initials": types.NVARCHAR(length=5),
            "first_name": types.NVARCHAR(length=255),
            "school": types.NVARCHAR(length=50),
        }
    elif "sqlite" in datbase_url:
        db_type = "sqlite"
        # SQLite does not support NVARCHAR with length specification
        team_dtypes = {
            "team_name": types.TEXT,
            "conference": types.TEXT,
        }
        player_dtypes = {
            "lastname_initials": types.TEXT,
            "first_name": types.TEXT,
            "school": types.TEXT,
        }
    else:
        raise ValueError("Unsupported database type in URL")

    try:
        # Create a SQLAlchemy engine
        engine = create_engine(datbase_url)
        with engine.begin() as conn:
            logging.info("Connection successful!")

            try:
                # DataFrame for teams and players
                men_df = usport_teams_stats("men")
                time.sleep(10)
                women_df = usport_teams_stats("women")
                time.sleep(10)
                men_players_df = usport_players_stats("men")
                time.sleep(10)
                women_players_df = usport_players_stats("women")
            except (ImportError, ValueError, TypeError) as e:
                logging.error("Error creating DataFrame: %s", e)
                raise
            except Exception as e:
                logging.error("Unexpected error: %s", e)
                raise

            # Add primary key columns to DataFrames
            men_df["team_id"] = range(1, len(men_df) + 1)
            women_df["team_id"] = range(1, len(men_df) + 1)
            men_players_df["player_id"] = range(1, len(men_players_df) + 1)
            women_players_df["player_id"] = range(1, len(women_players_df) + 1)

            # Write DataFrames to the database
            try:
                men_df.to_sql(name="men_team", con=conn, if_exists="replace", index=False, dtype=team_dtypes)
                logging.info("Men's team data written to 'men_team' table successfully!")
                women_df.to_sql(name="women_team", con=conn, if_exists="replace", index=False, dtype=team_dtypes)
                logging.info("Women's team data written to 'women_team' table successfully!")
                men_players_df.to_sql(name="men_players", con=conn, if_exists="replace", index=False, dtype=player_dtypes)
                logging.info("Men's players data written to 'men_players' table successfully!")
                women_players_df.to_sql(name="women_players", con=conn, if_exists="replace", index=False, dtype=player_dtypes)
                logging.info("Women's players data written to 'women_players' table successfully!")
            except ValueError as e:
                logging.error("Error writing data to database: %s", e)

            # SQL queries
            sql_queries = [
                "ALTER TABLE men_players ADD COLUMN team_id INTEGER;",
                "UPDATE men_players SET team_id = (SELECT team_id FROM men_team WHERE men_players.school = men_team.team_name);",
                "ALTER TABLE women_players ADD COLUMN team_id INTEGER;",
                "UPDATE women_players SET team_id = (SELECT team_id FROM women_team WHERE women_players.school = women_team.team_name);",
            ]

            if db_type == "mysql":
                # MySQL-specific queries
                sql_queries.insert(0, "ALTER TABLE men_players ADD PRIMARY KEY (player_id);")
                sql_queries.insert(1, "ALTER TABLE women_players ADD PRIMARY KEY (player_id);")
                sql_queries.insert(2, "ALTER TABLE men_team ADD PRIMARY KEY (team_id);")
                sql_queries.insert(3, "ALTER TABLE women_team ADD PRIMARY KEY (team_id);")
            else:
                # SQLite does not support `ALTER TABLE ... ADD PRIMARY KEY` for existing columns
                logging.info("SQLite: Primary keys are automatically created with INTEGER columns")

            try:
                # Execute SQL queries
                for idx, query in enumerate(sql_queries, start=1):
                    logging.info("Executing SQL Query %s", idx)
                    conn.execute(text(query))
                    logging.info("Executed query: %s\n", query.strip())
                logging.info("All SQL queries executed successfully. \n")
            except SQLAlchemyError as e:
                logging.error("\nAn error occurred while executing SQL queries: %s", e)

            if db_type == "mysql":
                # MySQL-specific table check and creation
                try:
                    check_table_query = """
                    SELECT table_name
                    FROM information_schema.tables
                    WHERE table_schema = 'usports_bball'
                    AND table_name = 'feedback';
                    """

                    result = conn.execute(text(check_table_query))
                    table_exists = result.fetchone()

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
                except SQLAlchemyError as e:
                    logging.error("An error occurred while executing SQL queries for feedback table: %s", e)
            else:
                logging.info("SQLite: Skipping 'feedback' table creation as it is MySQL-specific.")

    except SQLAlchemyError as e:
        logging.error("An error occurred with the database transaction: %s", e)
