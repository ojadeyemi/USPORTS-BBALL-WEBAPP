
import pymysql

from functions import usports_team_data


mens_team = ('https://universitysport.prestosports.com/sports/mbkb/2023-24/teams?sort=&r=0&pos=off', 52)
womens_team = ('https://universitysport.prestosports.com/sports/wbkb/2023-24/teams?sort=&r=0&pos=off', 48)

men_df = usports_team_data(mens_team[0], mens_team[1])
women_df = usports_team_data(womens_team[0], womens_team[1])


#note i have to create the database and tables before I can insert into them
#Connect to MySQL database
connection = pymysql.connect(
    host="localhost",
    user="root",
    password="Basketball", 
    database = 'usports_bball'
)

mycursor = connection.cursor()

column_names = (
    "assists_per_game",
    "blocks_per_game",
    "defensive_efficiency",
    "defensive_rebounds_per_game",
    "field_goal_attempted",
    "field_goal_made",
    "field_goal_percentage",
    "free_throw_percentage",
    "free_throws",
    "free_throws_attempts",
    "free_throws_made",
    "games_played",
    "net_efficiency",
    "offensive_efficiency",
    "offensive_rebounds_per_game",
    "points_per_game",
    "steals_per_game",
    "team_fouls_per_game",
    "3_point_percentage",
    "3_pointers",
    "3_pointers_attempted",
    "3_pointers_made",
    "total_rebounds_per_game",
    "turnovers_per_game",
    'field_goals_against',
    'field_goal_percentage_against',
    '3_points_against',
    '3_point_percentage_against',
    'offensive_rebounds_per_game_against',
    'defensive_rebounds_per_game_against',
    'total_rebounds_per_game_against',
    'assists_per_game_against',
    'turnovers_per_game_against',
    'steals_per_game_against',
    'blocks_per_game_against',
    'team_fouls_per_game_against',
    'points_per_game_against'
)
#column name from dataframe
desired_column_order =['Assists/Game', 'Blocks/Game', 'Defensive Efficiency', 'Defensive Rebounds/Game', 'Field Goal Attempted',
                    'Field Goal Made','Field Goal %','Free Throw %', 'Free Throws', 'Free Throws Attempted', 
                    'Free Throws Made', 'Games Played', 'Net Efficiency', 'Offensive Efficiency', 'Offensive Rebounds/Game', 
                    'Points/Game', 'Steals/Game', 'Team Fouls/Game', '3-point %', '3-points', '3-pointers Attempted', 
                    '3-pointers Made', 'Total Rebounds/Game', 'Turnovers/Game','Field Goals Against', 'Field Goals % Against',
                    '3-points Against', '3-points % Against','Offensive Rebounds/Game Against', 'Defensive Rebounds/Game Against',
                    'Total Rebounds/Game Against', 'Assists/Game Against','Turnovers/Game Against', 'Steals/Game Against',
                    'Blocks/Game Against', 'Team Fouls/Game Against', 'Points/Game Against']







'''
TO UPDATE COLUMNS FORMULA
sqlFormula = f"""
UPDATE mens_team
SET {', '.join([f"{col} = %s" for col in column_names])}
WHERE team_name = %s
"""

for index, row in men_df.iterrows():
    team_name = index
    # Create the data tuple with team_id and remaining data from the DataFrame row
    data_tuple = ([row[df_col] for df_col in desired_column_order])
    
    
    mycursor.execute(sqlFormula, data_tuple + [team_name])
'''

    
