import requests
from bs4 import BeautifulSoup
import pandas as pd

def __usports_player_offense_data(offense_url:str) -> pd.DataFrame:
    """
    Fetches and processes player offense statistics data from the given URL.

    Args:
        offense_url (str): URL of the player offense statistics data.

    Returns:
        pd.DataFrame: DataFrame containing processed player offense statistics.
    """ 
    offense_page = requests.get(offense_url)

    # Parse the HTML using BeautifulSoup
   
    offense_soup = BeautifulSoup(offense_page.content, 'html.parser')

    offense_rows = offense_soup.find_all('tr')

    # Initialize lists to store data
    data = {
        'lastname_initials': [],
        'first_name': [],
        'school': [],
        'minutes_played': [],
        'field_goal_made': [],
        'field_goal_attempted': [],
        'field_goal_percentage': [],
        'three_pointers_made': [],
        'three_pointers_attempted': [],
        'three_pointers_percentage': [],
        'free_throws_made': [],
        'free_throws_attempted': [],
        'free_throws_percentage': [],
        'total_points': [],
    }
    # Iterate through each row
    for row in offense_rows:
        cols = row.find_all('td')  # Find all <td> tags with class 'text'
        if len(cols) > 0:
            player_lastname_initials = cols[1].get_text(strip=True).split()[0]  # Assuming lastname initials are the first letter of the second <td> content
            firstname = ' '.join(cols[1].get_text(strip=True).split()[1:])  # Assuming firstname is the rest of the content after lastname initials
            school = cols[2].get_text(strip=True)
            minutes_played = cols[5].get_text(strip=True)
            field_goals_made, field_goals_attempted = cols[6].get_text(strip=True).split('-')
            field_goal_percentage = cols[7].get_text(strip=True)
            three_points_made,three_points_attempted = cols[8].get_text(strip=True).split('-')
            three_points_percentage = cols[9].get_text(strip=True)
            free_throws_made,free_throws_attempted = cols[10].get_text(strip=True).split('-')
            free_throw_percentage = cols[11].get_text(strip=True)
            total_points = cols[12].get_text(strip=True)

            # Append data to lists
            data['lastname_initials'].append(player_lastname_initials)
            data['first_name'].append(firstname)
            data['school'].append(school)
            data['minutes_played'].append(minutes_played)
            data['field_goal_made'].append(field_goals_made)
            data['field_goal_attempted'].append(field_goals_attempted)
            data['field_goal_percentage'].append(field_goal_percentage)
            data['three_pointers_made'].append(three_points_made)
            data['three_pointers_attempted'].append(three_points_attempted)
            data['three_pointers_percentage'].append(three_points_percentage)
            data['free_throws_made'].append(free_throws_made)
            data['free_throws_attempted'].append(free_throws_attempted)
            data['free_throws_percentage'].append(free_throw_percentage)
            data['total_points'].append(total_points)

    # Create DataFrame
    df = pd.DataFrame(data)
    return df


def __usports_player_defense_data(defense_url:str) -> pd.DataFrame:
    """
    Fetches and processes player offense statistics data from the given URL.

    Args:
        defense_url (str): URL of the player defense statistics data.

    Returns:
        pd.DataFrame: DataFrame containing processed player defense statistics.
    """ 
    defense_page = requests.get(defense_url)

    # Parse the HTML using BeautifulSoup
   
    defense_soup = BeautifulSoup(defense_page.content, 'html.parser')

    # Initialize lists to store data
    data = {
        'lastname_initials': [],
        'first_name': [],
        'school': [],
        'games_played': [],
        'games_started': [],
        'minutes_played': [],
        'offensive_rebounds': [],
        'defensive_rebounds': [],
        'total_rebounds': [],
        'personal_fouls': [],
        'disqualifications': [],
        'assists': [],
        'turnovers': [],
        'assist_per_turnover': [],
        'steals': [],
        'blocks': []
    }

    # Find all <tr> tags
    defense_rows = defense_soup.find_all('tr')

    # Iterate through each row
    for row in defense_rows:
        cols = row.find_all('td')  # Find all <td> tags with class 'text'
        if len(cols) > 0:
            player_lastname_initials = cols[1].get_text(strip=True).split()[0]  # Assuming lastname initials are the first letter of the second <td> content
            firstname = ' '.join(cols[1].get_text(strip=True).split()[1:])  # Assuming firstname is the rest of the content after lastname initials
            school = cols[2].get_text(strip=True)
            games_played = cols[3].get_text(strip=True)
            games_started = cols[4].get_text(strip=True)
            minutes_played = cols[5].get_text(strip=True)
            off_reb = cols[6].get_text(strip=True)
            def_reb = cols[7].get_text(strip=True)
            total_reb = cols[8].get_text(strip=True)
            personal_fouls = cols[9].get_text(strip=True)
            disqualifications = cols[10].get_text(strip=True)
            
            # Assuming the following columns correspond to assist, turnovers, assist/turnover, steals, and blocks
            assists = cols[11].get_text(strip=True)
            turnovers = cols[12].get_text(strip=True)
            assist_turnover = cols[13].get_text(strip=True)
            steals = cols[14].get_text(strip=True)
            blocks = cols[15].get_text(strip=True)
            
            # Append data to lists
            data['lastname_initials'].append(player_lastname_initials)
            data['first_name'].append(firstname)
            data['school'].append(school)
            data['games_played'].append(games_played)
            data['games_started'].append(games_started)
            data['minutes_played'].append(minutes_played)
            data['offensive_rebounds'].append(off_reb)
            data['defensive_rebounds'].append(def_reb)
            data['total_rebounds'].append(total_reb)
            data['personal_fouls'].append(personal_fouls)
            data['disqualifications'].append(disqualifications)
            data['assists'].append(assists)
            data['turnovers'].append(turnovers)
            data['assist_per_turnover'].append(assist_turnover)
            data['steals'].append(steals)
            data['blocks'].append(blocks)

    # Create DataFrame
    df = pd.DataFrame(data)

    return df


