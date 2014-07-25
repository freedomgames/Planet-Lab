"""REST backend for the google analytics UI."""


import flask
import flask_babel
import flask_login
import flask_restful
import flask_sqlalchemy
import flask_user
import logging


app = flask.Flask(__name__)
app.config.from_object('backend.config')
api = flask_restful.Api(app)
babel = flask_babel.Babel(app)
db = flask_sqlalchemy.SQLAlchemy(app)

if not app.debug:
    # debug mode defaults to sending errors to stdout/stderr
    # outside debug mode, we still want to print to stdout/stderr
    # because heroku will capture and log that output
    app.logger.addHandler(logging.StreamHandler())
    app.logger.setLevel(logging.INFO)


# We have to import these after defining app, api and db as these
# imports will be looking for those variables.
import backend.common.auth as auth
import backend.common.response as response
import backend.missions.views as mission_views
import backend.organizations.views as organization_views
import backend.quests.views as quest_views
import backend.questions.views as question_views
import backend.users.models as user_models
import backend.users.views as user_views


db_adapter = flask_user.SQLAlchemyAdapter(db, user_models.User)
flask_user.UserManager(db_adapter, app)


@app.route('/')
def index():
    """Return the index page."""
    return app.send_static_file('index.html')

@app.route('/app')
@flask_user.login_required
@response.no_cache
def app_page():
    """Return the javascript for the app."""
    return app.send_static_file('app.html')

@app.route('/current-user')
def user_info():
    """Return basic info about the currently logged-in user."""
    return flask.jsonify({'user_id': flask.session.get('user_id')})

@app.route('/logout', methods=('PUT',))
def logout():
    """Clear the session and return the index page."""
    flask_login.logout_user()
    flask.session.clear()
    return flask.make_response()

@app.errorhandler(Exception)
def other_error(error):
    """Catch any other exception.
    NOTE:
    This must be the last declared errorhandler or else it will
    swallow up other errorhandlers.
    """
    return response.error_handler(error, payload={'type': 'general error'})


api.add_resource(user_views.User, '/v1/users/<int:user_id>')
api.add_resource(
        user_views.UserAvatar, '/v1/users/<int:user_id>/avatar/<file_name>')

api.add_resource(mission_views.Mission, '/v1/missions/<int:mission_id>')
api.add_resource(mission_views.MissionList, '/v1/missions')
api.add_resource(
        mission_views.MissionUserList, '/v1/users/<int:user_id>/missions')

api.add_resource(quest_views.Quest, '/v1/quests/<int:quest_id>')
api.add_resource(quest_views.QuestList, '/v1/quests')

api.add_resource(
        quest_views.QuestStaticAsset,
        '/v1/quests/<int:quest_id>/uploads/<file_name>')
api.add_resource(
        quest_views.QuestStaticAssets, '/v1/quests/<int:quest_id>/uploads')

api.add_resource(quest_views.QuestUserList, '/v1/users/<int:user_id>/quests')
api.add_resource(
        quest_views.QuestMissionLink,
        '/v1/missions/<int:left_id>/quests/<int:right_id>')
api.add_resource(
        quest_views.QuestMissionLinkList,
        '/v1/missions/<int:mission_id>/quests')

api.add_resource(quest_views.Tag, '/v1/quest-tags/<int:tag_id>')
api.add_resource(quest_views.TagList, '/v1/quest-tags')
api.add_resource(
        quest_views.QuestTagLink,
        '/v1/quests/<int:left_id>/tags/<int:right_id>')

api.add_resource(
        question_views.Question,
        '/v1/quests/<int:quest_id>/questions/<int:question_id>')
api.add_resource(
        question_views.QuestionList,
        '/v1/quests/<int:parent_id>/questions')
api.add_resource(
        question_views.QuestionView,
        '/v1/questions/<int:question_id>')

api.add_resource(
        question_views.Answer,
        '/v1/questions/<int:question_id>/answers/<int:answer_id>')
api.add_resource(
        question_views.AnswerList,
        '/v1/questions/<int:parent_id>/answers')

api.add_resource(
        question_views.MultipleChoice,
        '/v1/questions/<int:question_id>/multiple_choices/'
            '<int:multiple_choice_id>')
api.add_resource(
        question_views.MultipleChoiceList,
        '/v1/questions/<int:parent_id>/multiple_choices')

api.add_resource(
        organization_views.Organization,
        '/v1/organizations/<int:organization_id>')
api.add_resource(organization_views.OrganizationList, '/v1/organizations')
api.add_resource(
        organization_views.OrganizationUserLink,
        '/v1/organizations/<int:left_id>/users/<int:right_id>')
