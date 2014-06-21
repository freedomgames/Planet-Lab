"""Utilities related to user authorization."""


import flask


def current_user_id():
    """Return the id of the user for whom we are handling a request."""
    return flask.session['user_id']
