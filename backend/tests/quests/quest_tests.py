"""Tests for quest endpoints."""


import json
import unittest

import harness


class QuestTest(harness.TestHarness):
    """Tests for quest endpoints."""

    def test_crud(self):
        """Basic CRUD tests."""
        # no quest yet, so 404
        resp = self.app.get("/api/users/1/quests/1")
        self.assertEqual(resp.status_code, 404)

        # create a user and some quests
        self.post_json("api/users/", {"name": "snakes"})
        resp = self.post_json(
                "api/users/1/quests/",
                {"name": "snakes", "description": "ladders", "points": 3})
        self.assertEqual(resp.status_code, 200)
        resp = self.post_json(
                "api/users/1/quests/",
                {"name": "happy", "description": "socks", "points": 1})
        self.assertEqual(resp.status_code, 200)

        # and get it back
        resp = self.app.get("/api/users/1/quests/1")
        self.assertEqual(json.loads(resp.data), {
            'points': 3,
            'user_id': 1,
            'description': 'ladders',
            'name': 'snakes',
            'id': 1})

        # edit
        resp = self.put_json('api/users/1/quests/1', {
            'name': 'cat', 'description': 'hat'})
        self.assertEqual(resp.status_code, 200)

        # and get it back
        resp = self.app.get("api/users/1/quests/1")
        self.assertEqual(json.loads(resp.data), {
            'points': 3,
            'user_id': 1,
            'description': 'hat',
            'name': 'cat',
            'id': 1})

        # list them
        resp = self.app.get("api/users/1/quests/")
        self.assertItemsEqual(json.loads(resp.data)['quests'], [
            {'points': 3, 'user_id': 1, 'description': 'hat',
                'name': 'cat', 'id': 1},
            {'points': 1, 'user_id': 1, 'description': 'socks',
                'name': 'happy', 'id': 2}])

        # delete
        resp = self.app.delete("api/users/1/quests/1")
        self.assertEqual(resp.status_code, 200)

        # and it's gone
        resp = self.app.get("/api/users/1/quests/1")
        self.assertEqual(resp.status_code, 404)

        resp = self.put_json('api/users/1/quests/1', {'name': 'nooooo'})
        self.assertEqual(resp.status_code, 404)

        resp = self.app.delete("/api/users/1/quests/1")
        self.assertEqual(resp.status_code, 404)


if __name__ == '__main__':
    unittest.main()
