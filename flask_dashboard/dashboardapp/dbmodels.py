# Imports db from __init__.py
from dashboardapp import db, login_manager
from datetime import datetime
from flask_login import UserMixin

# Enables the login manager to load the user
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Relational database to track users, api calls, datafiles and so on
class User(db.Model, UserMixin):
    id =  db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(), unique=True, nullable=False)
    lastname = db.Column(db.String(), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file= db.Column(db.String(20), nullable=False, default='default.jpg') # Profile picture
    password = db.Column(db.String(60), nullable=False)
    # Similar to creating a 'client' column in the 'APIUsage' database to link back to User
    apiUsage = db.relationship('APIUsage', backref= 'client', lazy=True)
    # Connect user to the datasets database
    datasetsUsage = db.relationship('Datasets', backref= 'owner', lazy=True)

    # returns the object representation in string format.
    def __repr__(self):
        return f"User('{self.firstname}', '{self.lastname}', '{self.email}', '{self.image_file}')"

class APIUsage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    num_of_calls = db.Column(db.Integer)
    # Encryption type is used to specify 'Statistics', 'Visualization', 'Encrypt-decrypt', 'Training', 'Inference'
    call_type = db.Column(db.String(20), nullable=False) 
    date_called = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    api_contents = db.Column(db.Text, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # returns the object representation in string format.
    def __repr__(self):
        return f"APIUsage('{self.encryption_call}', '{self.date_called}')"

# Database to store various files that users upload
class Datasets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    date_called = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_encrypted = db.Column(db.Boolean, nullable=False, default=False)
    description = db.Column(db.Text, nullable = False, default='')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Connect datasets to the encryption database
    #datasetsUsage = db.relationship('Encryption', backref= 'encrypteddata', lazy=True)


    # returns the object representation in string format.
    def __repr__(self):
        return f"Datasets('{self.filename}', '{self.date_called}','{self.description}')"

# Database to store encryption details
class Encryption(db.Model):
    __bind_key__ = 'keys'
    id = db.Column(db.Integer, primary_key=True)
    dataset_id = db.Column(db.Integer, nullable=False, unique = True)
    encryption_type = db.Column(db.String(20), nullable=False, default='Complete') 
    encryption_key = db.Column(db.Text, nullable=False, default='None')
    encryption_nonce = db.Column(db.Text, nullable=False, default='None')
    date_called = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    encryption_details = db.Column(db.Text, nullable = False, default='')
    
    # returns the object representation in string format.
    def __repr__(self):
        return f"Encryption('{self.dataset_id}','{self.encryption_type}', '{self.date_called}','{self.encryption_details}')"