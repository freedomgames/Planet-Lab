"""Tests for question endpoints."""


import json
import unittest

import backend
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
                {"name": "mouse", "summary": "nap"})
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
            "multiple_choices": [],
            "description": "cat hotel", "question_type": "text",
            "id": 1, "url": "/v1/quests/1/questions/1",
            "creator_id": 1, "creator_url": "/v1/users/1",
            "quest_id": 1, "quest_url": "/v1/quests/1"})

        # or two
        resp = self.post_json(
                "/v1/quests/1/questions/",
                {"question_type": "upload", "description": "snake farm"})
        self.assertEqual(json.loads(resp.data), {
            "multiple_choices": [],
            "description": "snake farm", "question_type": "upload",
            "id": 2, "url": "/v1/quests/1/questions/2",
            "creator_id": 1, "creator_url": "/v1/users/1",
            "quest_id": 1, "quest_url": "/v1/quests/1"})

        # and one more linked to a different quest
        resp = self.post_json(
                "/v1/quests/",
                {"name": "mouse", "summary": "nap"})
        self.assertEqual(resp.status_code, 200)

        resp = self.post_json(
                "/v1/quests/2/questions/",
                {"question_type": "upload", "description": "snake farm"})
        self.assertEqual(resp.status_code, 200)

        # and get them back
        resp = self.app.get("/v1/quests/1/questions/1")
        self.assertEqual(json.loads(resp.data), {
            "multiple_choices": [],
            "description": "cat hotel", "question_type": "text",
            "id": 1, "url": "/v1/quests/1/questions/1",
            "creator_id": 1, "creator_url": "/v1/users/1",
            "quest_id": 1, "quest_url": "/v1/quests/1"})

        resp = self.app.get("/v1/quests/1/questions/2")
        self.assertEqual(resp.status_code, 200)

        resp = self.app.get("/v1/quests/1/questions/")
        self.assertEqual(json.loads(resp.data)['questions'], [
            {"description": "cat hotel", "question_type": "text",
                "id": 1, "url": "/v1/quests/1/questions/1",
                "creator_id": 1, "creator_url": "/v1/users/1",
                "multiple_choices": [],
                "quest_id": 1, "quest_url": "/v1/quests/1"},
            {"description": "snake farm", "question_type": "upload",
                "id": 2, "url": "/v1/quests/1/questions/2",
                "creator_id": 1, "creator_url": "/v1/users/1",
                "multiple_choices": [],
                "quest_id": 1, "quest_url": "/v1/quests/1"}])

        # and get them back with just the id
        resp = self.app.get("/v1/questions/1")
        self.assertEqual(json.loads(resp.data), {
            "description": "cat hotel", "question_type": "text",
            "id": 1, "url": "/v1/quests/1/questions/1",
            "creator_id": 1, "creator_url": "/v1/users/1",
            "multiple_choices": [],
            "quest_id": 1, "quest_url": "/v1/quests/1"})

        # but can't do anything else with that URI
        resp = self.app.post("/v1/questions/1")
        self.assertEqual(resp.status_code, 405)

        resp = self.app.put("/v1/questions/1")
        self.assertEqual(resp.status_code, 405)

        resp = self.app.delete("/v1/questions/1")
        self.assertEqual(resp.status_code, 405)

        # edit
        resp = self.put_json('/v1/quests/1/questions/1', {
            "question_type": "text", 'description': 'a blue house'})
        self.assertEqual(resp.status_code, 200)

        # but we can't change the question_type after creating it
        resp = self.put_json('/v1/quests/1/questions/1', {
            "question_type": "upload", 'description': 'a blue house'})
        self.assertEqual(resp.status_code, 200)

        # and get them back
        resp = self.app.get("/v1/quests/1/questions/1")
        self.assertEqual(json.loads(resp.data), {
            "description": "a blue house", "question_type": "text",
            "id": 1, "url": "/v1/quests/1/questions/1",
            "creator_id": 1, "creator_url": "/v1/users/1",
            "multiple_choices": [],
            "quest_id": 1, "quest_url": "/v1/quests/1"})

        # delete
        resp = self.app.delete("/v1/quests/1/questions/1")
        self.assertEqual(resp.status_code, 200)

        # and it's gone
        resp = self.app.get("/v1/quests/1/questions/1")
        self.assertEqual(resp.status_code, 404)

        resp = self.put_json('/v1/quests/1/questions/1', {
            "question_type": "text", 'description': 'a blue house'})
        self.assertEqual(resp.status_code, 404)

        resp = self.app.delete("/v1/quests/1/questions/1")
        self.assertEqual(resp.status_code, 404)

        # make sure we can't create invalid question types
        resp = self.post_json('/v1/quests/1/questions/', {
            "question_type": "snakes", 'description': 'a blue house'})
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

    @harness.with_sess(user_id=1)
    def test_answer_crud(self):
        """Test CRUD on answer resources."""
        # create a user
        harness.create_user(name='snakes')
        # create a quest
        resp = self.post_json(
                "/v1/quests/",
                {"name": "mouse", "summary": "nap"})
        self.assertEqual(resp.status_code, 200)
        # create some questions
        resp = self.post_json(
                "/v1/quests/1/questions/",
                {"question_type": "text", "description": "cat hotel"})
        self.assertEqual(resp.status_code, 200)
        resp = self.post_json(
                "/v1/quests/1/questions/",
                {"question_type": "upload", "description": "cat upload"})
        self.assertEqual(resp.status_code, 200)

        # link some answers
        resp = self.post_json(
                "/v1/questions/1/answers/", {"answer_text": "cats"})
        self.assertEqual(json.loads(resp.data), {
            "question_type": "text", "answer_text": "cats",
            "answer_upload_url": None,
            "id": 1, "url": "/v1/questions/1/answers/1",
            "creator_id": 1, "creator_url": "/v1/users/1",
            "question_id": 1, "question_url": "/v1/questions/1"})

        resp = self.post_json(
                "/v1/questions/1/answers/",
                {"answer_text": "more cats"})
        self.assertEqual(json.loads(resp.data), {
            "question_type": "text", "answer_text": "more cats",
            "answer_upload_url": None,
            "id": 2, "url": "/v1/questions/1/answers/2",
            "creator_id": 1, "creator_url": "/v1/users/1",
            "question_id": 1, "question_url": "/v1/questions/1"})

        # 400 on invalid combinations of question_type and answer fields
        resp = self.post_json(
                "/v1/questions/1/answers/", {"answer_upload_url": "cats.html"})
        self.assertEqual(resp.status_code, 400)

        resp = self.put_json(
                "/v1/questions/1/answers/1", {"answer_upload_url": "cats.html"})
        self.assertEqual(resp.status_code, 400)

        resp = self.post_json(
                "/v1/questions/2/answers/", {"answer_text": "cats"})
        self.assertEqual(resp.status_code, 400)

        # get them back
        resp = self.app.get('/v1/questions/1/answers/2')
        self.assertEqual(json.loads(resp.data), {
            "question_type": "text", "answer_text": "more cats",
            "answer_upload_url": None,
            "id": 2, "url": "/v1/questions/1/answers/2",
            "creator_id": 1, "creator_url": "/v1/users/1",
            "question_id": 1, "question_url": "/v1/questions/1"})

        resp = self.app.get('/v1/questions/1/answers/')
        self.assertEqual(json.loads(resp.data)['answers'], [
            {"answer_text": "cats", "answer_upload_url": None,
                "creator_id": 1, "creator_url": "/v1/users/1",
                "id": 1, "question_id": 1, "question_type": "text",
                "question_url": "/v1/questions/1",
                "url": "/v1/questions/1/answers/1"},
            {"answer_text": "more cats", "answer_upload_url": None,
                "creator_id": 1, "creator_url": "/v1/users/1", "id": 2,
                "question_id": 1, "question_type": "text",
                "question_url": "/v1/questions/1",
                "url": "/v1/questions/1/answers/2"}])

        # edit
        resp = self.put_json('/v1/questions/1/answers/2', {
            "question_type": "text", "answer_text": "super cat"})
        self.assertEqual(resp.status_code, 200)

        resp = self.app.get('/v1/questions/1/answers/2')
        self.assertEqual(json.loads(resp.data), {
            "question_type": "text", "answer_text": "super cat",
            "answer_upload_url": None,
            "id": 2, "url": "/v1/questions/1/answers/2",
            "creator_id": 1, "creator_url": "/v1/users/1",
            "question_id": 1, "question_url": "/v1/questions/1"})

        # delete
        resp = self.app.delete('/v1/questions/1/answers/2')
        self.assertEqual(resp.status_code, 200)

        resp = self.app.get('/v1/questions/1/answers/2')
        self.assertEqual(resp.status_code, 404)

        # bad question_id / answer_id combos 404
        resp = self.app.get('/v1/questions/1/answers/1')
        self.assertEqual(resp.status_code, 200)

        resp = self.app.get('/v1/questions/100/answers/1')
        self.assertEqual(resp.status_code, 404)

        resp = self.app.put('/v1/questions/100/answers/1')
        self.assertEqual(resp.status_code, 404)

        resp = self.app.delete('/v1/questions/100/answers/1')
        self.assertEqual(resp.status_code, 404)

        resp = self.app.post('/v1/questions/100/answers/')
        self.assertEqual(resp.status_code, 404)

    @harness.with_sess(user_id=1)
    def multiple_choice_test(self):
        """Test the multiple choice resource."""

        # nothing, so 404
        resp = self.app.get(self.url_for(
            backend.question_views.MultipleChoice,
            question_id=1, multiple_choice_id=1))
        self.assertEqual(resp.status_code, 404)

        # create our resources
        harness.create_user(name='snakes')

        resp = self.post_json(
                self.url_for(backend.quest_views.QuestList),
                {"name": "mouse", "summary": "nap"})
        self.assertEqual(resp.status_code, 200)

        resp = self.post_json(
                self.url_for(backend.question_views.QuestionList, parent_id=1),
                {'description': 'q1', 'question_type': 'multiple_choice'})
        self.assertEqual(resp.status_code, 200)

        resp = self.post_json(
                self.url_for(backend.question_views.QuestionList, parent_id=1),
                {'description': 'q2', 'question_type': 'text'})
        self.assertEqual(resp.status_code, 200)

        resp = self.post_json(
                self.url_for(
                    backend.question_views.MultipleChoiceList, parent_id=1),
                {'answer': 'a', 'is_correct': False, 'order': 2})
        self.assertEqual(json.loads(resp.data), {
            "answer": "a", "is_correct": False, 'order': 2,
            "id": 1, "url": "/v1/questions/1/multiple_choices/1",
            "creator_id": 1, "creator_url": "/v1/users/1",
            "question_id": 1, "question_url": "/v1/questions/1"})

        resp = self.post_json(
                self.url_for(
                    backend.question_views.MultipleChoiceList, parent_id=1),
                {'answer': 'b', 'is_correct': True, 'order': 1})
        self.assertEqual(json.loads(resp.data), {
            "answer": "b", "is_correct": True, 'order': 1,
            "id": 2, "url": "/v1/questions/1/multiple_choices/2",
            "creator_id": 1, "creator_url": "/v1/users/1",
            "question_id": 1, "question_url": "/v1/questions/1"})

        # can't add a multiple choice answer to a non-multiple choice question
        resp = self.post_json(
                self.url_for(
                    backend.question_views.MultipleChoiceList, parent_id=2),
                {'answer': 'a', 'is_correct': False, 'order': 3})
        self.assertEqual(resp.status_code, 400)

        # or link to a non-existant question
        resp = self.post_json(
                self.url_for(
                    backend.question_views.MultipleChoiceList, parent_id=20),
                {'answer': 'a', 'is_correct': False, 'order': 3})
        self.assertEqual(resp.status_code, 404)

        # edit
        resp = self.put_json(
                self.url_for(
                    backend.question_views.MultipleChoice,
                    question_id=1, multiple_choice_id=2),
                {'answer': 'bee', 'is_correct': True, 'order': 1})
        self.assertEqual(resp.status_code, 200)

        resp = self.app.get(
                self.url_for(
                    backend.question_views.MultipleChoice,
                    question_id=1, multiple_choice_id=2))
        self.assertEqual(json.loads(resp.data), {
            "answer": "bee", "is_correct": True, 'order': 1,
            "id": 2, "url": "/v1/questions/1/multiple_choices/2",
            "creator_id": 1, "creator_url": "/v1/users/1",
            "question_id": 1, "question_url": "/v1/questions/1"})

        # see them get attached to a question
        resp = self.app.get(
                self.url_for(
                    backend.question_views.Question,
                    quest_id=1, question_id=1))
        self.assertEqual(json.loads(resp.data)['multiple_choices'], [
            {"answer": "bee", "is_correct": True, 'order': 1,
                "id": 2, "url": "/v1/questions/1/multiple_choices/2",
                "creator_id": 1, "creator_url": "/v1/users/1",
                "question_id": 1, "question_url": "/v1/questions/1"},
            {"answer": "a", "is_correct": False, 'order': 2,
                "id": 1, "url": "/v1/questions/1/multiple_choices/1",
                "creator_id": 1, "creator_url": "/v1/users/1",
                "question_id": 1, "question_url": "/v1/questions/1"}])

        resp = self.app.get(
                self.url_for(
                    backend.question_views.MultipleChoiceList, parent_id=1))
        self.assertEqual(json.loads(resp.data), {'multiple_choices': [
            {"answer": "bee", "is_correct": True, 'order': 1,
                "id": 2, "url": "/v1/questions/1/multiple_choices/2",
                "creator_id": 1, "creator_url": "/v1/users/1",
                "question_id": 1, "question_url": "/v1/questions/1"},
            {"answer": "a", "is_correct": False, 'order': 2,
                "id": 1, "url": "/v1/questions/1/multiple_choices/1",
                "creator_id": 1, "creator_url": "/v1/users/1",
                "question_id": 1, "question_url": "/v1/questions/1"}]})

        # make sure order is respected
        resp = self.put_json(
                self.url_for(
                    backend.question_views.MultipleChoice,
                    question_id=1, multiple_choice_id=2),
                {'answer': 'bee', 'is_correct': True, 'order': 3})
        self.assertEqual(resp.status_code, 200)

        resp = self.app.get(
                self.url_for(
                    backend.question_views.Question, quest_id=1, question_id=1))
        self.assertEqual(json.loads(resp.data)['multiple_choices'], [
            {"answer": "a", "is_correct": False, 'order': 2,
                "id": 1, "url": "/v1/questions/1/multiple_choices/1",
                "creator_id": 1, "creator_url": "/v1/users/1",
                "question_id": 1, "question_url": "/v1/questions/1"},
            {"answer": "bee", "is_correct": True, 'order': 3,
                "id": 2, "url": "/v1/questions/1/multiple_choices/2",
                "creator_id": 1, "creator_url": "/v1/users/1",
                "question_id": 1, "question_url": "/v1/questions/1"}])

        # delete
        resp = self.app.delete(
                self.url_for(
                    backend.question_views.MultipleChoice,
                    question_id=1, multiple_choice_id=2))
        self.assertEqual(resp.status_code, 200)

        resp = self.app.get(
                self.url_for(
                    backend.question_views.Question, quest_id=1, question_id=1))
        self.assertEqual(json.loads(resp.data)['multiple_choices'], [
            {"answer": "a", "is_correct": False, 'order': 2,
                "id": 1, "url": "/v1/questions/1/multiple_choices/1",
                "creator_id": 1, "creator_url": "/v1/users/1",
                "question_id": 1, "question_url": "/v1/questions/1"}])

        resp = self.app.get(
                self.url_for(
                    backend.question_views.MultipleChoice,
                    question_id=1, multiple_choice_id=2))
        self.assertEqual(resp.status_code, 404)


if __name__ == '__main__':
    unittest.main()
