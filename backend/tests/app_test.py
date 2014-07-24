"""Tests for basic app functionality."""


import json
import unittest

import harness


class AppTest(harness.TestHarness):
    """Tests for basic app functionality."""

    def test_index(self):
        """Make sure the index page works."""
        resp = self.app.get("/")
        self.assertEqual(resp.status_code, 200)

    @harness.with_sess(user_id=3)
    def test_user_info(self):
        """Test the current-user endpoint."""
        resp = self.app.get("/current-user")
        self.assertEqual(json.loads(resp.data), {'user_id': 3})

    @harness.with_sess(user_id=3)
    def test_logout(self):
        """Test the logout endpoint."""
        resp = self.app.put("/logout")
        self.assertEqual(resp.status_code, 200)

        resp = self.app.get("/current-user")
        self.assertEqual(json.loads(resp.data), {'user_id': None})


if __name__ == '__main__':
    unittest.main()
