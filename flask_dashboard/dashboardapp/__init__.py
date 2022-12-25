# import necessay files
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os



# statement to create flask app
app = Flask(__name__)
# The session key is in the environment variable
app.config['SECRET_KEY']='93c34a429a3473ca9cbd70ab5c6b931a'
# Setup the database
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///site.db'
# Create the database
db=SQLAlchemy(app)

from dashboardapp import routes