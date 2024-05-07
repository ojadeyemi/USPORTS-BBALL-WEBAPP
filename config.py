"""Configurations file"""
import os

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Retrieve the environment variable
password = os.getenv("USPORT_BBALL_PASSWORD")

mysqldatabase = f"mysql+pymysql://usportsballwebapp:{password}.@localhost/usports_bball"
class Config:
    """Default Configuration"""
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    """Development Configuration"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = mysqldatabase

class ProductionConfig(Config):
    """Production Configuration"""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = mysqldatabase
