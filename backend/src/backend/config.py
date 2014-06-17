"""Config values for the flask app."""


import os


DEBUG = bool(os.environ.get('DEBUG', False))
SECRET_KEY = os.environ.get('SECRET_KEY', 'snakes')
SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
USER_ENABLE_EMAIL = bool(os.environ.get('USER_ENABLE_EMAIL', True))
