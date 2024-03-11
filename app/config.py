import os

class Config:
    # Flask
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY')
    # Database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Projections
    PROJECTIONS_DOWNLOAD_INTERVAL_MINUTES = 30
    PROJECTIONS_DOWNLOAD_LOCAL_KEY = 'projections.csv'

