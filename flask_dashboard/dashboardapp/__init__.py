# import necessay files
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os



# statement to create flask app
app = Flask(__name__)
# The session key is in the environment variable
app.config['SECRET_KEY']='93c34a429a3473ca9cbd70ab5c6b931a'
# Setup the database (two seperates ones for data and keys)
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///site.db'

app.config['SQLALCHEMY_BINDS']= {
    'keys':'sqlite:///keys.db'}
# Upload extensions for datasets
app.config['UPLOAD_EXTENSIONS'] = ['.db', '.csv']
# Create the database
db=SQLAlchemy(app)
# Password manager
bcrypt = Bcrypt(app)
# Login manager
login_manager = LoginManager(app)
# Set the login route (function name of the route)
login_manager.login_view = 'login'
# Blue info alert from bootstrap
login_manager.login_message_category='info'

from dashboardapp import routes