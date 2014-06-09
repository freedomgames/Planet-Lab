"""Tests for mission endpoints."""


import json
import unittest

import harness


class QuestTest(harness.TestHarness):
    """Tests for quest endpoints."""

    def test_crud(self):
        """Basic CRUD tests."""
        # no quest yet, so 404
        resp = self.app.get("/api/users/1/missions/1/quest/1")
        self.assertEqual(resp.status_code, 404)

        # create a user, some missions, and some quests
        self.post_json("api/users/", {"name": "snakes"})
        self.post_json(
                "api/users/1/missions/",
                {"name": "snakes", "description": "ladders", "points": 3})
        self.post_json(
                "api/users/1/missions/",
                {"name": "happy", "description": "socks", "points": 1})

        resp = self.post_json(
                "api/users/1/missions/1/quests/",
                {"name": "mouse", "description": "nip"})
        self.assertEqual(resp.status_code, 200)
        resp = self.post_json(
                "api/users/1/missions/1/quests/",
                {"name": "blouse", "description": "blip"})
        self.assertEqual(resp.status_code, 200)
        resp = self.post_json(
                "api/users/1/missions/2/quests/",
                {"name": "house", "description": "snip", "icon_url": "blue"})
        self.assertEqual(resp.status_code, 200)

        # and get it back
        resp = self.app.get("/api/users/1/missions/1/quests/1")
        self.assertEqual(json.loads(resp.data), {
            'user_id': 1,
            'description': 'nip',
            'icon_url': None,
            'mission_id': 1,
            'id': 1,
            'url': '/api/users/1/missions/1/quests/1',
            'name': 'mouse'})

        # edit
        resp = self.put_json('api/users/1/missions/1/quests/1', {
            'icon_url': 'rubber'})
        self.assertEqual(resp.status_code, 200)

        # and get it back
        resp = self.app.get("api/users/1/missions/1/quests/1")
        self.assertEqual(json.loads(resp.data), {
            'user_id': 1,
            'description': 'nip',
            'icon_url': 'rubber',
            'mission_id': 1,
            'id': 1,
            'url': '/api/users/1/missions/1/quests/1',
            'name': 'mouse'})

        # list them
        resp = self.app.get("api/users/1/missions/1/quests/")
        self.assertItemsEqual(json.loads(resp.data)['quests'], [
            {'user_id': 1, 'description': 'nip', 'icon_url': 'rubber',
                'url': '/api/users/1/missions/1/quests/1',
                'mission_id': 1, 'id': 1, 'name': 'mouse'},
            {'user_id': 1, 'description': 'blip', 'icon_url': None,
                'url': '/api/users/1/missions/1/quests/2',
                'mission_id': 1, 'id': 2, 'name': 'blouse'}])

        # delete
        resp = self.app.delete("api/users/1/missions/1/quests/1")
        self.assertEqual(resp.status_code, 200)

        # and it's gone
        resp = self.app.get("/api/users/1/missions/1/quests/1")
        self.assertEqual(resp.status_code, 404)

        resp = self.put_json('api/users/1/missions/1/quests/1', {'name': 'no!'})
        self.assertEqual(resp.status_code, 404)

        resp = self.app.delete("/api/users/1/missions/1/quests/1")
        self.assertEqual(resp.status_code, 404)

    def test_404s(self):
        """Make sure we return 404's on invalid id combinations."""
        # create a user and a mission
        self.post_json("api/users/", {"name": "snakes"})
        self.post_json(
                "api/users/1/missions/",
                {"name": "snakes", "description": "ladders", "points": 3})

        # 404 on bad user-mission combos
        resp = self.post_json(
                "api/users/1/missions/2/quests/",
                {"name": "house", "description": "snip", "icon_url": "blue"})
        self.assertEqual(resp.status_code, 404)

        resp = self.post_json(
                "api/users/2/missions/1/quests/",
                {"name": "house", "description": "snip", "icon_url": "blue"})
        self.assertEqual(resp.status_code, 404)

        # okay, now let's get one
        resp = self.post_json(
                "api/users/1/missions/1/quests/",
                {"name": "house", "description": "snip", "icon_url": "blue"})
        self.assertEqual(resp.status_code, 200)
        resp = self.app.get("/api/users/1/missions/1/quests/1")
        self.assertEqual(resp.status_code, 200)

        # make sure we can't do anything on bad user-mission-quest id combos
        resp = self.app.get("/api/users/2/missions/1/quests/1")
        self.assertEqual(resp.status_code, 404)
        resp = self.app.get("/api/users/1/missions/2/quests/1")
        self.assertEqual(resp.status_code, 404)
        resp = self.app.get("/api/users/1/missions/1/quests/2")
        self.assertEqual(resp.status_code, 404)

        resp = self.put_json("/api/users/2/missions/1/quests/1", {'name': 'a'})
        self.assertEqual(resp.status_code, 404)
        resp = self.put_json("/api/users/1/missions/2/quests/1", {'name': 'a'})
        self.assertEqual(resp.status_code, 404)
        resp = self.put_json("/api/users/1/missions/1/quests/2", {'name': 'a'})
        self.assertEqual(resp.status_code, 404)

        resp = self.app.delete("/api/users/2/missions/1/quests/1")
        self.assertEqual(resp.status_code, 404)
        resp = self.app.delete("/api/users/1/missions/2/quests/1")
        self.assertEqual(resp.status_code, 404)
        resp = self.app.delete("/api/users/1/missions/1/quests/2")
        self.assertEqual(resp.status_code, 404)


if __name__ == '__main__':
    unittest.main()
