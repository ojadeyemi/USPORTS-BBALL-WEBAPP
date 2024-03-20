from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Basketball@localhost/usports_bball_test'
db = SQLAlchemy(app)


class Team(db.Model):
    __tablename__ = 'men_team_test'
    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(255))
    conference = db.Column(db.String(255))
    last_ten_games = db.Column(db.String(50))
    games_played = db.Column(db.Integer)
    total_wins = db.Column(db.Integer)
    total_losses = db.Column(db.Integer)
    win_percentage = db.Column(db.Float(precision=1))
    streak = db.Column(db.String(50))


@app.route("/")
def index():
    # Query the required columns from the teams table
    teams = Team.query.with_entities(
        Team.team_name,
        Team.last_ten_games,
        Team.conference,
        Team.total_losses,
        Team.total_wins,
        Team.win_percentage,
        Team.streak,
        Team.games_played
    ).order_by(Team.total_wins.desc()).all()
    # Render the index.html template with the retrieved data
    return render_template("index.html", teams=teams)


if __name__ == "__main__":
    app.run(debug=True)