from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Feedback(db.Model):
    __tablename__ = "feedback_test"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    message = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.now(tz=timezone.utc))


class MenTeam(db.Model):
    __tablename__ = "men_team_test"
    team_id = db.Column(db.Integer, primary_key=True)
    players = db.relationship("MenPlayers", back_populates="school_team")
    team_name = db.Column(db.String(255))
    conference = db.Column(db.String(10))
    last_ten_games = db.Column(db.String(50))
    games_played = db.Column(db.Integer)
    total_wins = db.Column(db.Integer)
    total_losses = db.Column(db.Integer)
    win_percentage = db.Column(db.Float(precision=1))
    streak = db.Column(db.String(50))
    offensive_efficiency = db.Column(db.Float(precision=2))
    defensive_efficiency = db.Column(db.Float(precision=2))
    

class WomenTeam(db.Model):
    __tablename__ = "women_team_test"
    team_id = db.Column(db.Integer, primary_key=True)
    players = db.relationship("WomenPlayers", back_populates="school_team")
    team_name = db.Column(db.String(255))
    conference = db.Column(db.String(10))
    last_ten_games = db.Column(db.String(50))
    games_played = db.Column(db.Integer)
    total_wins = db.Column(db.Integer)
    total_losses = db.Column(db.Integer)
    win_percentage = db.Column(db.Float(precision=1))
    streak = db.Column(db.String(50))
    offensive_efficiency = db.Column(db.Float(precision=2))
    defensive_efficiency = db.Column(db.Float(precision=2))

class MenPlayers(db.Model):
    __tablename__ = "men_players_test"
    player_id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('men_team_test.team_id'))
    school_team = db.relationship("MenTeam", back_populates="players")
    first_name = db.Column(db.String(255))
    lastname_initials = db.Column(db.String(2))
    school = db.Column(db.String(255))
    games_played = db.Column(db.Integer)
    games_started = db.Column(db.Integer)
    minutes_played = db.Column(db.Integer)
    total_points = db.Column(db.Integer)
    offensive_rebounds = db.Column(db.Integer)
    defensive_rebounds = db.Column(db.Integer)
    total_rebounds = db.Column(db.Integer)
    personal_fouls = db.Column(db.Integer)
    disqualifications = db.Column(db.Integer)
    assists = db.Column(db.Integer)
    turnovers = db.Column(db.Integer)
    assist_per_turnover = db.Column(db.Float)
    steals = db.Column(db.Integer)
    blocks = db.Column(db.Integer)
    field_goal_made = db.Column(db.Integer)
    field_goal_attempted = db.Column(db.Integer)
    field_goal_percentage = db.Column(db.Float)
    three_pointers_made = db.Column(db.Integer)
    three_pointers_attempted = db.Column(db.Integer)
    three_pointers_percentage = db.Column(db.Float)
    free_throws_made = db.Column(db.Integer)
    free_throws_attempted = db.Column(db.Integer)
    free_throws_percentage = db.Column(db.Float)
    


class WomenPlayers(db.Model):
    __tablename__ = "women_players_test"
    player_id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('women_team_test.team_id'))
    school_team = db.relationship("WomenTeam", back_populates="players")
    first_name = db.Column(db.String(255))
    lastname_initials = db.Column(db.String(2))
    school = db.Column(db.String(255))
    games_played = db.Column(db.Integer)
    games_started = db.Column(db.Integer)
    minutes_played = db.Column(db.Integer)
    total_points = db.Column(db.Integer)
    offensive_rebounds = db.Column(db.Integer)
    defensive_rebounds = db.Column(db.Integer)
    total_rebounds = db.Column(db.Integer)
    personal_fouls = db.Column(db.Integer)
    disqualifications = db.Column(db.Integer)
    assists = db.Column(db.Integer)
    turnovers = db.Column(db.Integer)
    assist_per_turnover = db.Column(db.Float)
    steals = db.Column(db.Integer)
    blocks = db.Column(db.Integer)
    field_goal_made = db.Column(db.Integer)
    field_goal_attempted = db.Column(db.Integer)
    field_goal_percentage = db.Column(db.Float)
    three_pointers_made = db.Column(db.Integer)
    three_pointers_attempted = db.Column(db.Integer)
    three_pointers_percentage = db.Column(db.Float)
    free_throws_made = db.Column(db.Integer)
    free_throws_attempted = db.Column(db.Integer)
    free_throws_percentage = db.Column(db.Float)