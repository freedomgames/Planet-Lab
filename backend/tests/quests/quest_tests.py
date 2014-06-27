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
                {"name": "mouse", "summary": "nip",
                    "inquiry_questions": ['a', 'b']})
        self.assertEqual(json.loads(resp.data), {
            "name": "mouse", "summary": "nip", "inquiry_questions": ["a", "b"],
            "icon_url": None, "video_links": [],
            "id": 1, "url": "/v1/quests/1",
            "pbl_description": None, "mentor_guide": None,
            "min_grade_level": None, "max_grade_level": None,
            "hours_required": None, "minutes_required": None,
            "creator_id": 1, "creator_url": "/v1/users/1"})
        self.assertEqual(resp.status_code, 200)
        resp = self.post_json(
                "/v1/quests/",
                {"name": "blouse", "summary": "blip"})
        self.assertEqual(resp.status_code, 200)

        # create this one as a different user
        self.update_session(user_id=2)
        resp = self.post_json(
                "/v1/quests/",
                {"name": "house", "summary": "snip", "icon_url": "blue"})
        self.assertEqual(resp.status_code, 200)
        self.update_session(user_id=1)

        # and get it back
        resp = self.app.get("/v1/quests/1")
        self.assertEqual(json.loads(resp.data), {
            'creator_id': 1,
            'creator_url': '/v1/users/1',
            'summary': 'nip',
            'icon_url': None,
            "inquiry_questions": ["a", "b"],
            "pbl_description": None, "mentor_guide": None,
            "min_grade_level": None, "max_grade_level": None,
            "hours_required": None, "minutes_required": None,
            'id': 1,
            'video_links': [],
            'url': '/v1/quests/1',
            'name': 'mouse'})

        # edit
        resp = self.put_json('/v1/quests/1', {
            'summary': 'nip', 'name': 'mouse', 'icon_url': 'rubber',
            "pbl_description": 'p', "mentor_guide": 'g',
            "min_grade_level": 1, "max_grade_level": 2,
            "hours_required": 3, "minutes_required": 4,
            "video_links": ['snakes.mp4', 'ladders.mp4'],
            'inquiry_questions': ['b', 'c', 'd']})
        self.assertEqual(resp.status_code, 200)

        # and get it back
        resp = self.app.get("/v1/quests/1")
        self.assertEqual(json.loads(resp.data), {
            'creator_id': 1,
            'creator_url': '/v1/users/1',
            'summary': 'nip',
            "pbl_description": 'p', "mentor_guide": 'g',
            "min_grade_level": 1, "max_grade_level": 2,
            "hours_required": 3, "minutes_required": 4,
            'icon_url': 'rubber',
            "video_links": ['snakes.mp4', 'ladders.mp4'],
            "inquiry_questions": ["b", "c", "d"],
            'id': 1,
            'url': '/v1/quests/1',
            'name': 'mouse'})

        # list them
        resp = self.app.get("/v1/users/1/quests/")
        self.assertItemsEqual(json.loads(resp.data)['quests'], [
            {'creator_id': 1, 'summary': 'nip', 'icon_url': 'rubber',
                'creator_url': '/v1/users/1',
                "inquiry_questions": ["b", "c", "d"],
                "pbl_description": 'p', "mentor_guide": 'g',
                "min_grade_level": 1, "max_grade_level": 2,
                "hours_required": 3, "minutes_required": 4,
                "video_links": ['snakes.mp4', 'ladders.mp4'],
                'url': '/v1/quests/1', 'id': 1, 'name': 'mouse'},
            {'creator_id': 1, 'summary': 'blip', 'icon_url': None,
                'creator_url': '/v1/users/1', 'video_links': [],
                "inquiry_questions": [],
                "pbl_description": None, "mentor_guide": None,
                "min_grade_level": None, "max_grade_level": None,
                "hours_required": None, "minutes_required": None,
                'url': '/v1/quests/2', 'id': 2, 'name': 'blouse'}])

        # delete
        resp = self.app.delete("/v1/quests/1")
        self.assertEqual(resp.status_code, 200)

        # and it's gone
        resp = self.app.get("/v1/quests/1")
        self.assertEqual(resp.status_code, 404)

        resp = self.put_json('/v1/quests/1', {
            'summary': 'nip', 'name': 'mouse',
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
                {"name": "mouse", "summary": "nip"})
        self.assertEqual(resp.status_code, 200)

        resp = self.post_json(
                "/v1/quests/",
                {"name": "blouse", "summary": "blip"})
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
            {"summary": "nip", "icon_url": None, "id": 1,
                "name": "mouse", "url": "/v1/quests/1", 'video_links': [],
                'inquiry_questions': [],
                "pbl_description": None, "mentor_guide": None,
                "min_grade_level": None, "max_grade_level": None,
                "hours_required": None, "minutes_required": None,
                'creator_url': '/v1/users/1', "creator_id": 1}])

        resp = self.app.put("/v1/missions/1/quests/2")
        self.assertEqual(resp.status_code, 200)

        resp = self.app.get("/v1/missions/1/quests/")
        self.assertItemsEqual(json.loads(resp.data)['quests'], [
            {"summary": "nip", "icon_url": None, "id": 1,
                "name": "mouse", "url": "/v1/quests/1", 'video_links': [],
                'inquiry_questions': [],
                "pbl_description": None, "mentor_guide": None,
                "min_grade_level": None, "max_grade_level": None,
                "hours_required": None, "minutes_required": None,
                'creator_url': '/v1/users/1', "creator_id": 1},
            {'creator_id': 1, 'summary': 'blip',
                'creator_url': '/v1/users/1', 'video_links': [],
                'inquiry_questions': [],
                "pbl_description": None, "mentor_guide": None,
                "min_grade_level": None, "max_grade_level": None,
                "hours_required": None, "minutes_required": None,
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
            {"summary": "nip", "icon_url": None, "id": 1,
                "name": "mouse", "url": "/v1/quests/1", 'video_links': [],
                'inquiry_questions': [],
                "pbl_description": None, "mentor_guide": None,
                "min_grade_level": None, "max_grade_level": None,
                "hours_required": None, "minutes_required": None,
                'creator_url': '/v1/users/1', "creator_id": 1},
            {'creator_id': 1, 'summary': 'blip',
                'creator_url': '/v1/users/1', 'video_links': [],
                'inquiry_questions': [],
                "pbl_description": None, "mentor_guide": None,
                "min_grade_level": None, "max_grade_level": None,
                "hours_required": None, "minutes_required": None,
                'url': '/v1/quests/2', 'icon_url': None,
                'id': 2, 'name': 'blouse'}])

        # delete links
        resp = self.app.delete("/v1/missions/1/quests/2")
        self.assertEqual(resp.status_code, 200)

        resp = self.app.get("/v1/missions/1/quests/")
        self.assertEqual(json.loads(resp.data)['quests'], [
            {"summary": "nip", "icon_url": None, "id": 1,
                "name": "mouse", "url": "/v1/quests/1", 'video_links': [],
                'inquiry_questions': [],
                "pbl_description": None, "mentor_guide": None,
                "min_grade_level": None, "max_grade_level": None,
                "hours_required": None, "minutes_required": None,
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
