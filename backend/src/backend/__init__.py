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

if not app.debug:
    # debug mode defaults to sending errors to stdout/stderr
    # outside debug mode, we still want to print to stdout/stderr
    # because heroku will capture and log that output
    app.logger.addHandler(logging.StreamHandler())
    app.logger.setLevel(logging.INFO)


@app.route('/')
def index():
    """Return the index page."""
    return "Hello"


def error_handler(error, status_code=500, payload=None, debug=app.debug):
    """Generic handler to return an exception as a json response."""
    app.logger.exception(error)

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


import backend.users.views as user_views
import backend.missions.views as mission_views
import backend.quests.views as quest_views

api.add_resource(user_views.User, '/v1/users/<int:user_id>')
api.add_resource(user_views.UserList, '/v1/users/')

api.add_resource(mission_views.Mission, '/v1/missions/<int:mission_id>')
api.add_resource(mission_views.MissionList, '/v1/missions/')
api.add_resource(mission_views.MissionUserList, '/v1/users/<int:user_id>/missions/')

api.add_resource(quest_views.Quest, '/v1/quests/<int:quest_id>')
api.add_resource(quest_views.QuestList, '/v1/quests/')
api.add_resource(quest_views.QuestUserList, '/v1/users/<int:user_id>/quests/')

api.add_resource(
        quest_views.QuestMissionLink,
        '/v1/missions/<int:left_id>/quests/<int:right_id>')
api.add_resource(
        quest_views.QuestMissionLinkList,
        '/v1/missions/<int:mission_id>/quests/')
