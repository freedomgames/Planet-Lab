"""Utilities related to user authorization."""


import flask
import functools


def login_required(func):
    """Decorator to force login before the resource can be requested."""

    @functools.wraps(func)
    def protected_func(*args, **kwargs):
        """Redirect to the login resource if needed,
        otherwise call the decorated function.
        """
        if 'user_id' not in flask.session:
            # Put the page they were heading for into the
            # session so we can redirect them there later.
            # We sadly can't carry this around in query string because
            # oauth is picky about the callback URL, including the
            # query string, so it will look like the user is
            # being redirected to a non-authorized URL.
            flask.session['next'] = flask.request.path
            return flask.redirect(flask.url_for('login'))
        else:
            return func(*args, **kwargs)
    return protected_func


def current_user_id():
    """Return the id of the user for whom we are handling a request."""
    return flask.session['user_id']
