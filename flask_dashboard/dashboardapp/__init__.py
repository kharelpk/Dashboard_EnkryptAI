# import necessay files
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from dashboardapp.config import Config



# Create the database
db=SQLAlchemy()
# Password manager
bcrypt = Bcrypt()
# Login manager
login_manager = LoginManager()
# Set the login route (function name of the route)
login_manager.login_view = 'login'
# Blue info alert from bootstrap
login_manager.login_message_category='info'


# Graph types
CHART_OPTIONS = ['HISTOGRAM', 'PIE CHART', 'BAR CHART']
ADMIN_EMAIL = 'admin@admin.com'



def create_app(config_class = Config):
    # statement to create flask app
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    # Password manager
    bcrypt.init_app(app)
    # Login manager
    login_manager.init_app(app)

    from dashboardapp.users.routes import users
    from dashboardapp.main.routes import main
    app.register_blueprint(users)
    app.register_blueprint(main)

    return app



