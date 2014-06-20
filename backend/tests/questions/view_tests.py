"""Tests for organization endpoints."""


import json
import unittest

import harness


class QuestionTest(harness.TestHarness):
    """Tests for question endpoints."""

    @harness.with_sess(user_id=1)
    def test_crud(self):
        """Basic CRUD tests."""
        # create a user
        harness.create_user(name='snakes')
        # create a quest
        resp = self.post_json(
                "/v1/quests/",
                {"name": "mouse", "description": "nap"})
        self.assertEqual(resp.status_code, 200)

        # no questions yet
        resp = self.app.get("/v1/quests/1/questions/1")
        self.assertEqual(resp.status_code, 404)

        resp = self.app.get("/v1/quests/1/questions/")
        self.assertEqual(json.loads(resp.data)['questions'], [])

        # create a resource
        resp = self.post_json(
                "/v1/quests/1/questions/",
                {"question_type": "text", "description": "cat hotel"})
        self.assertEqual(json.loads(resp.data), {
            "description": "cat hotel", "question_type": "text",
            "id": 1, "url": "/v1/quests/1/questions/1",
            "creator": 1, "creator_url": "/v1/users/1",
            "quest_id": 1, "quest_url": "/v1/quests/1"})

        # or two
        resp = self.post_json(
                "/v1/quests/1/questions/",
                {"question_type": "upload", "description": "snake farm"})
        self.assertEqual(json.loads(resp.data), {
            "description": "snake farm", "question_type": "upload",
            "id": 2, "url": "/v1/quests/1/questions/2",
            "creator": 1, "creator_url": "/v1/users/1",
            "quest_id": 1, "quest_url": "/v1/quests/1"})

        # and one more linked to a different quest
        resp = self.post_json(
                "/v1/quests/",
                {"name": "mouse", "description": "nap"})
        self.assertEqual(resp.status_code, 200)

        resp = self.post_json(
                "/v1/quests/2/questions/",
                {"question_type": "upload", "description": "snake farm"})
        self.assertEqual(resp.status_code, 200)

        # and get them back
        resp = self.app.get("/v1/quests/1/questions/1")
        self.assertEqual(json.loads(resp.data), {
            "description": "cat hotel", "question_type": "text",
            "id": 1, "url": "/v1/quests/1/questions/1",
            "creator": 1, "creator_url": "/v1/users/1",
            "quest_id": 1, "quest_url": "/v1/quests/1"})

        resp = self.app.get("/v1/quests/1/questions/2")
        self.assertEqual(resp.status_code, 200)

        resp = self.app.get("/v1/quests/1/questions/")
        self.assertEqual(json.loads(resp.data)['questions'], [
            {"description": "cat hotel", "question_type": "text",
                "id": 1, "url": "/v1/quests/1/questions/1",
                "creator": 1, "creator_url": "/v1/users/1",
                "quest_id": 1, "quest_url": "/v1/quests/1"},
            {"description": "snake farm", "question_type": "upload",
                "id": 2, "url": "/v1/quests/1/questions/2",
                "creator": 1, "creator_url": "/v1/users/1",
                "quest_id": 1, "quest_url": "/v1/quests/1"}])

        # edit
        resp = self.put_json('/v1/quests/1/questions/1', {
            "question_type": "text", 'description': 'a blue house'})
        self.assertEqual(resp.status_code, 200)

        # and get them back
        resp = self.app.get("/v1/quests/1/questions/1")
        self.assertEqual(json.loads(resp.data), {
            "description": "a blue house", "question_type": "text",
            "id": 1, "url": "/v1/quests/1/questions/1",
            "creator": 1, "creator_url": "/v1/users/1",
            "quest_id": 1, "quest_url": "/v1/quests/1"})


        # delete
        resp = self.app.delete("/v1/quests/1/questions/1")
        self.assertEqual(resp.status_code, 200)

        # and it's gone
        resp = self.app.get("/v1/quests/1/questions/1")
        self.assertEqual(resp.status_code, 404)

        resp = self.put_json("/v1/quests/1/questions/1", {'description': 'a'})
        self.assertEqual(resp.status_code, 404)

        resp = self.app.delete("/v1/quests/1/questions/1")
        self.assertEqual(resp.status_code, 404)

        # make sure we handled enums properly
        resp = self.put_json("/v1/quests/1/questions/2", {'question_type': 'a'})
        self.assertEqual(resp.status_code, 400)

        # and 404 on bad quest ids
        resp = self.app.get("/v1/quests/1/questions/2")
        self.assertEqual(resp.status_code, 200)

        resp = self.app.get("/v1/quests/2/questions/2")
        self.assertEqual(resp.status_code, 404)

        resp = self.post_json(
                "/v1/quests/20/questions/",
                {"question_type": "upload", "description": "snake farm"})
        self.assertEqual(resp.status_code, 404)

        resp = self.app.get("/v1/quests/20/questions/")
        self.assertEqual(resp.status_code, 404)

        # cascade delete on quests to linked questions
        resp = self.app.get("/v1/quests/1/questions/2")
        self.assertEqual(resp.status_code, 200)

        resp = self.app.delete("/v1/quests/1")
        self.assertEqual(resp.status_code, 200)

        resp = self.app.get("/v1/quests/1/questions/2")
        self.assertEqual(resp.status_code, 404)


if __name__ == '__main__':
    unittest.main()
