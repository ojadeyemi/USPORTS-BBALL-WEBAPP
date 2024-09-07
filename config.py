"""Configurations file"""

import os

# Load environment variables from .env file
from dotenv import load_dotenv

load_dotenv()

# Retrieve the environment variable
username = os.getenv("USPORT_BBALL_USERNAME")
password = os.getenv("USPORT_BBALL_PASSWORD")

mysqldatabase = f"mysql+pymysql://{username}:{password}.@localhost/usports_bball"

# SQLite database URL for development
sqlite_database = "sqlite:///{}".format(os.path.abspath("./instance/usports_bball_dev.db"))


class Config:
    """Default Configuration"""

    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    """Development Configuration"""

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = sqlite_database


class ProductionConfig(Config):
    """Production Configuration"""

    DEBUG = False
    SQLALCHEMY_DATABASE_URI = mysqldatabase
