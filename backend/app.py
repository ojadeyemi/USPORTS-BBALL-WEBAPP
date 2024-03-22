from flask import Flask, render_template, request
from sqlalchemy import func
from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Basketball@localhost/usports_bball_test'
db.init_app(app)


@app.route("/")
def index():
    return render_template("home.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route("/mbb")
@app.route("/wbb")
def league():
    if request.path == "/mbb":
        Team = MenTeam
        Player = MenPlayers
        league_name = "Men's"
    elif request.path == "/wbb":
         Team = WomenTeam
         Player = WomenPlayers
         league_name = "Women's"
    else:
         # Handle invalid paths or other cases
        return render_template("error.html", message="Invalid league")
    
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

    players = Player.query.with_entities(
        Player.lastname_initials,
        Player.first_name,
        Player.school,
        Player.field_goal_attempted,
        func.round(Player.total_points / Player.games_played, 1).label('points_per_game'),
        func.round(Player.total_rebounds / Player.games_played, 1).label('rebounds_per_game'),
        func.round(Player.assists / Player.games_played, 1).label('assists_per_game'),
        func.round((Player.field_goal_made / Player.field_goal_attempted) * 100, 1).label('field_goal_percentage'),
        func.round(Player.three_pointers_made / Player.games_played, 1).label('three_pointers_made_per_game'),
        func.round((Player.three_pointers_made / Player.three_pointers_attempted) * 100, 1).label('three_pointers_percentage'),
         func.round(Player.blocks / Player.games_played, 1).label('blocks_per_game'),
        func.round(Player.steals / Player.games_played, 1).label('steals_per_game')
    ).all()
    

    # Render the index.html template with the retrieved data
    return render_template("league.html", teams=teams, players=players, league=league_name)


if __name__ == "__main__":
    app.run(debug=True)