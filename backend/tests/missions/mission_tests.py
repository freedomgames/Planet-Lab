"""Tests for mission endpoints."""


import json
import unittest

import harness


class MissionTest(harness.TestHarness):
    """Tests for mission endpoints."""

    def test_crud(self):
        """Basic CRUD tests."""
        # no mission yet, so 404
        resp = self.app.get("/api/users/1/missions/1")
        self.assertEqual(resp.status_code, 404)

        # create a user and some missions
        self.post_json("api/users/", {"name": "snakes"})
        resp = self.post_json(
                "api/users/1/missions/",
                {"name": "snakes", "description": "ladders", "points": 3})
        self.assertEqual(resp.status_code, 200)
        resp = self.post_json(
                "api/users/1/missions/",
                {"name": "happy", "description": "socks", "points": 1})
        self.assertEqual(json.loads(resp.data), {
            "description": "socks",
            "id": 2,
            "name": "happy",
            "points": 1,
            "url": "/api/users/1/missions/2",
            "quests": [],
            "user_id": 1})
        self.assertEqual(resp.status_code, 200)

        # and get it back
        resp = self.app.get("/api/users/1/missions/1")
        self.assertEqual(json.loads(resp.data), {
            'points': 3,
            'user_id': 1,
            'description': 'ladders',
            'name': 'snakes',
            'url': '/api/users/1/missions/1',
            "quests": [],
            'id': 1})

        # edit
        resp = self.put_json('api/users/1/missions/1', {
            'name': 'cat', 'description': 'hat'})
        self.assertEqual(resp.status_code, 200)

        # and get it back
        resp = self.app.get("api/users/1/missions/1")
        self.assertEqual(json.loads(resp.data), {
            'points': 3,
            'user_id': 1,
            'description': 'hat',
            'name': 'cat',
            'url': '/api/users/1/missions/1',
            "quests": [],
            'id': 1})

        # list them
        resp = self.app.get("api/users/1/missions/")
        self.assertItemsEqual(json.loads(resp.data)['missions'], [
            {'points': 3, 'user_id': 1, 'description': 'hat', 'quests': [],
                'name': 'cat', 'id': 1, 'url': '/api/users/1/missions/1'},
            {'points': 1, 'user_id': 1, 'description': 'socks', 'quests': [],
                'name': 'happy', 'id': 2, 'url': '/api/users/1/missions/2'}])

        # delete
        resp = self.app.delete("api/users/1/missions/1")
        self.assertEqual(resp.status_code, 200)

        # and it's gone
        resp = self.app.get("/api/users/1/missions/1")
        self.assertEqual(resp.status_code, 404)

        resp = self.put_json('api/users/1/missions/1', {'name': 'nooooo'})
        self.assertEqual(resp.status_code, 404)

        resp = self.app.delete("/api/users/1/missions/1")
        self.assertEqual(resp.status_code, 404)

    def test_links(self):
        """Test links between quests and missions."""

        # create the resources
        resp = self.post_json("api/users/", {"name": "snakes"})
        self.assertEqual(resp.status_code, 200)

        resp = self.post_json(
                "api/users/1/quests/",
                {"name": "mouse", "description": "nip"})
        self.assertEqual(resp.status_code, 200)

        resp = self.post_json(
                "api/users/1/quests/",
                {"name": "blouse", "description": "blip"})
        self.assertEqual(resp.status_code, 200)

        resp = self.post_json(
                "api/users/1/missions/",
                {"name": "hat", "description": "snap", "points": 2})
        self.assertEqual(resp.status_code, 200)

        resp = self.post_json(
                "api/users/1/missions/",
                {"name": "cat", "description": "map", "points": 1})
        self.assertEqual(resp.status_code, 200)

        resp = self.app.put("/api/users/1/missions/1/quests/1")
        self.assertEqual(resp.status_code, 200)

        resp = self.app.put("/api/users/1/missions/1/quests/2")
        self.assertEqual(resp.status_code, 200)

        resp = self.app.put("/api/users/1/missions/2/quests/1")
        self.assertEqual(resp.status_code, 200)

        resp = self.app.get("/api/users/1/missions/1")
        self.assertEqual(json.loads(resp.data), {
            "description": "snap", "id": 1, "name": "hat", "points": 2,
            "url": "/api/users/1/missions/1", "user_id": 1,
            "quests": [
                {"description": "nip", "icon_url": None, "id": 1,
                    "name": "mouse", "user_id": 1},
                {"description": "blip", "icon_url": None, "id": 2,
                    "name": "blouse", "user_id": 1}]})

        resp = self.app.get("/api/users/1/missions/2")
        self.assertEqual(json.loads(resp.data), {
            "name": "cat", "description": "map", "points": 1, "id": 2,
            "url": "/api/users/1/missions/2", "user_id": 1,
            "quests": [
                {"description": "nip", "icon_url": None, "id": 1,
                    "name": "mouse", "user_id": 1}]})


if __name__ == '__main__':
    unittest.main()
