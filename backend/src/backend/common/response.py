"""Functions for creating http responses."""

import flask
import functools
import traceback

import backend


def no_cache(func):
    """Decorator that may be added to any function that returns a flask
    response.  Adds headers which prevent browser caching.
    """
    @functools.wraps(func)
    def new_func(*args, **kwargs):
        """Add headers to the response before returning it."""
        response = func(*args, **kwargs)
        response.headers.add(
                'Cache-Control', 'no-store, no-cache, must-revalidate')
        response.headers.add('Pragma', 'no-cache')
        response.headers.add('Expires', '0')
        return response
    return new_func


def error_handler(
        error, status_code=500, payload=None, debug=backend.app.debug):
    """Generic handler to return an exception as a json response."""
    backend.app.logger.exception(error)

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
