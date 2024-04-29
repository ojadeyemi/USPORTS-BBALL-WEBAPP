import os
from .database_update import update_usports_bball_db

def update_db():
    """ Update Database"""
    mysql_password = os.environ.get('USPORT_BBALL_PASSWORD')
    update_usports_bball_db(mysql_password)
