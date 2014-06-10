"""Tests for mission endpoints."""


import json
import unittest

import harness


class QuestTest(harness.TestHarness):
    """Tests for quest endpoints."""

    def test_crud(self):
        """Basic CRUD tests."""
        # no quest yet, so 404
        resp = self.app.get("/api/users/1/quest/1")
        self.assertEqual(resp.status_code, 404)

        # create a user, some missions, and some quests
        self.post_json("api/users/", {"name": "snakes"})
        self.post_json("api/users/", {"name": "rakes"})

        resp = self.post_json(
                "api/users/1/quests/",
                {"name": "mouse", "description": "nip"})
        self.assertEqual(resp.status_code, 200)
        resp = self.post_json(
                "api/users/1/quests/",
                {"name": "blouse", "description": "blip"})
        self.assertEqual(resp.status_code, 200)
        resp = self.post_json(
                "api/users/2/quests/",
                {"name": "house", "description": "snip", "icon_url": "blue"})
        self.assertEqual(resp.status_code, 200)

        # and get it back
        resp = self.app.get("/api/users/1/quests/1")
        self.assertEqual(json.loads(resp.data), {
            'user_id': 1,
            'description': 'nip',
            'icon_url': None,
            'id': 1,
            'url': '/api/users/1/quests/1',
            'name': 'mouse'})

        # edit
        resp = self.put_json('api/users/1/quests/1', {
            'icon_url': 'rubber'})
        self.assertEqual(resp.status_code, 200)

        # and get it back
        resp = self.app.get("api/users/1/quests/1")
        self.assertEqual(json.loads(resp.data), {
            'user_id': 1,
            'description': 'nip',
            'icon_url': 'rubber',
            'id': 1,
            'url': '/api/users/1/quests/1',
            'name': 'mouse'})

        # list them
        resp = self.app.get("api/users/1/quests/")
        self.assertItemsEqual(json.loads(resp.data)['quests'], [
            {'user_id': 1, 'description': 'nip', 'icon_url': 'rubber',
                'url': '/api/users/1/quests/1',
                'id': 1, 'name': 'mouse'},
            {'user_id': 1, 'description': 'blip', 'icon_url': None,
                'url': '/api/users/1/quests/2',
                'id': 2, 'name': 'blouse'}])

        # delete
        resp = self.app.delete("api/users/1/quests/1")
        self.assertEqual(resp.status_code, 200)

        # and it's gone
        resp = self.app.get("/api/users/1/quests/1")
        self.assertEqual(resp.status_code, 404)

        resp = self.put_json('api/users/1/quests/1', {'name': 'no!'})
        self.assertEqual(resp.status_code, 404)

        resp = self.app.delete("/api/users/1/quests/1")
        self.assertEqual(resp.status_code, 404)

    def test_links(self):
        """Test linking quests and missions together."""

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

        # no links yet
        resp = self.app.get("/api/users/1/missions/1/quests/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(json.loads(resp.data)['quests'], [])

        # create some links
        resp = self.app.put("/api/users/1/missions/1/quests/1")
        self.assertEqual(resp.status_code, 200)

        resp = self.app.get("/api/users/1/missions/1/quests/")
        self.assertEqual(json.loads(resp.data)['quests'], [
            {"description": "nip", "icon_url": None, "id": 1,
                "name": "mouse", "url": "/api/users/1/quests/1",
                "user_id": 1}])

        resp = self.app.put("/api/users/1/missions/1/quests/2")
        self.assertEqual(resp.status_code, 200)

        resp = self.app.get("/api/users/1/missions/1/quests/")
        self.assertItemsEqual(json.loads(resp.data)['quests'], [
            {"description": "nip", "icon_url": None, "id": 1,
                "name": "mouse", "url": "/api/users/1/quests/1",
                "user_id": 1},
            {'user_id': 1, 'description': 'blip',
                'url': '/api/users/1/quests/2', 'icon_url': None,
                'id': 2, 'name': 'blouse'}])

        # check for idempotency
        resp = self.app.put("/api/users/1/missions/1/quests/2")
        self.assertEqual(resp.status_code, 200)

        resp = self.app.get("/api/users/1/missions/1/quests/")
        self.assertItemsEqual(json.loads(resp.data)['quests'], [
            {"description": "nip", "icon_url": None, "id": 1,
                "name": "mouse", "url": "/api/users/1/quests/1",
                "user_id": 1},
            {'user_id': 1, 'description': 'blip',
                'url': '/api/users/1/quests/2', 'icon_url': None,
                'id': 2, 'name': 'blouse'}])

        # delete links
        resp = self.app.delete("/api/users/1/missions/1/quests/2")
        self.assertEqual(resp.status_code, 200)

        resp = self.app.get("/api/users/1/missions/1/quests/")
        self.assertEqual(json.loads(resp.data)['quests'], [
            {"description": "nip", "icon_url": None, "id": 1,
                "name": "mouse", "url": "/api/users/1/quests/1",
                "user_id": 1}])

        resp = self.app.delete("/api/users/1/missions/1/quests/1")
        self.assertEqual(resp.status_code, 200)

        resp = self.app.get("/api/users/1/missions/1/quests/")
        self.assertEqual(json.loads(resp.data)['quests'], [])


if __name__ == '__main__':
    unittest.main()
