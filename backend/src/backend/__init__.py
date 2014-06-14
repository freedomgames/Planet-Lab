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
api.add_resource(backend.users.views.User, '/api/users/<int:user_id>')
api.add_resource(backend.users.views.UserList, '/api/users/')

import backend.missions.views
api.add_resource(
        backend.missions.views.Mission,
        '/api/users/<int:user_id>/missions/<int:mission_id>')
api.add_resource(
        backend.missions.views.MissionList,
        '/api/users/<int:user_id>/missions/')

import backend.quests.views
api.add_resource(
        backend.quests.views.Quest,
        '/api/users/<int:user_id>/missions/<int:mission_id>'
        '/quests/<int:quest_id>')
api.add_resource(
        backend.quests.views.QuestList,
        '/api/users/<int:user_id>/missions/<int:mission_id>/quests/')
