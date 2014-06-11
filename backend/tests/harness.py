import functools
import json
import unittest

import backend

class TestHarness(unittest.TestCase):
    """Base class for writing unit tests against the backend."""

    def setUp(self):
        """Flush the db, create the tables and start the test app."""
        backend.db.drop_all()
        backend.db.create_all()
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



