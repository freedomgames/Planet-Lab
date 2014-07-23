"""Tests for mission endpoints."""


import json
import unittest

import backend
import harness


class MissionTest(harness.TestHarness):
    """Tests for mission endpoints."""

    @harness.with_sess(user_id=1)
    def test_crud(self):
        """Basic CRUD tests."""
        # no mission yet, so 404
        resp = self.app.get("/v1/missions/1")
        self.assertEqual(resp.status_code, 404)

        # create a user and some missions
        harness.create_user(name='snakes')
        resp = self.post_json(
                self.url_for(backend.mission_views.MissionList),
                {"name": "snakes", "description": "ladders", "points": 3})
        self.assertEqual(resp.status_code, 200)
        resp = self.post_json(
                self.url_for(backend.mission_views.MissionList),
                {"name": "happy", "description": "socks", "points": 1})
        self.assertEqual(json.loads(resp.data), {
            "description": "socks",
            "id": 2,
            "name": "happy",
            "points": 1,
            "url": "/v1/missions/2",
            "quests": [],
            "creator_url": "/v1/users/1",
            "creator_id": 1})
        self.assertEqual(resp.status_code, 200)

        # and get it back
        resp = self.app.get("/v1/missions/1")
        self.assertEqual(json.loads(resp.data), {
            'points': 3,
            "creator_url": "/v1/users/1",
            'creator_id': 1,
            'description': 'ladders',
            'name': 'snakes',
            'url': '/v1/missions/1',
            "quests": [],
            'id': 1})

        # edit
        resp = self.put_json('/v1/missions/1', {
            'name': 'cat', 'description': 'hat', 'points': 3})
        self.assertEqual(resp.status_code, 200)

        # and get it back
        resp = self.app.get("/v1/missions/1")
        self.assertEqual(json.loads(resp.data), {
            'points': 3,
            "creator_url": "/v1/users/1",
            'creator_id': 1,
            'description': 'hat',
            'name': 'cat',
            'url': '/v1/missions/1',
            "quests": [],
            'id': 1})

        # list them
        resp = self.app.get(self.url_for(
            backend.mission_views.MissionUserList, user_id=1))
        self.assertItemsEqual(json.loads(resp.data)['missions'], [
            {'points': 3, 'creator_id': 1, 'description': 'hat', 'quests': [],
                "creator_url": "/v1/users/1",
                'name': 'cat', 'id': 1, 'url': '/v1/missions/1'},
            {'points': 1, 'creator_id': 1, 'description': 'socks', 'quests': [],
                "creator_url": "/v1/users/1",
                'name': 'happy', 'id': 2, 'url': '/v1/missions/2'}])
        # delete
        resp = self.app.delete("/v1/missions/1")
        self.assertEqual(resp.status_code, 200)

        # and it's gone
        resp = self.app.get("/v1/missions/1")
        self.assertEqual(resp.status_code, 404)

        resp = self.put_json('/v1/missions/1', {
            'name': 'cat', 'description': 'hat', 'points': 3})
        self.assertEqual(resp.status_code, 404)

        resp = self.app.delete("/v1/missions/1")
        self.assertEqual(resp.status_code, 404)

    @harness.with_sess(user_id=1)
    def test_links(self):
        """Test links between quests and missions."""

        # create the resources
        harness.create_user(name='snakes')

        resp = self.post_json(
                self.url_for(backend.quest_views.QuestList),
                {"name": "mouse", "summary": "nip"})
        self.assertEqual(resp.status_code, 200)

        resp = self.post_json(
                self.url_for(backend.quest_views.QuestList),
                {"name": "blouse", "summary": "blip"})
        self.assertEqual(resp.status_code, 200)

        resp = self.post_json(
                self.url_for(backend.mission_views.MissionList),
                {"name": "hat", "description": "snap", "points": 2})
        self.assertEqual(resp.status_code, 200)

        resp = self.post_json(
                self.url_for(backend.mission_views.MissionList),
                {"name": "cat", "description": "map", "points": 1})
        self.assertEqual(resp.status_code, 200)

        resp = self.app.put("/v1/missions/1/quests/1")
        self.assertEqual(resp.status_code, 200)

        resp = self.app.put("/v1/missions/1/quests/2")
        self.assertEqual(resp.status_code, 200)

        resp = self.app.put("/v1/missions/2/quests/1")
        self.assertEqual(resp.status_code, 200)

        resp = self.app.get("/v1/missions/1")
        self.assertEqual(json.loads(resp.data), {
            "description": "snap", "id": 1, "name": "hat", "points": 2,
            "url": "/v1/missions/1", "creator_id": 1,
            "creator_url": "/v1/users/1",
            "quests": [
                {"summary": "nip", "icon_url": None, "id": 1,
                    "url": "/v1/quests/1",
                    "creator_url": "/v1/users/1",
                    "name": "mouse", "creator_id": 1},
                {"summary": "blip", "icon_url": None, "id": 2,
                    "url": "/v1/quests/2",
                    "creator_url": "/v1/users/1",
                    "name": "blouse", "creator_id": 1}]})

        resp = self.app.get("/v1/missions/2")
        self.assertEqual(json.loads(resp.data), {
            "name": "cat", "description": "map", "points": 1, "id": 2,
            "url": "/v1/missions/2", "creator_id": 1,
            "creator_url": "/v1/users/1",
            "quests": [
                {"summary": "nip", "icon_url": None, "id": 1,
                    "url": "/v1/quests/1",
                    "creator_url": "/v1/users/1",
                    "name": "mouse", "creator_id": 1}]})


if __name__ == '__main__':
    unittest.main()
