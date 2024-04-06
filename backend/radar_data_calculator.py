from sqlalchemy.engine.row import Row
from sqlalchemy import func, ColumnElement
from models import db, MenTeam, WomenTeam
from math import floor
from typing import Union

def normalize(value: Union[int, float], min_value: Union[int, float], max_value: Union[int, float], upper_bound: int = 99) -> int:
    """
    Normalize a value within a range defined by min_value and max_value.
    
    Args:
        value (int or float): The value to normalize.
        min_value (int or float): The minimum value of the range.
        max_value (int or float): The maximum value of the range.
        
    Returns:
        Int: The normalized value.
    """
    #just incase
    if min_value == max_value:
        max_value += 0.1  # Add 0.1 to max_value if min_value and max_value are the same

    # Normalize value to range 60-99
    normalized_value = 60 + ((value - min_value) / (max_value - min_value)) * (upper_bound - 60)
    return floor(normalized_value) #return floor



def find_min_max_values(team_table: Union[type[MenTeam], type[WomenTeam]]) -> Row:
    min_max_values:Row = db.session.query(
    func.min(query_net_efficiency(team_table)).label('min_net_efficiency'),
    func.max(query_net_efficiency(team_table)).label('max_net_efficiency'),
    func.min(query_off_efficiency(team_table)).label('min_offensive_efficiency'),
    func.max(query_off_efficiency(team_table)).label('max_offensive_efficiency'),
    func.min(query_def_efficiency(team_table)).label('min_defensive_efficiency'),
    func.max(query_def_efficiency(team_table)).label('max_defensive_efficiency'),
    func.min(query_playmaking(team_table)).label('min_playmaking'),
    func.max(query_playmaking(team_table)).label('max_playmaking'),
    func.min(query_rebound_margin(team_table)).label('min_rebound_margin'),
    func.max(query_rebound_margin(team_table)).label('max_rebound_margin')
    # Add similar queries for other categories
    ).one()
    return min_max_values

def calculate_radar_data(specific_team_table: Union[type[MenTeam], type[WomenTeam]], min_max_values:Row):
    #Query minimum and maximum valuies from the database
    min_net_efficiency = min_max_values.min_net_efficiency
    max_net_efficiency = min_max_values.max_net_efficiency
    min_offensive_efficiency = min_max_values.min_offensive_efficiency
    max_offensive_efficiency = min_max_values.max_offensive_efficiency
    min_defensive_efficiency = min_max_values.min_defensive_efficiency
    max_defensive_efficiency = min_max_values.max_defensive_efficiency
    min_playmaking = min_max_values.min_playmaking
    max_playmaking = min_max_values.max_playmaking
    min_rebound_margin = min_max_values.min_rebound_margin
    max_rebound_margin = min_max_values.max_rebound_margin
    # Extract min and max values for other categories similarly

    # Get all teams from the provided table
    team_data : list[Union[MenTeam, WomenTeam]] = specific_team_table.query.all()
    
    # Calculate radar chart data for each team
    radar_data: dict[str, list[int]] = {}
    
    for team in team_data:
        overall_efficiency = normalize(query_net_efficiency(team), min_net_efficiency, max_net_efficiency, 98)
        offensive_efficiency = normalize(query_off_efficiency(team), min_offensive_efficiency, max_offensive_efficiency)
        defensive_efficiency = normalize(1/query_def_efficiency(team), 1/max_defensive_efficiency, 1/min_defensive_efficiency)
        playmaking = normalize(query_playmaking(team), min_playmaking, max_playmaking)
        rebound_margin = normalize(query_rebound_margin(team),min_rebound_margin, max_rebound_margin)
        
        

        radar_data[team.team_name] = [overall_efficiency, offensive_efficiency, defensive_efficiency, playmaking, rebound_margin]# Add other categories similarly

                
    return radar_data

def query_net_efficiency(team: Union[MenTeam, WomenTeam]):
        return team.net_efficiency

def query_off_efficiency(team: Union[MenTeam, WomenTeam]):
        return team.offensive_efficiency

def query_def_efficiency(team: Union[MenTeam, WomenTeam]):
        return team.defensive_efficiency

def query_playmaking(team: Union[MenTeam, WomenTeam]):
    if team.turnovers_per_game == 0:
        return team.assists_per_game  # To handle division by zero
    assist_turnover_ratio = team.assists_per_game / team.turnovers_per_game
    return assist_turnover_ratio

def query_rebound_margin(team: Union[MenTeam, WomenTeam]):
     return team.total_rebounds_per_game - team.total_rebounds_per_game_against





