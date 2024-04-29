from .models import MenTeam, WomenTeam
from typing import Union

def calculate_categories(team: Union[MenTeam, WomenTeam]):
    """
    "get team and opponet per game stats in order:
    ['Points', 'FG%', 'Threes', '3PT%',  'Rebounds', 'Off Rebounds', 'Assists', 'Steals', 'Blocks', 'Turnovers', 'Fouls']
    """
                      
    # Calculate team per game stats
    points_per_game = round(team.total_points / team.games_played,1)
    field_goal_percentage = team.field_goal_percentage
    three_pointers_made_per_game = round(team.three_pointers_made / team.games_played,1)
    three_point_percentage = team.three_point_percentage
    total_rebounds_per_game = team.total_rebounds_per_game
    offensive_rebounds_per_game = team.offensive_rebounds_per_game
    assists_per_game = team.assists_per_game
    steals_per_game = team.steals_per_game
    blocks_per_game = team.blocks_per_game
    turnovers_per_game = team.turnovers_per_game
    fouls_per_game = team.team_fouls_per_game
    ppp = round(team.offensive_efficiency,2)

    # Calculate opponent per game stats
    points_per_game_against = round(team.total_points_against / team.games_played,1)
    field_goal_percentage_against = team.field_goals_percentage_against
    three_pointers_made_per_game_against = round(team.three_pointers_made_against / team.games_played,1)
    three_point_percentage_against = team.three_points_percentage_against
    total_rebounds_per_game_against = team.total_rebounds_per_game_against
    offensive_rebounds_per_game_against = team.offensive_rebounds_per_game_against
    assists_per_game_against = team.assists_per_game_against
    steals_per_game_against = team.steals_per_game_against
    blocks_per_game_against = team.blocks_per_game_against
    turnovers_per_game_against = team.turnovers_per_game_against
    fouls_per_game_against = team.team_fouls_per_game_against
    ppp_against = round(team.defensive_efficiency,2)

    # Pack the calculated stats into tuples
    team_stats = (points_per_game, field_goal_percentage, three_pointers_made_per_game, 
                  three_point_percentage, total_rebounds_per_game, 
                  offensive_rebounds_per_game, assists_per_game, steals_per_game, 
                  blocks_per_game, turnovers_per_game, fouls_per_game,ppp)
    team_opponent_stats = (points_per_game_against,field_goal_percentage_against, three_pointers_made_per_game_against, 
                           three_point_percentage_against, total_rebounds_per_game_against, 
                           offensive_rebounds_per_game_against, assists_per_game_against, 
                           steals_per_game_against, blocks_per_game_against, 
                           turnovers_per_game_against, fouls_per_game_against,ppp_against)

    return team_stats, team_opponent_stats