"""Config values for the flask app."""


import os


DEBUG = bool(os.environ.get('DEBUG', False))
GOOGLE_CLIENT_ID = os.environ['GOOGLE_CLIENT_ID']
GOOGLE_CLIENT_SECRET = os.environ['GOOGLE_CLIENT_SECRET']
SECRET_KEY = os.environ.get('SECRET_KEY', 'snakes')
SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
