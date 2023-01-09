import os
class Config:
    # The session key is in the environment variable
    SECRET_KEY='93c34a429a3473ca9cbd70ab5c6b931a' #os.environ.get('SECRET_KEY')
    # Setup the database (two seperates ones for data and keys)
    SQLALCHEMY_DATABASE_URI='sqlite:///site.db'#os.environ.get('SQLALCHEMY_DATABASE_URI')

    SQLALCHEMY_BINDS= {
        'keys':'sqlite:///keys.db'} #os.environ.get('SQLALCHEMY_DATABASE_URI_2'
    # Upload extensions for datasets
    UPLOAD_EXTENSIONS = ['.csv']