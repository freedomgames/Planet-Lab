"""Tests for handling s3."""

import boto.s3.bucket
import boto.s3.key
import datetime
import json
import mock
import unittest

import backend
import backend.common.s3 as s3
import backend.quests.views as quest_views
import harness


class FakeDateTime(datetime.datetime):
    """Mock object to return a constant 'now' time."""
    @staticmethod
    def utcnow():
        """Return a constant 'now' time."""
        return FakeDateTime(2012, 12, 21)


class S3Test(harness.TestHarness):
    """Tests for handling s3."""

    @mock.patch.object(s3.datetime, 'datetime', FakeDateTime)
    def test_s3_upload_signature(self):
        """Test the s3_upload_signature function."""
        signature = s3.s3_upload_signature('snake.png', 'image/png')
        self.assertEqual(signature, {
            'file_name': 'snake.png',
            's3_url': 'https://bucket.s3.amazonaws.com/snake.png',
            'upload_args': {
                'url': 'https://bucket.s3.amazonaws.com/',
                'method': 'POST',
                'data': {
                    'AWSAccessKeyId': 'key',
                    'success_action_status': '201',
                    'acl': 'public-read',
                    'key': 'snake.png',
                    'Content-Type': 'image/png',
                    'Signature': 'kETEObkncWe3ZPmvevjVxVNvojQ=',
                    'Policy': "eyJjb25kaXRpb25zIjogW1siZXEiLCAiJGtleSIsICJz"
                              "bmFrZS5wbmciXSwgeyJidWNrZXQiOiAiYnVja2V0In0s"
                              "IHsiYWNsIjogInB1YmxpYy1yZWFkIn0sIFsiZXEiLCAi"
                              "JENvbnRlbnQtVHlwZSIsICJpbWFnZS9wbmciXSwgeyJzd"
                              "WNjZXNzX2FjdGlvbl9zdGF0dXMiOiAiMjAxIn1dLCAiZX"
                              "hwaXJhdGlvbiI6ICIyMDEyLTEyLTIxVDAxOjAwOjAwLjA"
                              "wMFoifQ=="}}})

    @harness.with_sess(user_id=1)
    def test_sign_avatar_upload(self):
        """Test the sign-avatar-upload route."""

        resp = self.app.get(
                self.url_for(
                    backend.user_views.UserAvatar,
                    user_id='1',
                    file_name='a.png',
                    mime_type='image/png'))
        self.assertEqual(
                json.loads(resp.data)['s3_url'],
                "https://bucket.s3.amazonaws.com/avatars/1/a.png")

    @harness.with_sess(user_id=1)
    def test_sign_quest_upload(self):
        """Test the sign-quest-upload route."""
        resp = self.app.get(
                self.url_for(
                    backend.quest_views.QuestStaticAsset,
                    quest_id='4',
                    file_name='b.png',
                    mime_type='image/png'))
        self.assertEqual(
                json.loads(resp.data)['s3_url'],
                "https://bucket.s3.amazonaws.com/quests/4/b.png")

    @harness.with_sess(user_id=1)
    @mock.patch.object(quest_views.s3, 'get_bucket')
    def test_asset_listing(self, m_get_bucket):
        """Test listing assets for quest uploads."""

        class FakeBucket(object):
            """Mock object for an S3 bucket."""
            bucket = boto.s3.bucket.Bucket(
                    connection=s3.get_conn(), name='bucket')

            def make_key(self, name):
                """Return a key with the given name in the bucket 'bucket'."""
                return boto.s3.key.Key(bucket=self.bucket, name=name)

            def list(self, prefix):
                """Mock list method on the bucket."""
                return [self.make_key(prefix),
                        self.make_key(prefix + 'a'),
                        self.make_key(prefix + 'b')]

        m_get_bucket.return_value = FakeBucket()

        resp = self.app.get(
                self.url_for(
                    backend.quest_views.QuestStaticAssets, quest_id='4'))
        self.assertEqual(json.loads(resp.data), {
            "assets": [
                {"file_name": "a",
                    "url": "https://bucket.s3.amazonaws.com/quests/4/a"},
                {"file_name": "b",
                    "url": "https://bucket.s3.amazonaws.com/quests/4/b"}]})

    @harness.with_sess(user_id=1)
    @mock.patch.object(quest_views.s3, 'get_bucket')
    def test_asset_delete(self, m_get_bucket):
        """Test deleting assets for quest uploads."""

        class FakeBucket(object):
            """Mock object for an S3 bucket."""

            @staticmethod
            def delete_key(key):
                """Assert that 'key' is the correct value."""
                self.assertEqual(key, 'quests/4/a')

        m_get_bucket.return_value = FakeBucket()

        resp = self.app.delete(
                self.url_for(
                    backend.quest_views.QuestStaticAsset,
                    quest_id='4', file_name='a'))
        self.assertEqual(resp.status_code, 200)

if __name__ == '__main__':
    unittest.main()
