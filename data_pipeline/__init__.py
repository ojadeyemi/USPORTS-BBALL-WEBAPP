import os
from dotenv import load_dotenv
from data_pipeline.database_update import update_usports_bball_db
from config import DevelopmentConfig, ProductionConfig

# Load environment variables from .env file
load_dotenv()

# Determine the environment and select the appropriate database URL
environment = os.getenv("FLASK_ENV", "development")

if environment == "production":
    database_url = ProductionConfig.SQLALCHEMY_DATABASE_URI
else:
    database_url = DevelopmentConfig.SQLALCHEMY_DATABASE_URI

def update_db():
    """ Update Database """
    update_usports_bball_db(database_url)