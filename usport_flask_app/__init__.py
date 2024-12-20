"""U Sport web app with routes"""
from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import func, cast, Numeric
from sqlalchemy.exc import SQLAlchemyError
from config import DevelopmentConfig, ProductionConfig
from .models import db, Feedback, MenTeam, WomenTeam, MenPlayers, WomenPlayers
from .radar_data_calculator import calculate_radar_data, find_min_max_values
from .team_stats_calulator import calculate_categories



def create_app(config_name=ProductionConfig):
    """Create flask app instance"""
    app = Flask(__name__)

    app.config.from_object(config_name)

    @app.route('/health')
    def healthcheck():
        """
        Endpoint for health checks.

        Returns:
            dict: A JSON response indicating the application's health status.
        """
        return {'status': 'healthy'}

    # Define the route for the index page(home page)
    @app.route("/", methods=["POST", "GET"])
    def index():
        if request.method == 'POST':
            # Handle form submission
            name = request.form['name']
            email = request.form['email']
            message = request.form['message']
            # Create an instance of the Feedback model
            feedback_entry = Feedback(name=name[:200], email=email, message=message)
            # Add the instance to the database session
            db.session.add(feedback_entry)
            try:
                # Commit the changes to the database
                db.session.commit()
            except SQLAlchemyError as e:
                # Rollback the transaction in case of error
                db.session.rollback()
                print("Error adding feedback entry:", str(e))
            # Redirect to the index page after form submission
            return redirect("/")
        # Render the home.html template for GET requests
        return render_template("index.html")


    # Define the route for the about page
    @app.route('/about')
    def about():
        return render_template("about.html")

    # Define the route for the league page
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
        
        fallback_player_portrait_url = url_for('static', filename='player_photos/default_portrait.png') 
        # Query the required columns from the teams table
        teams = Team.query.with_entities(
            Team.team_id,
            Team.team_name,
            Team.last_ten_games,
            Team.conference,
            Team.total_losses,
            Team.total_wins,
            cast(Team.win_percentage, Numeric(10, 2)).label('win_percentage'),
            Team.streak,
            Team.games_played,
            cast(Team.offensive_efficiency, Numeric(10, 3)).label('offensive_efficiency'),
            cast(Team.defensive_efficiency, Numeric(10, 3)).label('defensive_efficiency')
        ).order_by(Team.win_percentage.desc()).all()
        
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
            Team.games_played.label("team_games_played"),
            Team.conference.label("team_conference"),
            func.round(Player.total_points / Player.games_played, 4).label('points_per_game'),
            func.round(Player.total_rebounds / Player.games_played, 4).label('rebounds_per_game'),
            func.round(Player.assists / Player.games_played, 4).label('assists_per_game'),
            func.round(Player.three_pointers_made / Player.games_played, 4).label('three_pointers_made_per_game'),
            func.round(Player.free_throws_made / Player.games_played, 4).label('free_throws_made_per_game'),
            (func.round(Player.blocks / Player.games_played, 4)).label('blocks_per_game'),
            func.round(Player.steals / Player.games_played, 4).label('steals_per_game'),
            func.round(Player.field_goal_made / Player.games_played, 4).label('field_goal_made_per_game')
        ).outerjoin(
        Team, Player.team_id == Team.team_id
    ).all()
        
        radar_data = calculate_radar_data(Team,find_min_max_values(Team)) # type: ignore
        
        # Render the league.html template with the retrieved data
        return render_template("league.html", teams=teams, players=players, league=league_name, league_path=league_path, 
                               fallback_player_portrait_url=fallback_player_portrait_url, radar_data=radar_data)

    # Define the route for the team page
    @app.route("/<league_path>/<team_path>")
    def team_page(league_path: str,team_path: str):
        if league_path == "mbb":
            league_name = "Men's"
            team = MenTeam
            players = MenPlayers   
        elif league_path == "wbb":
            league_name = "Women's"
            team = WomenTeam
            players = WomenPlayers  
        else:
            # Handle invalid paths or other cases
            return render_template("error.html", message="Invalid team")
        
        team = team.query.filter_by(team_name=team_path).one()
        players = players.query.filter_by(team_id=team.team_id).all()
        fallback_player_portrait_url = url_for('static', filename='img/player_photos/default_portrait.png') 
        categories = ["Points", "FG%", "Threes", "3PT%", "Rebounds", "Off Rebounds",
                       "Assists", "Steals", "Blocks", "Turnovers", "Fouls", "PointsPerPossession"]
        team_stats,opponent_stats = calculate_categories(team)
        return render_template("team.html", team=team, players=players, league=league_name, league_path=league_path, 
                            fallback_player_portrait_url=fallback_player_portrait_url, teamstats=team_stats, 
                            opponentstats=opponent_stats, categories=categories)
    return app
#PASS TEAM AND OPPONENT VALUES AS TEAM AND OPPONENT STAS WITH THE CATEGORIES 
    #define error routes seperately
