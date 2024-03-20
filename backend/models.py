
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()




class MenTeam(db.Model):
    __tablename__ = "men_team_test"
    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(255))
    conference = db.Column(db.String(255))
    last_ten_games = db.Column(db.String(50))
    games_played = db.Column(db.Integer)
    total_wins = db.Column(db.Integer)
    total_losses = db.Column(db.Integer)
    win_percentage = db.Column(db.Float(precision=1))
    streak = db.Column(db.String(50))

class WomenTeam(db.Model):
    __tablename__ = "women_team_test"
    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(255))
    conference = db.Column(db.String(255))
    last_ten_games = db.Column(db.String(50))
    games_played = db.Column(db.Integer)
    total_wins = db.Column(db.Integer)
    total_losses = db.Column(db.Integer)
    win_percentage = db.Column(db.Float(precision=1))
    streak = db.Column(db.String(50))

