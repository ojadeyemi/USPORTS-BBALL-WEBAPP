
"""
USports Basketball Statistics Web Scraping and Processing Package

This package provides functions for web scraping and processing basketball statistics data from the USports website. It encompasses functionality for retrieving both team and player statistics.

Dependencies:
    - requests
    - BeautifulSoup (bs4)
    - pandas
    
Functions:
- usports_team_stats: Fetches and processes team statistics data, including standings, win-loss totals, and other relevant team metrics.
- usports_player_stats: Fetches and processes player statistics data, including total games played, total points scored, field goal percentage, and other individual player metrics.

These functions return pandas DataFrames containing the respective statistics data.
Note: This is based on current season only, to get stats from previous season you'll need to manually make changes in both team and players webscraping files

# Example:
>>> from usportsbballstats import usports_team_stats, usports_player_stats
#Fetching and processing men's team and players statistics 
>>> men_team_stats_df = usports_team_stats('men')
# Fetching and processing player statistics data for men's players
>>> men_player_stats_df = usports_player_stats('men') \n

Author:
    OJ Adeyemi

Date Created:
    March 1, 2024
"""
from .team_stats import usports_team_stats
from .player_stats import usports_player_stats

