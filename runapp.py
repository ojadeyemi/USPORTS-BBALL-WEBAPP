
from config import DevelopmentConfig, ProductionConfig
from usport_flask_app import create_app
from usport_flask_app.models import db

if __name__ == '__main__':
    app = create_app(config_name=DevelopmentConfig)
    db.init_app(app)
    app.run()
