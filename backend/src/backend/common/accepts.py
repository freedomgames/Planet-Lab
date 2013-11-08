"""Utility functions for handling accept headers."""


import flask


def wants_json():
    """Return a boolean indicating whether we should return json."""
    best = flask.request.accept_mimetypes.best_match(
            ('application/json', 'text/html'))
    return (best == 'application/json' and
            flask.request.accept_mimetypes[best] >
            flask.request.accept_mimetypes['text/html'])
