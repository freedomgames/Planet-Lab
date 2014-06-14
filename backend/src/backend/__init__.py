"""REST backend for the google analytics UI."""


import flask
import flask.ext.restful as flask_restful
import flask.ext.sqlalchemy as flask_sqlalchemy
import logging
import traceback

import backend.config as config


app = flask.Flask(__name__)
app.config.from_object('backend.config')
api = flask_restful.Api(app)
db = flask_sqlalchemy.SQLAlchemy(app)


@app.route('/')
def index():
    """Return the index page."""
    return "Hello"


def error_handler(error, status_code=500, payload=None, debug=config.DEBUG):
    """Generic handler to return an exception as a json response."""
    logging.exception(error)

    if debug:
        response = {'message': error.message,
                'traceback': traceback.format_exc()}
    else:
        response = {'message': 'server error'}

    if payload is not None:
        response.update(payload)

    response = flask.jsonify(response)
    response.status_code = status_code
    return response

@app.errorhandler(Exception)
def other_error(error):
    """Catch any other exception.
    NOTE:
    This must be the last declared errorhandler or else it will
    swallow up other errorhandlers.
    """
    return error_handler(error, payload={'type': 'general error'})


import backend.users.views
api.add_resource(backend.users.views.User, '/api/users/<int:id_>')
api.add_resource(backend.users.views.UserList, '/api/users/')
