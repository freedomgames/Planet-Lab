"""Routes for handling user authorization via OAuth."""

import flask
import flask_oauth
import requests
import sqlalchemy

import backend
import backend.users.models as user_models


OAUTH = flask_oauth.OAuth()

GOOGLE_OAUTH = OAUTH.remote_app(
        'google',
        base_url='https://www.google.com/accounts/',
        authorize_url='https://accounts.google.com/o/oauth2/auth',
        request_token_url=None,
        request_token_params={
            'scope': 'https://www.googleapis.com/auth/userinfo.email',
            'response_type': 'code'},
        access_token_url='https://accounts.google.com/o/oauth2/token',
        access_token_method='POST',
        access_token_params={'grant_type': 'authorization_code'},
        consumer_key=backend.app.config['GOOGLE_CLIENT_ID'],
        consumer_secret=backend.app.config['GOOGLE_CLIENT_SECRET'])

GOOGLE_USER_INFO_URI = 'https://www.googleapis.com/oauth2/v1/userinfo'


def get_google_user_info(access_token):
    """Retrieve profile information about the user."""
    headers = {'Authorization': 'OAuth ' + access_token}
    return requests.get(GOOGLE_USER_INFO_URI, headers=headers)


@backend.app.route('/auth/google/login')
def google_login():
    """Redirect the user to the Google oauth page."""
    callback = flask.url_for('google_callback', _external=True)
    return GOOGLE_OAUTH.authorize(callback=callback)


@backend.app.route('/auth/google/oauth2callback')
@GOOGLE_OAUTH.authorized_handler
def google_callback(resp):
    """Create or retrieve the user from the database, setting their
    user id in the session.
    """
    try:
        access_token = resp['access_token']
    except (KeyError, TypeError):
        # user must have bailed, back to the login page
        return flask.redirect(flask.url_for('login'))
    else:
        info_resp = get_google_user_info(access_token)
        if info_resp.status_code != 200:
            # Must have been a bad access token or something is up
            # with the goole API.
            backend.app.logger.error(
                    "error in google oauth response: %s\n%s",
                    info_resp.status_code, info_resp.text)
            return flask.Response("Error with Google Log-In", 500)
        else:
            user_id = get_or_create_google_user(access_token, info_resp.json())
            flask.session['user_id'] = user_id
            next_url = flask.session.pop('next', flask.url_for('app_page'))
            return flask.redirect(next_url)


def get_or_create_google_user(access_token, user_info):
    """Create the user with the given user information if they do
    not already exist.  Return the id of the new or existing user.
    """
    oauth_id = user_info['id']
    oauth_type = user_models.GOOGLE_OAUTH_TYPE
    email = user_info.get('email')
    name = user_info.get('name')
    if name is None:
        name = (user_info.get('given_name', '') +
                user_info.get('family_name', ''))

    # We want to do a 'get or insert' in one atomic query.
    # We accomplish this with a writable CTE unioned with a select.
    # The CTE is essentially
    # "insert new-user where not exists existing-user returning new-user-id"
    # unioned with "select id from existing-user"
    # Unfortunately, SQLAlchemy does not support writable CTE's, so we are
    # foreced to maintain raw SQL here.
    query = sqlalchemy.text("""
WITH
existing_user AS (
SELECT id
FROM users
WHERE oauth_id=:oauth_id AND oauth_type=:oauth_type),

new_user AS (
INSERT INTO users (oauth_id, email, name, oauth_type, oauth_token)
SELECT :oauth_id, :email, :name,
       :oauth_type, :access_token
WHERE NOT EXISTS (SELECT id FROM existing_user)
RETURNING id)

SELECT id FROM new_user
UNION
SELECT id FROM existing_user""")

    res = backend.db.session.execute(query, {
        'oauth_id': oauth_id, 'oauth_type': oauth_type,
        'email': email, 'name': name, 'access_token': access_token})
    backend.db.session.commit()
    inserted_id = res.first()[0]
    return inserted_id


@GOOGLE_OAUTH.tokengetter
def google_access_token():
    """Retrieve the user's access token from the database."""
    user_id = flask.session.get('user_id')
    if user_id is None:
        return None
    else:
        token_row = backend.db.session.query(
                user_models.User.oauth_token).filter_by(id=user_id).first()
        if token_row:
            return (token_row[0], '')
        else:
            return None
