#importing libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd

def __usports_team_data(stats_url: str, standings_url: str, no_of_teams: int) -> pd.DataFrame:
    '''
    This function takes the URL of the USport's team stats and the number of teams and returns a
    DataFrame of the team and their stats, removing any rows of teams that didn't play that season.

    Args:
        stats_url (str): URL of the team statistics data.
        standings_url (str): URL of the standings page.
        no_of_teams (int): Number of teams.

    Returns:
        pd.DataFrame: DataFrame containing processed team statistics.
    '''
    #perfrom GET request to the URL and returns the server response to the HTTP request
    page = requests.get(stats_url)
   
    if(page.status_code != 200):
        print("USport's Server did not respond with HTTP request")

    #parse html document
    soup = BeautifulSoup(page.content, 'html.parser')

    #Find the table containing stats
    rows = soup.find_all('tr')
    
    #Intialize lists to store data
    team_names =[]
    games_played = []
    field_goals = []
    field_goal_percentage = []
    three_pointers = []
    three_point_percentage = []
    free_throws = []
    free_throw_percentage = []
    off_rebounds_per_game = []
    def_rebounds_per_game = []
    total_rebounds_per_game = []
    assists_per_game = []
    turnovers_per_game = []
    steals_per_game = []
    blocks_per_game = []
    fouls_per_game = []
    points_per_game = []
    off_efficiency = []
    net_efficiency = []
    field_goals_against = []
    field_goal_against_percentage = []
    three_pointers_against = []
    three_point_against_percentage = []
    off_rebounds_per_game_against = []
    def_rebounds_per_game_against = []
    total_rebounds_per_game_against = []
    assists_per_game_against = []
    turnovers_per_game_against = []
    steals_per_game_against = []
    blocks_per_game_against = []
    fouls_per_game_against = []
    points_per_game_against = []
    def_efficiency = []

    #Loop through each row(skip the first row as it's the header)
    for index, row in enumerate(rows[1:]):

        #exit loop when we reached end of table
        if index >= no_of_teams:
            break

        #Extract team name
        school_name = row.find('td', class_='pinned-col text').text.strip()
   
        team_names.append(school_name)

        #Extract data from other columns
        columns = row.find_all('td', align = 'center')
        games_played.append(columns[0].text.strip())
        field_goals.append(columns[1].text.strip())
        field_goal_percentage.append(columns[2].text.strip())
        three_pointers.append(columns[3].text.strip())
        three_point_percentage.append(columns[4].text.strip())
        free_throws.append(columns[5].text.strip())
        free_throw_percentage.append(columns[6].text.strip())
        off_rebounds_per_game.append(columns[7].text.strip())
        def_rebounds_per_game.append(columns[8].text.strip())
        total_rebounds_per_game.append(columns[9].text.strip())
        assists_per_game.append(columns[10].text.strip())
        turnovers_per_game.append(columns[11].text.strip())
        steals_per_game.append(columns[12].text.strip())
        blocks_per_game.append(columns[13].text.strip())
        fouls_per_game.append(columns[14].text.strip())
        points_per_game.append(columns[15].text.strip())
        off_efficiency.append(columns[16].text.strip())
        net_efficiency.append(columns[17].text.strip())

    #Loop through defensive stats row (skip first row(header) and second row which contains game played)
    for index, row in enumerate(rows[no_of_teams+2:]):
        
        #exit loop when we reached end of table
        if index >= no_of_teams:
            break

        #Extract data from other columns
        columns = row.find_all('td', align = 'center')
        field_goals_against.append(columns[1].text.strip())
        field_goal_against_percentage.append(columns[2].text.strip())
        three_pointers_against.append(columns[3].text.strip())
        three_point_against_percentage.append(columns[4].text.strip())
        off_rebounds_per_game_against.append(columns[5].text.strip())
        def_rebounds_per_game_against.append(columns[6].text.strip())
        total_rebounds_per_game_against.append(columns[7].text.strip())
        assists_per_game_against.append(columns[9].text.strip())
        turnovers_per_game_against.append(columns[10].text.strip())
        steals_per_game_against.append(columns[11].text.strip())
        blocks_per_game_against.append(columns[12].text.strip())
        fouls_per_game_against.append(columns[13].text.strip())
        points_per_game_against.append(columns[14].text.strip())
        def_efficiency.append(columns[15].text.strip())   

    data_collected = {
        'team_name': team_names,
        'games_played': games_played,
        'points_per_game': points_per_game,
        'field_goals': field_goals,
        'field_goal_percentage': field_goal_percentage,
        'three_points': three_pointers,
        'three_point_percentage': three_point_percentage,
        'free_throws': free_throws,
        'free_throw_percentage': free_throw_percentage,
        'offensive_rebounds_per_game': off_rebounds_per_game,
        'defensive_rebounds_per_game': def_rebounds_per_game,
        'total_rebounds_per_game': total_rebounds_per_game,
        'assists_per_game' : assists_per_game,
        'turnovers_per_game': turnovers_per_game,
        'steals_per_game': steals_per_game,
        'blocks_per_game': blocks_per_game,
        'team_fouls_per_game': fouls_per_game,
        'offensive_efficiency': off_efficiency,
        'defensive_efficiency': def_efficiency,
        'Net_efficiency': net_efficiency,
        'field_goals_against': field_goals_against,
        'field_goals_percentage_against': field_goal_against_percentage,
        'three_points_against': three_pointers_against,
        'three_points_percentage_against': three_point_against_percentage,
        'offensive_rebounds_per_game_against': off_rebounds_per_game_against,
        'defensive_rebounds_per_game_against': def_rebounds_per_game_against,
        'total_rebounds_per_game_against': total_rebounds_per_game_against,
        'assists_per_game_against': assists_per_game_against,
        'turnovers_per_game_against': turnovers_per_game_against,
        'steals_per_game_against': steals_per_game_against,
        'blocks_per_game_against': blocks_per_game_against,
        'team_fouls_per_game_against': fouls_per_game_against,
        'points_per_game_against': points_per_game_against
        }
    
    
    #create dictionary that maps university sports team to respective conference
    team_conference = {
    'Acadia': 'AUS',
    'Alberta': 'CW',
    'Algoma': 'OUA West',
    'Bishop\'s': 'RSEQ',
    'Brandon': 'CW',
    'Brock': 'OUA Central',
    'Calgary': 'CW',
    'Cape Breton': 'AUS',
    'Carleton': 'OUA East',
    'Concordia': 'RSEQ',
    'Dalhousie': 'AUS',
    'Guelph': 'OUA West',
    'Lakehead': 'OUA Central',
    'Laurentian': 'OUA East',
    'Laurier': 'OUA West',
    'Laval': 'RSEQ',
    'Lethbridge': 'CW',
    'MacEwan': 'CW',
    'Manitoba': 'CW',
    'McGill': 'RSEQ',
    'McMaster': 'OUA Central',
    'Memorial': 'AUS',
    'Mount Royal': 'CW',
    'Nipissing': 'OUA East',
    'Ontario Tech': 'OUA East',
    'Ottawa': 'OUA East',
    'Queen\'s': 'OUA East',
    'Regina': 'CW',
    'Saint Mary\'s': 'AUS',
    'Saskatchewan': 'CW',
    'StFX': 'AUS',
    'Thompson Rivers': 'CW',
    'Toronto': 'OUA Central',
    'Toronto Metropolitan': 'OUA Central',
    'Trinity Western': 'CW',
    'UBC': 'CW',
    'UBC Okanagan': 'CW',
    'UFV': 'CW',
    'UNB': 'AUS',
    'UNBC': 'CW',
    'UPEI': 'AUS',
    'UQAM': 'RSEQ',
    'Victoria': 'CW',
    'Waterloo': 'OUA West',
    'Western': 'OUA West',
    'Windsor': 'OUA West',
    'Winnipeg': 'CW',
    'York': 'OUA Central'
    }

    #Create a DataFrame
    df = pd.DataFrame(data_collected)

    #remove rows with null vlaues
    df = df[df['games_played'] != '-']

    # Add a new column based on the dictionary
    df['conference'] = df['team_name'].map(team_conference).astype('category')

    #make new columns for fieldgoal_made and fieldgoal taken
    df[['field_goal_made', 'field_goal_attempted']] = df['field_goals'].str.split('-', expand=True).astype(int)
    df[['three_pointers_made', 'three_pointers_attempted']] = df['three_points'].str.split('-', expand=True).astype(int)
    df[['free_throws_made', 'free_throws_attempted']] = df['free_throws'].str.split('-', expand=True).astype(int)
    df[['field_goal_made_against', 'field_goal_attempted_against']] = df['field_goals_against'].str.split('-', expand=True).astype(int)
    df[['three_pointers_made_against', 'three_pointers_attempted_against']] = df['three_points_against'].str.split('-', expand=True).astype(int)
    #delete original field_goal and three point columns
    df.drop(columns=['field_goals','three_points','free_throws','field_goals_against','three_points_against'], inplace=True)

    # Convert columns to their respective data types
    df['games_played'] = df['games_played'].astype(int)
    df['field_goal_percentage'] = df['field_goal_percentage'].astype(float)
    #df['three_points'] = df['three_points'].astype(str)
    df['three_point_percentage'] = df['three_point_percentage'].astype(float)
    #df['free_throws'] = df['free_throws'].astype(str)
    df['free_throw_percentage'] = df['free_throw_percentage'].astype(float)
    df['offensive_rebounds_per_game'] = df['offensive_rebounds_per_game'].astype(float)
    df['defensive_rebounds_per_game'] = df['defensive_rebounds_per_game'].astype(float)
    df['total_rebounds_per_game'] = df['total_rebounds_per_game'].astype(float)
    df['assists_per_game'] = df['assists_per_game'].astype(float)
    df['turnovers_per_game'] = df['turnovers_per_game'].astype(float)
    df['steals_per_game'] = df['steals_per_game'].astype(float)
    df['blocks_per_game'] = df['blocks_per_game'].astype(float)
    df['team_fouls_per_game'] = df['team_fouls_per_game'].astype(float)
    df['points_per_game'] = df['points_per_game'].astype(float)
    #df['field_goals_against'] = df['field_goals_against'].astype(str)
    df['field_goals_percentage_against'] = df['field_goals_percentage_against'].astype(float)
    #df['three_points_against'] = df['three_points_against'].astype(str)
    df['three_points_percentage_against'] = df['three_points_percentage_against'].astype(float)
    df['offensive_rebounds_per_game_against'] = df['offensive_rebounds_per_game_against'].astype(float)
    df['defensive_rebounds_per_game_against'] = df['defensive_rebounds_per_game_against'].astype(float)
    df['total_rebounds_per_game_against'] = df['total_rebounds_per_game_against'].astype(float)
    df['assists_per_game_against'] = df['assists_per_game_against'].astype(float)
    df['turnovers_per_game_against'] = df['turnovers_per_game_against'].astype(float)
    df['steals_per_game_against'] = df['steals_per_game_against'].astype(float)
    df['blocks_per_game_against'] = df['blocks_per_game_against'].astype(float)
    df['team_fouls_per_game_against'] = df['team_fouls_per_game_against'].astype(float)
    df['points_per_game_against'] = df['points_per_game_against'].astype(float)
    try:
        df['offensive_efficiency'] = df['offensive_efficiency'].astype(float)
        df['defensive_efficiency'] = df['defensive_efficiency'].astype(float)
        df['Net_efficiency'] = df['Net_efficiency'].astype(float)
    except:
        print(f"Some team's_efficiency was not recorded")

    #page from second url
    page = requests.get(standings_url)
   
    if(page.status_code != 200):
        print("USport's Server did not respond with HTTP request")

    #parse html document
    soup = BeautifulSoup(page.content, 'html.parser')

    #initialize list to stroe data
    team_names = []
    total_wins = []
    total_losses = []
    win_percentage = []
    last_ten_games = []
    streak = []
    league_points_for = []
    league_points_against = []
    league_points = []

    # Find all <tr> blocks within <table> elements with class="stats-table"
    tr_blocks = soup.select('table.stats-table tr')

    # Iterate through each <tr> block
    for block in tr_blocks:
        # Check if the <tr> block contains a team name (i.e., <a> element)
        team_name_element = block.select_one('td.stats-team a')
        if team_name_element:
            # Extract team name
            team_names.append(team_name_element.text.strip())

            #Extraact other stats
            stats_elements = block.select('td')
            total_wins.append(int(stats_elements[2].text.strip()))
            total_losses.append(int(stats_elements[3].text.strip()))
            win_percentage.append(float(stats_elements[4].text.strip()))
            last_ten_games.append(stats_elements[5].text.strip())
            streak.append(stats_elements[6].text.strip())
            league_points_for.append(int(stats_elements[7].text.strip()))
            league_points_against.append(int(stats_elements[8].text.strip()))
            league_points.append(int(stats_elements[9].text.strip()))
    
    # Assuming last_ten_games contains a list of strings like "Won 3" or "Lost 2"
    modified_streak = []

    for game_result in streak:
        if "Won" in game_result:
            modified_streak.append("W" + game_result[3:])
        elif "Lost" in game_result:
            modified_streak.append("L" + game_result[4:])

    data_collected = {
    'team_name': team_names,
    'total_wins': total_wins,
    'total_losses': total_losses,
    'win_percentage': win_percentage,
    'last_ten_games': last_ten_games,
    'streak' : modified_streak,
    'total_points': league_points_for,
    'total_points_against':league_points_against
}
    #Create a DataFrame
    df2 = pd.DataFrame(data_collected)
    df = pd.merge(df,df2,on='team_name', how='inner')
    return df


def usports_team_stats(arg:str) -> pd.DataFrame:
    """
    Fetches and processes team statistics data from USports website.

    Args:
        arg (str): Gender of the teams. Should be either 'men' or 'women'.

    Returns:
        pd.DataFrame: DataFrame containing processed team statistics.
    """
    if(arg.lower() == 'men'):
        team = ('https://universitysport.prestosports.com/sports/mbkb/2023-24/teams?sort=&r=0&pos=off',
             'https://universitysport.prestosports.com/sports/mbkb/2023-24/standings-conf', 52)
    elif(arg.lower() == 'women'):
        team = ('https://universitysport.prestosports.com/sports/wbkb/2023-24/teams?sort=&r=0&pos=off',
               'https://universitysport.prestosports.com/sports/wbkb/2023-24/standings-conf', 48)
    team_stats_df = __usports_team_data(team[0], team[1], team[2])
    return team_stats_df