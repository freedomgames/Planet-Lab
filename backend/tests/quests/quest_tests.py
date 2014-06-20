"""Tests for mission endpoints."""


import json
import unittest

import harness


class QuestTest(harness.TestHarness):
    """Tests for quest endpoints."""

    @harness.with_sess(user_id=1)
    def test_crud(self):
        """Basic CRUD tests."""
        # no quest yet, so 404
        resp = self.app.get("/v1/quest/1")
        self.assertEqual(resp.status_code, 404)

        # create a user, some missions, and some quests
        harness.create_user(name="snakes")
        harness.create_user(name="rakes")

        resp = self.post_json(
                "/v1/quests/",
                {"name": "mouse", "description": "nip"})
        self.assertEqual(resp.status_code, 200)
        resp = self.post_json(
                "/v1/quests/",
                {"name": "blouse", "description": "blip"})
        self.assertEqual(resp.status_code, 200)

        # create this one as a different user
        self.update_session(user_id=2)
        resp = self.post_json(
                "/v1/quests/",
                {"name": "house", "description": "snip", "icon_url": "blue"})
        self.assertEqual(resp.status_code, 200)
        self.update_session(user_id=1)

        # and get it back
        resp = self.app.get("/v1/quests/1")
        self.assertEqual(json.loads(resp.data), {
            'creator_id': 1,
            'creator_url': '/v1/users/1',
            'description': 'nip',
            'icon_url': None,
            'id': 1,
            'url': '/v1/quests/1',
            'name': 'mouse'})

        # edit
        resp = self.put_json('/v1/quests/1', {
            'description': 'nip', 'name': 'mouse', 'icon_url': 'rubber'})
        self.assertEqual(resp.status_code, 200)

        # and get it back
        resp = self.app.get("/v1/quests/1")
        self.assertEqual(json.loads(resp.data), {
            'creator_id': 1,
            'creator_url': '/v1/users/1',
            'description': 'nip',
            'icon_url': 'rubber',
            'id': 1,
            'url': '/v1/quests/1',
            'name': 'mouse'})

        # list them
        resp = self.app.get("/v1/users/1/quests/")
        self.assertItemsEqual(json.loads(resp.data)['quests'], [
            {'creator_id': 1, 'description': 'nip', 'icon_url': 'rubber',
                'creator_url': '/v1/users/1',
                'url': '/v1/quests/1', 'id': 1, 'name': 'mouse'},
            {'creator_id': 1, 'description': 'blip', 'icon_url': None,
                'creator_url': '/v1/users/1',
                'url': '/v1/quests/2', 'id': 2, 'name': 'blouse'}])

        # delete
        resp = self.app.delete("/v1/quests/1")
        self.assertEqual(resp.status_code, 200)

        # and it's gone
        resp = self.app.get("/v1/quests/1")
        self.assertEqual(resp.status_code, 404)

        resp = self.put_json('/v1/quests/1', {
            'description': 'nip', 'name': 'mouse',
            'icon_url': 'rubber'})
        self.assertEqual(resp.status_code, 404)

        resp = self.app.delete("/v1/quests/1")
        self.assertEqual(resp.status_code, 404)

    @harness.with_sess(user_id=1)
    def test_links(self):
        """Test linking quests and missions together."""

        # create the resources
        harness.create_user(name='snakes')

        resp = self.post_json(
                "/v1/quests/",
                {"name": "mouse", "description": "nip"})
        self.assertEqual(resp.status_code, 200)

        resp = self.post_json(
                "/v1/quests/",
                {"name": "blouse", "description": "blip"})
        self.assertEqual(resp.status_code, 200)

        resp = self.post_json(
                "/v1/missions/",
                {"name": "hat", "description": "snap", "points": 2})
        self.assertEqual(resp.status_code, 200)

        resp = self.post_json(
                "/v1/missions/",
                {"name": "cat", "description": "map", "points": 1})
        self.assertEqual(resp.status_code, 200)

        # no links yet
        resp = self.app.get("/v1/missions/1/quests/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(json.loads(resp.data)['quests'], [])

        # create some links
        resp = self.app.put("/v1/missions/1/quests/1")
        self.assertEqual(resp.status_code, 200)

        resp = self.app.get("/v1/missions/1/quests/")
        self.assertEqual(json.loads(resp.data)['quests'], [
            {"description": "nip", "icon_url": None, "id": 1,
                "name": "mouse", "url": "/v1/quests/1",
                'creator_url': '/v1/users/1', "creator_id": 1}])

        resp = self.app.put("/v1/missions/1/quests/2")
        self.assertEqual(resp.status_code, 200)

        resp = self.app.get("/v1/missions/1/quests/")
        self.assertItemsEqual(json.loads(resp.data)['quests'], [
            {"description": "nip", "icon_url": None, "id": 1,
                "name": "mouse", "url": "/v1/quests/1",
                'creator_url': '/v1/users/1', "creator_id": 1},
            {'creator_id': 1, 'description': 'blip',
                'creator_url': '/v1/users/1',
                'url': '/v1/quests/2', 'icon_url': None,
                'id': 2, 'name': 'blouse'}])

        # still nothing linked to this mission
        resp = self.app.get("/v1/missions/2/quests/")
        self.assertEqual(json.loads(resp.data)['quests'], [])

        # check for idempotency
        resp = self.app.put("/v1/missions/1/quests/2")
        self.assertEqual(resp.status_code, 200)

        resp = self.app.get("/v1/missions/1/quests/")
        self.assertItemsEqual(json.loads(resp.data)['quests'], [
            {"description": "nip", "icon_url": None, "id": 1,
                "name": "mouse", "url": "/v1/quests/1",
                'creator_url': '/v1/users/1', "creator_id": 1},
            {'creator_id': 1, 'description': 'blip',
                'creator_url': '/v1/users/1',
                'url': '/v1/quests/2', 'icon_url': None,
                'id': 2, 'name': 'blouse'}])

        # delete links
        resp = self.app.delete("/v1/missions/1/quests/2")
        self.assertEqual(resp.status_code, 200)

        resp = self.app.get("/v1/missions/1/quests/")
        self.assertEqual(json.loads(resp.data)['quests'], [
            {"description": "nip", "icon_url": None, "id": 1,
                "name": "mouse", "url": "/v1/quests/1",
                'creator_url': '/v1/users/1', "creator_id": 1}])

        resp = self.app.delete("/v1/missions/1/quests/1")
        self.assertEqual(resp.status_code, 200)

        resp = self.app.get("/v1/missions/1/quests/")
        self.assertEqual(json.loads(resp.data)['quests'], [])

        # 404 on non-existent resources
        resp = self.app.delete("/v1/missions/1/quests/20")
        self.assertEqual(resp.status_code, 404)

        resp = self.app.delete("/v1/missions/30/quests/1")
        self.assertEqual(resp.status_code, 404)


if __name__ == '__main__':
    unittest.main()
