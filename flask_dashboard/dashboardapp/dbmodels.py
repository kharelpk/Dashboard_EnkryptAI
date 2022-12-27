# Imports db from __init__.py
from dashboardapp import db, login_manager
from datetime import datetime
from flask_login import UserMixin

# Enables the login manager to load the user
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Relational database to track users and api calls
class User(db.Model, UserMixin):
    id =  db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(), unique=True, nullable=False)
    lastname = db.Column(db.String(), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file= db.Column(db.String(20), nullable=False, default='default.jpg') # Profile picture
    password = db.Column(db.String(60), nullable=False)
    # Similar to creating a 'client' column in the 'APIUsage' database to link back to User
    apiUsage = db.relationship('APIUsage', backref= 'client', lazy=True)

    # returns the object representation in string format.
    def __repr__(self):
        return f"User('{self.firstname}', '{self.lastname}', '{self.email}', '{self.image_file}')"

class APIUsage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    encryption_call = db.Column(db.Integer)
    # Encryption type is used to specify 'Statistics', 'Visualization', 'Encrypt-decrypt', 'Training', 'Inference'
    enryption_type = db.Column(db.String(20), nullable=False) 
    date_called = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    api_contents = db.Column(db.Text, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # returns the object representation in string format.
    def __repr__(self):
        return f"APIUsage('{self.encryption_call}', '{self.date_called}')"

