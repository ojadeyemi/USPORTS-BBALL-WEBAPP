from sqlalchemy import create_engine, text
from sqlalchemy import types as t
import sys

from functions import usports_team_stats, usports_player_stats

connection_string = 'mysql+pymysql://root:Basketball@localhost/usports_bball_test'

# Create a SQLAlchemy engine
engine = create_engine(connection_string)

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



#drop foreign key constraints first
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

