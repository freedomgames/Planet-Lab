"""Tests for the response module."""

import json
import unittest

import backend
import backend.common.response as response


class ResponseTest(unittest.TestCase):
    """Tests for the response module."""

    def test_error_handler(self):
        """Test the error_handler function."""
        with backend.app.test_request_context():
            resp = response.error_handler(Exception('error test'), debug=False)
            self.assertEqual(
                    json.loads(resp.data), {"message": "server error"})

            resp = response.error_handler(
                    Exception('error test'), debug=False, payload={'a': 'b'})
            self.assertEqual(json.loads(resp.data), {
                "message": "server error", "a": "b"})

            resp = response.error_handler(Exception('error test'), debug=True)
            self.assertEqual(
                    json.loads(resp.data)['message'], 'error test')

    def test_no_cache(self):
        """Test the no_cache decorator."""

        class FakeHeaders(object):
            def __init__(self):
                self.headers = {}

            def add(self, key, value):
                self.headers[key] = value

        class FakeResponse(object):
            def __init__(self):
                self.headers = FakeHeaders()

        @response.no_cache
        def fake_function():
            return FakeResponse()

        headers = fake_function().headers.headers
        self.assertEqual(headers, {
            'Expires': '0',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-store, no-cache, must-revalidate'})


if __name__ == '__main__':
    unittest.main()
