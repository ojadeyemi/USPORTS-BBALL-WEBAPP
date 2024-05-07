import os
from .database_update import update_usports_bball_db

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Retrieve the environment variable
password = os.getenv("USPORT_BBALL_PASSWORD")

def update_db():
    """ Update Database"""
    update_usports_bball_db(password)
