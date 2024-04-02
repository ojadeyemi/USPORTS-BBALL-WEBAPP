"""
USports Basketball Data Processing Script

This script is used to override the old tables with the new table containing the latest data fetched from the USports website. The usports_team_stats and usports_player_stats functions, which are imported from another Python file, are used to parse through the USports website and collect statistics into pandas DataFrame objects.

Dependencies:
- SQLAlchemy: Used for interacting with the MySQL database.
- pandas: Used for data manipulation and processing.
- requests: Used for making HTTP requests to fetch data from the USports website.
- BeautifulSoup (bs4): Used for parsing HTML content fetched from the website.

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
from sqlalchemy import types as t

from functions import usports_team_stats, usports_player_stats

#DO NOT MODIFY UNLESS YOU ARE OJ ADEYEMI
connection_string = 'mysql+pymysql://root:Basketball@localhost/usports_bball_test'

# Create a SQLAlchemy engine
engine = create_engine(connection_string)
engine.connect()
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


#drop foreign key constraints first if table has already been made
sql_query = [
"""
ALTER TABLE women_players_test
DROP foreign key women_players_fk;
""",

"""
ALTER TABLE men_players_test
DROP foreign key men_players_fk;
"""]

with engine.connect() as con:
    for query in sql_query:
        con.execute(text(query))
        con.commit()


team_df_schema = {'team_name': t.NVARCHAR(length=255),
            'conference': t.NVARCHAR(length=50),
            'last_ten_games': t.NVARCHAR(length=50),
            'streak':t.NVARCHAR(length=50)}
player_df_schema = {'lastname_initials':t.NVARCHAR(length = 2),
                    'first_name':t.NVARCHAR(length=255),
                    'school':t.NVARCHAR(length=255)}


# Convert the DataFrame to an SQL table
men_df.to_sql('men_team_test', con=engine, if_exists='replace',index=False,dtype=team_df_schema)
women_df.to_sql('women_team_test', con=engine, if_exists='replace',index=False, dtype=team_df_schema)
men_players_df.to_sql('men_players_test', con=engine, if_exists='replace', index=False,dtype=player_df_schema)
women_players_df.to_sql('women_players_test', con=engine, if_exists='replace', index=False,dtype=player_df_schema)

sql_query = ["""
-- Alter the men_team_test table
ALTER TABLE men_team_test
ADD COLUMN team_id INT AUTO_INCREMENT,
ADD CONSTRAINT PRIMARY KEY (team_id);
""",

"""
-- Alter the women_team_test table
ALTER TABLE women_team_test
ADD COLUMN team_id INT AUTO_INCREMENT,
ADD CONSTRAINT PRIMARY KEY (team_id);
""",

"""
-- Alter the men_players_test table
ALTER TABLE men_players_test
ADD COLUMN player_id INT AUTO_INCREMENT,
ADD CONSTRAINT PRIMARY KEY (player_id),
ADD COLUMN team_id INT,
ADD CONSTRAINT men_players_fk FOREIGN KEY(team_id)
REFERENCES men_team_test(team_id);
""",

"""
-- Alter the women_players_test table
ALTER TABLE women_players_test
ADD COLUMN player_id INT AUTO_INCREMENT,
ADD CONSTRAINT PRIMARY KEY (player_id),
ADD COLUMN team_id INT,
ADD CONSTRAINT women_players_fk FOREIGN KEY(team_id)
REFERENCES women_team_test(team_id);
""",

"""
UPDATE men_players_test
INNER JOIN men_team_test ON men_players_test.school = men_team_test.team_name
SET men_players_test.team_id = men_team_test.team_id
WHERE player_id >= 0;
""",

"""
UPDATE women_players_test
INNER JOIN women_team_test ON women_players_test.school = women_team_test.team_name
SET women_players_test.team_id = women_team_test.team_id
WHERE player_id >= 0;
"""]

with engine.connect() as con:
    for query in sql_query:
        con.execute(text(query))
        con.commit()
        print('something')
    print("success")

