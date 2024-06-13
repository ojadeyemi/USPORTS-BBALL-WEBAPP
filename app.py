"""main app.py"""
from dotenv import load_dotenv
from config import DevelopmentConfig
from usport_flask_app import create_app
from usport_flask_app.models import db
from data_pipeline import update_db

# Load environment variables from .env file
load_dotenv()

app = create_app(config_name=DevelopmentConfig)
db.init_app(app)

@app.cli.command()
def scheduled():
    """Run scheduled job to update database."""
    update_db()

if __name__ == "__main__":
    app.run()
