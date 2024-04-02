"""
Models for USports Basketball Data

This file defines SQLAlchemy models representing the database schema used for storing USports basketball data for men's and women's teams and players.

Dependencies:
    - datetime
    - timezone
    - sqlalchemy

Classes:
    - Feedback: Represents feedback data.
    - MenTeam: Represents men's basketball team data.
    - WomenTeam: Represents women's basketball team data.
    - MenPlayers: Represents men's basketball player data.
    - WomenPlayers: Represents women's basketball player data.
"""

from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Float, ForeignKey, DateTime, Text

db = SQLAlchemy()

class Feedback(db.Model):
    __tablename__ = "feedback_test"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(200))
    message: Mapped[str] = mapped_column(Text)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(tz=timezone.utc))

class __BaseTeam(db.Model):
    """ Base class for representing a basketball team. """
    __abstract__ = True
    team_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    team_name: Mapped[str] = mapped_column(String(255), unique=True)
    conference: Mapped[str] = mapped_column(String(10))
    last_ten_games: Mapped[str] = mapped_column(String(50))
    games_played: Mapped[int] = mapped_column(Integer)
    total_wins: Mapped[int] = mapped_column(Integer)
    total_losses: Mapped[int] = mapped_column(Integer)
    win_percentage: Mapped[float] = mapped_column(Float(precision=1))
    streak: Mapped[str] = mapped_column(String(50))
    offensive_efficiency: Mapped[float] = mapped_column(Float(precision=2))
    defensive_efficiency: Mapped[float] = mapped_column(Float(precision=2))

class __BasePlayer(db.Model):
    """ Base class for representing a player in a basketball team. """
    __abstract__ = True
    player_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    team_id: Mapped[int] = mapped_column(Integer, ForeignKey('__BaseTeam.team_id'))
    first_name: Mapped[str] = mapped_column(String(255))
    lastname_initials: Mapped[str] = mapped_column(String(2))
    school: Mapped[str] = mapped_column(String(255))
    games_played: Mapped[int] = mapped_column(Integer)
    games_started: Mapped[int] = mapped_column(Integer)
    minutes_played: Mapped[int] = mapped_column(Integer)
    total_points: Mapped[int] = mapped_column(Integer)
    offensive_rebounds: Mapped[int] = mapped_column(Integer)
    defensive_rebounds: Mapped[int] = mapped_column(Integer)
    total_rebounds: Mapped[int] = mapped_column(Integer)
    personal_fouls: Mapped[int] = mapped_column(Integer)
    disqualifications: Mapped[int] = mapped_column(Integer)
    assists: Mapped[int] = mapped_column(Integer)
    turnovers: Mapped[int] = mapped_column(Integer)
    assist_per_turnover: Mapped[float] = mapped_column(Float)
    steals: Mapped[int] = mapped_column(Integer)
    blocks: Mapped[int] = mapped_column(Integer)
    field_goal_made: Mapped[int] = mapped_column(Integer)
    field_goal_attempted: Mapped[int] = mapped_column(Integer)
    field_goal_percentage: Mapped[float] = mapped_column(Float)
    three_pointers_made: Mapped[int] = mapped_column(Integer)
    three_pointers_attempted: Mapped[int] = mapped_column(Integer)
    three_pointers_percentage: Mapped[float] = mapped_column(Float)
    free_throws_made: Mapped[int] = mapped_column(Integer)
    free_throws_attempted: Mapped[int] = mapped_column(Integer)
    free_throws_percentage: Mapped[float] = mapped_column(Float)


class MenTeam(__BaseTeam):
    """Represents men's basketball team data."""
    __tablename__ = "men_team_test"
    
class WomenTeam(__BaseTeam):
    """Represents women's basketball team data."""
    __tablename__ = "women_team_test"

class MenPlayers(__BasePlayer):
    """Represents men's basketball player data."""
    __tablename__ = "men_players_test"
    

class WomenPlayers(__BasePlayer):
    """Represents women's basketball player data."""
    __tablename__ = "women_players_test"