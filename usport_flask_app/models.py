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
from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

db = SQLAlchemy()


class Feedback(db.Model):
    """Class for representing feedback table"""

    __tablename__ = "feedback"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(200))
    email: Mapped[str] = mapped_column(String(200))
    message: Mapped[str] = mapped_column(Text)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(tz=timezone.utc))

    def __init__(self, name: str, email: str, message: str):
        self.name = name
        self.email = email
        self.message = message


class __BaseTeam(db.Model):
    """Base class for representing a basketball team."""

    __abstract__ = True
    team_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    team_name: Mapped[str] = mapped_column(String(255), unique=True)
    conference: Mapped[str] = mapped_column(String(50))
    games_played: Mapped[int] = mapped_column(Integer)
    total_wins: Mapped[int] = mapped_column(Integer)
    total_losses: Mapped[int] = mapped_column(Integer)
    win_percentage: Mapped[float] = mapped_column(Float(precision=2))
    offensive_efficiency: Mapped[float] = mapped_column(Float(precision=2))
    defensive_efficiency: Mapped[float] = mapped_column(Float(precision=2))
    net_efficiency: Mapped[float] = mapped_column(Float(precision=2))
    points_per_game: Mapped[float] = mapped_column(Float(precision=2))
    field_goal_percentage: Mapped[float] = mapped_column(Float)
    three_point_percentage: Mapped[float] = mapped_column(Float)
    free_throw_percentage: Mapped[float] = mapped_column(Float)
    offensive_rebounds_per_game: Mapped[float] = mapped_column(Float)
    defensive_rebounds_per_game: Mapped[float] = mapped_column(Float)
    total_rebounds_per_game: Mapped[float] = mapped_column(Float)
    assists_per_game: Mapped[float] = mapped_column(Float)
    turnovers_per_game: Mapped[float] = mapped_column(Float)
    steals_per_game: Mapped[float] = mapped_column(Float)
    blocks_per_game: Mapped[float] = mapped_column(Float)
    team_fouls_per_game: Mapped[float] = mapped_column(Float)
    field_goal_percentage_against: Mapped[float] = mapped_column(Float)
    three_point_percentage_against: Mapped[float] = mapped_column(Float)
    offensive_rebounds_per_game_against: Mapped[float] = mapped_column(Float)
    defensive_rebounds_per_game_against: Mapped[float] = mapped_column(Float)
    total_rebounds_per_game_against: Mapped[float] = mapped_column(Float)
    assists_per_game_against: Mapped[float] = mapped_column(Float)
    turnovers_per_game_against: Mapped[float] = mapped_column(Float)
    steals_per_game_against: Mapped[float] = mapped_column(Float)
    blocks_per_game_against: Mapped[float] = mapped_column(Float)
    team_fouls_per_game_against: Mapped[float] = mapped_column(Float)
    points_per_game_against: Mapped[float] = mapped_column(Float)
    field_goal_made: Mapped[int] = mapped_column(Integer)
    field_goal_attempted: Mapped[int] = mapped_column(Integer)
    three_pointers_made: Mapped[int] = mapped_column(Integer)
    three_pointers_attempted: Mapped[int] = mapped_column(Integer)
    free_throws_made: Mapped[int] = mapped_column(Integer)
    free_throws_attempted: Mapped[int] = mapped_column(Integer)
    field_goal_made_against: Mapped[int] = mapped_column(Integer)
    field_goal_attempted_against: Mapped[int] = mapped_column(Integer)
    three_pointers_made_against: Mapped[int] = mapped_column(Integer)
    three_pointers_attempted_against: Mapped[int] = mapped_column(Integer)
    total_points: Mapped[int] = mapped_column(Integer)
    total_points_against: Mapped[int] = mapped_column(Integer)

    def __repr__(self):
        return f"<Team(id={self.team_id}, team_name='{self.team_name}', conference='{self.conference})>"


class __BasePlayer(db.Model):
    """Base class for representing a player in a basketball team."""

    __abstract__ = True
    player_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    team_id: Mapped[int] = mapped_column(Integer, ForeignKey("__BaseTeam.team_id"))
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
    assist_to_turnover_ratio: Mapped[float] = mapped_column(Float)
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

    def __repr__(self):
        return (
            f"<Player(lastname_initials='{self.lastname_initials},first_name='{self.first_name}',"
            f"school='{self.school}', player_id={self.player_id}, team_id={self.team_id})>"
        )


class MenTeam(__BaseTeam):
    """Represents men's basketball team data."""

    __tablename__ = "men_team"


class WomenTeam(__BaseTeam):
    """Represents women's basketball team data."""

    __tablename__ = "women_team"


class MenPlayers(__BasePlayer):
    """Represents men's basketball player data."""

    __tablename__ = "men_players"


class WomenPlayers(__BasePlayer):
    """Represents women's basketball player data."""

    __tablename__ = "women_players"
