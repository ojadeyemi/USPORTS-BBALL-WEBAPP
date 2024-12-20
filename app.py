"""main runapp.py"""

from dotenv import load_dotenv

from data_pipeline import update_db
from usport_flask_app import create_app
from usport_flask_app.models import db

# Load environment variables from .env file
load_dotenv()

app = create_app()
db.init_app(app)


@app.cli.command()
def scheduled():
    """Run scheduled job to update database."""
    update_db()


if __name__ == "__main__":
    app.run()
