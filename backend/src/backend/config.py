"""Config values for the flask app."""


import os


AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
CLOUDFRONT_URL = os.environ['CLOUDFRONT_URL']
DEBUG = bool(os.environ.get('DEBUG', False))
S3_BUCKET = os.environ['S3_BUCKET']
SECRET_KEY = os.environ['SECRET_KEY']
SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
USER_ENABLE_EMAIL = bool(os.environ.get('USER_ENABLE_EMAIL', True))
