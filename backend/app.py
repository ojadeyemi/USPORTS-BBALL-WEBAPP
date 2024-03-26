from flask import Flask, render_template, request, redirect
from sqlalchemy import func
from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Basketball@localhost/usports_bball_test'

db.init_app(app)
mydict = {} #figure out how to use this dict and store in database

@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == 'POST':
        name = request.form['name']
        message = request.form['message']
        mydict[name] = message
        print(mydict)
        return redirect("/")
    else:
        return render_template("home.html")



@app.route('/about')
def about():
    return render_template("about.html")

@app.route("/<league_path>")
def league(league_path):
    if league_path == "mbb":
        Team = MenTeam
        Player = MenPlayers
        league_name = "Men's"
    elif league_path == "wbb":
         Team = WomenTeam
         Player = WomenPlayers
         league_name = "Women's"
    else:
         # Handle invalid paths or other cases
        return render_template("error.html", message="Invalid league")
    
    # Query the required columns from the teams table
    teams = Team.query.with_entities(
        Team.team_id,
        Team.team_name,
        Team.last_ten_games,
        Team.conference,
        Team.total_losses,
        Team.total_wins,
        Team.win_percentage,
        Team.streak,
        Team.games_played,
        func.round(Team.offensive_efficiency * 100,1).label('offensive_efficiency'),
        func.round(Team.defensive_efficiency * 100,1).label('defensive_efficiency'),
    ).order_by(Team.total_wins.desc()).all()

    players = Player.query.with_entities(
        Player.lastname_initials,
        Player.first_name,
        Player.school,
        Player.games_played,
        Player.field_goal_attempted,
        Player.three_pointers_attempted,
        Player.field_goal_percentage,
        Player.three_pointers_percentage,
        Player.free_throws_percentage,
        Player.team_id,
        Team.games_played.label("team_games_played"),
        Team.conference.label("team_conference"),
        func.round(Player.total_points / Player.games_played, 1).label('points_per_game'),
        func.round(Player.total_rebounds / Player.games_played, 1).label('rebounds_per_game'),
        func.round(Player.assists / Player.games_played, 1).label('assists_per_game'),
        func.round(Player.three_pointers_made / Player.games_played, 1).label('three_pointers_made_per_game'),
        func.round(Player.free_throws_made / Player.games_played, 1).label('free_throws_made_per_game'),
         func.round(Player.blocks / Player.games_played, 1).label('blocks_per_game'),
        func.round(Player.steals / Player.games_played, 1).label('steals_per_game'),
        func.round(Player.field_goal_made / Player.games_played, 1).label('field_goal_made_per_game')
    ).outerjoin(
    Team, Player.team_id == Team.team_id
).all()
    
    # Render the league.html template with the retrieved data
    return render_template("league.html", teams=teams, players=players, league=league_name, league_path=league_path)

@app.route("/<league_path>/<team_path>")
def team_page(league_path,team_path):
    if league_path == "mbb":
        league_name = "Men's"
        team = MenTeam.query.filter_by(team_name=team_path).first()
        players = MenPlayers.query.filter_by(team_id=team.team_id).all()
        return render_template("team.html", team=team, players=players, league=league_name, league_path=league_path)
    
    elif league_path == "wbb":
        league_name = "Women's"
        team = WomenTeam.query.filter_by(team_name=team_path).first()
        players = WomenPlayers.query.filter_by(team_id=team.team_id).all()
        return render_template("team.html", team=team, players=players, league=league_name, league_path=league_path)
    else:
         # Handle invalid paths or other cases
        return render_template("error.html", message="Invalid team")
    



if __name__ == "__main__":
    app.run(debug=True, port=5000)
    print(mydict)