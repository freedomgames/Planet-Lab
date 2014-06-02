import backend
import json
import unittest

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
