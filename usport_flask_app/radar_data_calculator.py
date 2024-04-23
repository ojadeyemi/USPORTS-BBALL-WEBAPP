"""
This module contains functions for calculating and normalizing basketball statistics used in the USPORTS BASKETBALL WEB APP.

Functions:
    - normalize: Normalize a value within a specified range.
    - find_min_max_values: Find the minimum and maximum values for various statistics across teams.
    - calculate_radar_data: Calculate radar chart data for teams based on their statistics.
"""
from sqlalchemy.engine.row import Row
from sqlalchemy import func
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
        max_value += 0.01  # Add 0.01 to max_value if min_value and max_value are the same

    # Normalize value to range 60-99
    normalized_value = 50 + ((value - min_value) / (max_value - min_value)) * (upper_bound - 50)
    return floor(normalized_value) #return floor


def find_min_max_values(team_table: Union[MenTeam, WomenTeam]) -> Row:
    """
    Find the minimum and maximum values for various statistics across teams.

    Args:
        team_table (Union[type[MenTeam], type[WomenTeam]]): The table of teams.

    Returns:
        Row: A row containing the minimum and maximum values for various statistics.
    """
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
    func.max(query_rebound_margin(team_table)).label('max_rebound_margin'),
    func.min(query_effective_fg_percentage(team_table)).label('min_EFG'),
    func.max(query_effective_fg_percentage(team_table)).label('max_EFG'),
     func.min(query_3pt_shooting_efficiency(team_table)).label('min_3pt_rating'),
    func.max(query_3pt_shooting_efficiency(team_table)).label('max_3pt_rating')
    # Add similar queries for other categories
    ).one()
    return min_max_values

def calculate_radar_data(specific_team_table: Union[MenTeam, WomenTeam], min_max_values:Row):
    """
    Calculate radar chart data for teams based on their statistics.

    Args:
        specific_team_table (Union[type[MenTeam], type[WomenTeam]]): The specific table of teams.
        min_max_values (Row): The minimum and maximum values for various statistics.

    Returns:
        dict[str, list[int]]: Radar chart data for each team.
    """
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
    min_effective_fg_percentage = min_max_values.min_EFG
    max_effective_fg_percentage = min_max_values.max_EFG
    min_3pt_rating = min_max_values.min_3pt_rating
    max_3pt_rating = min_max_values.max_3pt_rating    
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
        EFG_percentage = normalize(query_effective_fg_percentage(team), min_effective_fg_percentage, max_effective_fg_percentage)
        three_point_rating = normalize(query_3pt_shooting_efficiency(team), min_3pt_rating, max_3pt_rating, 98)
        
        
        #order of array should match labels in javascript charjs label
        radar_data[team.team_name] = [overall_efficiency, defensive_efficiency, playmaking, rebound_margin, three_point_rating, EFG_percentage, offensive_efficiency]
          
    return radar_data


def query_net_efficiency(team: Union[MenTeam, WomenTeam]):
    """
    Retrieves the net efficiency of a team.

    Args:
        team (Union[MenTeam, WomenTeam]): The team for which to retrieve the net efficiency.

    Returns:
        float: The net efficiency of the team.
    """
    return team.net_efficiency


def query_off_efficiency(team: Union[MenTeam, WomenTeam]):
    """
    Retrieves the offensive efficiency of a team.

    Args:
        team (Union[MenTeam, WomenTeam]): The team for which to retrieve the offensive efficiency.

    Returns:
        float: The offensive efficiency of the team.
    """
    return team.offensive_efficiency


def query_def_efficiency(team: Union[MenTeam, WomenTeam]):
    """
    Retrieves the defensive efficiency of a team.

    Args:
        team (Union[MenTeam, WomenTeam]): The team for which to retrieve the defensive efficiency.

    Returns:
        float: The defensive efficiency of the team.
    """
    return team.defensive_efficiency


def query_playmaking(team: Union[MenTeam, WomenTeam]):
    """
    Calculates the playmaking efficiency of a team.

    Args:
        team (Union[MenTeam, WomenTeam]): The team for which to calculate the playmaking efficiency.

    Returns:
        float: The playmaking efficiency of the team.
    """
    if team.turnovers_per_game == 0:
        return team.assists_per_game  # To handle division by zero
    assist_turnover_ratio = team.assists_per_game / team.turnovers_per_game
    return assist_turnover_ratio


def query_rebound_margin(team: Union[MenTeam, WomenTeam]):
    """
    Retrieves the rebound margin of a team.

    Args:
        team (Union[MenTeam, WomenTeam]): The team for which to retrieve the rebound margin.

    Returns:
        float: The rebound margin of the team.
    """
    return team.total_rebounds_per_game - team.total_rebounds_per_game_against


def query_effective_fg_percentage(team: Union[MenTeam, WomenTeam]):
    """
    Calculates the effective field goal percentage of a team.

    Args:
        team (Union[MenTeam, WomenTeam]): The team for which to calculate the effective field goal percentage.

    Returns:
        float: The effective field goal percentage of the team.
    """
    efg = (team.field_goal_made + (0.5 * team.three_pointers_made)) / team.field_goal_attempted
    return efg


def query_3pt_shooting_efficiency(team: Union[MenTeam, WomenTeam]):
    """
    Calculates the 3-point shooting efficiency of a team.

    Args:
        team (Union[MenTeam, WomenTeam]): The team for which to calculate the 3-point shooting efficiency.

    Returns:
        float: The 3-point shooting efficiency of the team.
    """
    # Calculate the team's 3-point attempts per game
    three_point_attempts_per_game = team.three_pointers_attempted / team.games_played
    
    # Calculate the team's 3-point shooting efficiency
    three_point_efficiency = (0.9 * team.three_point_percentage) + (0.1 * three_point_attempts_per_game)
    
    return three_point_efficiency