import functools
import json
import unittest
import uuid

import backend
import backend.users.models as user_models


class TestHarness(unittest.TestCase):
    """Base class for writing unit tests against the backend."""

    def setUp(self):
        """Flush the db, create the tables and start the test app."""
        # All of these goofy commit() calls are to force transactions
        # to finish up before proceeding.  Bad things happen if you
        # try to do a drop_all while a transaction is still hanging
        # around (it hangs indefinitely.)
        backend.db.session.commit()
        backend.db.drop_all()
        backend.db.session.commit()
        backend.db.create_all()
        backend.db.session.commit()

        self.app = backend.app.test_client()

    def post_json(self, url, data):
        """Helper method for posting a JSON payload."""
        return self.app.post(url, data=json.dumps(data), headers={
            'Content-type': 'application/json'})

    def put_json(self, url, data):
        """Helper method for puting a JSON payload."""
        return self.app.put(url, data=json.dumps(data), headers={
            'Content-type': 'application/json'})

    def update_session(self, **session_update):
        """Set the given session values."""
        with self.app.session_transaction() as sess:
            sess.update(**session_update)

    def url_for(self, *args, **kwargs):
        """Short-cut to the flask_restful url_for function."""
        with backend.app.test_request_context():
            return backend.api.url_for(*args, **kwargs)


def create_user(**user_args):
    """Insert a user into the database with the given paramater."""
    if 'username' not in user_args:
        user_args['username'] = str(uuid.uuid4())
    if 'active' not in user_args:
        user_args['active'] = True

    user = user_models.User(**user_args)
    backend.db.session.add(user)
    backend.db.session.commit()


def with_sess(**session_update):
    """Decorator for calling a function with the suplied session
    values set.
    """
    def decorator(func):
        """Decorator for session updates."""
        @functools.wraps(func)
        def decorated_func(self, *args, **kwargs):
            """Update the session and call the decorated function."""
            # update the session
            with self.app.session_transaction() as sess:
                sess.update(**session_update)
            # call the original function
            res = func(self, *args, **kwargs)
            # empty the session
            with self.app.session_transaction() as sess:
                sess.clear()
            return res
        return decorated_func
    return decorator
