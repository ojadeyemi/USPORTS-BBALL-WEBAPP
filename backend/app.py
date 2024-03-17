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
    offensive_efficiency = db.Column(db.Integer)
    defensive_efficiency = db.Column(db.Integer)
    net_efficiency = db.Column(db.Integer)


@app.route("/")
def index():
    # Query the required columns from the teams table
    teams = Team.query.with_entities(
        Team.team_name,
        Team.conference,
        Team.last_ten_games,
        Team.offensive_efficiency,
        Team.defensive_efficiency,
        Team.net_efficiency
    ).all()
    # Render the index.html template with the retrieved data
    return render_template("index.html", teams=teams)


if __name__ == "__main__":
    app.run(debug=True)