"""Tests for the s3 module."""

import flask
import json
import unittest

import backend
import harness


class S3Test(harness.TestHarness):
    """Tests for the s3 module."""

    @harness.with_sess(user_id=1)
    def test_sign_avatar_upload(self):
        """Test the sign-avatar-upload route."""

        with backend.app.test_request_context():
            resp = self.app.get(
                    flask.url_for(
                        's3.sign_avatar_upload',
                        file_name='a.png',
                        mime_type='image/png'))
            self.assertEqual(
                    json.loads(resp.data)['url'],
                    "https://bucket.s3.amazonaws.com/avatars/1/a.png")

    def test_sign_quest_upload(self):
        """Test the sign-quest-upload route."""

        with backend.app.test_request_context():
            resp = self.app.get(
                    flask.url_for(
                        's3.sign_quest_upload',
                        quest_id='4',
                        file_name='b.png',
                        mime_type='image/png'))
            self.assertEqual(
                    json.loads(resp.data)['url'],
                    "https://bucket.s3.amazonaws.com/quests/4/b.png")


if __name__ == '__main__':
    unittest.main()
