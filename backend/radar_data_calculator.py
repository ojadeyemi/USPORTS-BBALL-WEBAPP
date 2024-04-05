from models import db, MenTeam
from math import floor
from typing import Union

def normalize(value: Union[int, float], min_value: Union[int, float], max_value: Union[int, float]) -> int:
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
    normalized_value = 50 + ((value - min_value) / (max_value - min_value)) * 49
    return floor(normalized_value)

def find_min_max_values(team_table):
    min_max_values = db.session.query(
    db.func.min(team_table.net_efficiency).label('min_net_efficiency'),
    db.func.max(team_table.net_efficiency).label('max_net_efficiency'),
    db.func.min(team_table.offensive_efficiency).label('min_offensive_efficiency'),
    db.func.max(team_table.offensive_efficiency).label('max_offensive_efficiency'),
    db.func.min(team_table.defensive_efficiency).label('min_defensive_efficiency'),
    db.func.max(team_table.defensive_efficiency).label('max_defensive_efficiency')
    # Add similar queries for other categories
    ).one()
    return min_max_values

def calculate_radar_data(specific_team_table, min_max_values):
    #Query minimum and maximum valuies from the database

     
    min_net_efficiency = min_max_values.min_net_efficiency
    max_net_efficiency = min_max_values.max_net_efficiency
    min_offensive_efficiency = min_max_values.min_offensive_efficiency
    max_offensive_efficiency = min_max_values.max_offensive_efficiency
    min_defensive_efficiency = min_max_values.min_defensive_efficiency
    max_defensive_efficiency = min_max_values.max_defensive_efficiency
    # Extract min and max values for other categories similarly

    # Get all teams from the provided table
    team_data = specific_team_table.query.all()

    # Calculate radar chart data for each team
    radar_data = {}

    for team in team_data:
        
        overall_efficiency = normalize(team.net_efficiency, min_net_efficiency, max_net_efficiency)
        offensive_efficiency = normalize(team.offensive_efficiency, min_offensive_efficiency, max_offensive_efficiency)
        defensive_efficiency = normalize(1/team.defensive_efficiency, 1/max_defensive_efficiency, 1/min_defensive_efficiency)
        
        

        radar_data[team.team_name] = [overall_efficiency,offensive_efficiency,defensive_efficiency]# Add other categories similarly

                
    return radar_data







