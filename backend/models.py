
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()




class MenTeam(db.Model):
    __tablename__ = "men_team_test"
    team_id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(255))
    conference = db.Column(db.String(10))
    last_ten_games = db.Column(db.String(50))
    games_played = db.Column(db.Integer)
    total_wins = db.Column(db.Integer)
    total_losses = db.Column(db.Integer)
    win_percentage = db.Column(db.Float(precision=1))
    streak = db.Column(db.String(50))

class WomenTeam(db.Model):
    __tablename__ = "women_team_test"
    team_id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(255))
    conference = db.Column(db.String(10))
    last_ten_games = db.Column(db.String(50))
    games_played = db.Column(db.Integer)
    total_wins = db.Column(db.Integer)
    total_losses = db.Column(db.Integer)
    win_percentage = db.Column(db.Float(precision=1))
    streak = db.Column(db.String(50))

class MenPlayers(db.Model):
    __tablename__ = "men_players_test"
    player_id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('men_team_test.team_id'))
    first_name = db.Column(db.String(255))
    last_name_initials = db.Column(db.String(2))
    school = db.Column(db.String(255))