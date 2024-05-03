"""Configurations file"""
import os

mysqldatabase = f"mysql+pymysql://usportsballwebapp:{os.environ.get('USPORT_BBALL_PASSWORD')}.@localhost/usports_bball"
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
