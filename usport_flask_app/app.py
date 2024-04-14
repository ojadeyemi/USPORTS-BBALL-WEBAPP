import os
from models import db
from routes import app

#Define the databse URI
mysqldatabase = f"mysql+pymysql://usportsballwebapp:{os.environ.get('USPORT_BBALL_PASSWORD')}.@localhost/usports_bball_test" #ignore
sqlite_database = f"sqlite:///{app.root_path}/../database/usports_bball_test.sqlite"
app.config['SQLALCHEMY_DATABASE_URI'] = sqlite_database


#Initialize the database
db.init_app(app)

if __name__ == "__main__":
    app.run(debug=True, port=5000)