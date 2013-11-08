"""Config values for the flask app."""


import os


DEBUG = bool(os.environ.get('DEBUG', True))
SECRET_KEY = os.environ.get(
        'SECRET_KEY',
        '\xc9\xabf\x18\xe4nL`t\xf5G\x86\xd6?\xde\xd9>6\x00Z\xdc\xd3\x82h')
SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