def usports_player_stats(arg:str) -> pd.DataFrame:
    """
    Fetches and processes player statistics data from USports website.

    Args:
        arg (str): Gender of the players. Should be either 'men' or 'women'.

    Returns:
        pd.DataFrame: DataFrame containing processed player statistics.
    """
    if(arg == 'men'):
            players_off_stats_df = __usports_player_offense_data('https://universitysport.prestosports.com/sports/mbkb/2023-24/players?view=&pos=st&r=0')
            players_def_stats_df = __usports_player_defense_data('https://universitysport.prestosports.com/sports/mbkb/2023-24/players?view=&pos=bt&r=0')
    elif (arg == 'women'):
        players_off_stats_df = __usports_player_offense_data('https://universitysport.prestosports.com/sports/wbkb/2023-24/players?view=&pos=st&r=0')
        players_def_stats_df = __usports_player_defense_data('https://universitysport.prestosports.com/sports/wbkb/2023-24/players?view=&pos=bt&r=0')

    players_stats_df = pd.merge(players_def_stats_df, players_off_stats_df, on=['lastname_initials','first_name','school', 'minutes_played'], how='inner')
    
    players_stats_df['games_played'] = pd.to_numeric(players_stats_df['games_played'], errors='coerce').fillna(0).astype(int)
    players_stats_df['games_started'] = pd.to_numeric(players_stats_df['games_started'], errors='coerce').fillna(0).astype(int)
    players_stats_df['minutes_played'] = pd.to_numeric(players_stats_df['minutes_played'], errors='coerce').fillna(0).astype(int)
    players_stats_df['offensive_rebounds'] = pd.to_numeric(players_stats_df['offensive_rebounds'], errors='coerce').fillna(0).astype(int)
    players_stats_df['defensive_rebounds'] = pd.to_numeric(players_stats_df['defensive_rebounds'], errors='coerce').fillna(0).astype(int)
    players_stats_df['total_rebounds'] = pd.to_numeric(players_stats_df['total_rebounds'], errors='coerce').fillna(0).astype(int)
    players_stats_df['personal_fouls'] = pd.to_numeric(players_stats_df['personal_fouls'], errors='coerce').fillna(0).astype(int)
    players_stats_df['disqualifications'] = pd.to_numeric(players_stats_df['disqualifications'], errors='coerce').fillna(0).astype(int)
    players_stats_df['assists'] = pd.to_numeric(players_stats_df['assists'], errors='coerce').fillna(0).astype(int)
    players_stats_df['turnovers'] = pd.to_numeric(players_stats_df['turnovers'], errors='coerce').fillna(0).astype(int)
    players_stats_df['assist_per_turnover'] = pd.to_numeric(players_stats_df['assist_per_turnover'], errors='coerce').fillna(0).astype(float)
    players_stats_df['steals'] = pd.to_numeric(players_stats_df['steals'], errors='coerce').fillna(0).astype(int)
    players_stats_df['blocks'] = pd.to_numeric(players_stats_df['blocks'], errors='coerce').fillna(0).astype(int)
    players_stats_df['field_goal_made'] = pd.to_numeric(players_stats_df['field_goal_made'], errors='coerce').fillna(0).astype(int)
    players_stats_df['field_goal_attempted'] = pd.to_numeric(players_stats_df['field_goal_attempted'], errors='coerce').fillna(0).astype(int)
    players_stats_df['field_goal_percentage'] = pd.to_numeric(players_stats_df['field_goal_percentage'], errors='coerce').fillna(0).astype(float)
    players_stats_df['three_pointers_made'] = pd.to_numeric(players_stats_df['three_pointers_made'], errors='coerce').fillna(0).astype(int)
    players_stats_df['three_pointers_attempted'] = pd.to_numeric(players_stats_df['three_pointers_attempted'], errors='coerce').fillna(0).astype(int)
    players_stats_df['three_pointers_percentage'] = pd.to_numeric(players_stats_df['three_pointers_percentage'], errors='coerce').fillna(0).astype(float)
    players_stats_df['free_throws_made'] = pd.to_numeric(players_stats_df['free_throws_made'], errors='coerce').fillna(0).astype(int)
    players_stats_df['free_throws_attempted'] = pd.to_numeric(players_stats_df['free_throws_attempted'], errors='coerce').fillna(0).astype(int)
    players_stats_df['free_throws_percentage'] = pd.to_numeric(players_stats_df['free_throws_percentage'], errors='coerce').fillna(0).astype(float)
    players_stats_df['total_points'] = pd.to_numeric(players_stats_df['total_points'], errors='coerce').fillna(0).astype(int)

    return players_stats_df