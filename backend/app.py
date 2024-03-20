from flask import Flask, render_template, request
from models import db, MenTeam, WomenTeam

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Basketball@localhost/usports_bball_test'
db.init_app(app)


@app.route("/")
def index():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route("/mbb")
@app.route("/wbb")
def league():
    if request.path == "/mbb":
        Team = MenTeam
        league_name = "Men's"
    elif request.path == "/wbb":
         Team = WomenTeam
         league_name = "Women's"
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
    return render_template("league.html", teams=teams, league=league_name)


if __name__ == "__main__":
    app.run(debug=True)