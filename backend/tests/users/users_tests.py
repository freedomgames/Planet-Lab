"""Tests for user endpoints."""


import json
import unittest

import harness


class UsersTest(harness.TestHarness):
    """Tests for user endpoints."""

    def test_crud(self):
        """Basic CRUD tests."""
        # no users yet, so 404
        resp = self.app.get("/api/users/1")
        self.assertEqual(resp.status_code, 404)

        # create a user
        resp = self.post_json("api/users/", {"name": "snakes"})
        self.assertEqual(json.loads(resp.data), {
            'organization': None,
            'avatar_url': None,
            'id': 1,
            'name': 'snakes'})

        # and get it back
        resp = self.app.get("/api/users/1")
        self.assertEqual(json.loads(resp.data), {
            'organization': None,
            'avatar_url': None,
            'id': 1,
            'name': 'snakes'})

        # missing required fields for a 400
        resp = self.post_json("api/users/", {})
        self.assertEqual(resp.status_code, 400)

        # edit the user
        resp = self.put_json('api/users/1', {
            'name': 'ladders', 'organization': 'hat hotel'})
        self.assertEqual(resp.status_code, 200)

        # and get it back
        resp = self.app.get("api/users/1")
        self.assertEqual(json.loads(resp.data), {
            'organization': 'hat hotel',
            'avatar_url': None,
            'id': 1,
            'name': 'ladders'})

        # delete the user
        resp = self.app.delete("api/users/1")
        self.assertEqual(resp.status_code, 200)

        # and it's gone
        resp = self.app.get("/api/users/1")
        self.assertEqual(resp.status_code, 404)

        resp = self.put_json('api/users/1', {
            'name': 'ladders', 'organization': 'hat hotel'})
        self.assertEqual(resp.status_code, 404)

        resp = self.app.delete("/api/users/1")
        self.assertEqual(resp.status_code, 404)


if __name__ == '__main__':
    unittest.main()
