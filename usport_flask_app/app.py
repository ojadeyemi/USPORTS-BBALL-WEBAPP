import os
from models import db
from routes import app

# Define the databse URI
# ignore
mysqldatabase = f"mysql+pymysql://usportsballwebapp:{os.environ.get('USPORT_BBALL_PASSWORD')}.@localhost/usports_bball"
app.config['SQLALCHEMY_DATABASE_URI'] = mysqldatabase


# Initialize the database
db.init_app(app)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
