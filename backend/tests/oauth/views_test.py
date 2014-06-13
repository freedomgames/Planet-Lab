"""Tests for handling OAuth responses."""

import mock
import unittest

import backend
import backend.oauth.views as views
import backend.users.models as user_models
import harness


class OAuthTest(harness.TestHarness):
    """Tests for handling OAuth responses."""

    def test_get_or_create_google_user(self):
        """Make sure get_or_create_google_user creates and retrieves
        existing users appropriately.
        """
        # a new user
        self.assertEqual(1, views.get_or_create_google_user('token', {
            'id': '4a', 'email': 'email', 'name': 'name'}))
        # same id, so should return the same user id
        self.assertEqual(1, views.get_or_create_google_user('token', {
            'id': '4a', 'email': 'email', 'name': 'name'}))
        # new id, so should be a new user id
        self.assertEqual(2, views.get_or_create_google_user('token', {
            'id': '7d', 'email': 'email', 'name': 'name'}))
        # idempotency check again
        self.assertEqual(2, views.get_or_create_google_user('token', {
            'id': '7d', 'email': 'email', 'name': 'name'}))

    def test_google_access_token(self):
        """Test the google_access_token function."""
        self.assertEqual(1, views.get_or_create_google_user('token1', {
            'id': '4a', 'email': 'email', 'name': 'name'}))

        self.assertEqual(2, views.get_or_create_google_user('token2', {
            'id': '7d', 'email': 'email', 'name': 'name'}))

        with mock.patch.object(views, 'flask', new=mock.Mock(session={})):
            self.assertEqual(None, views.google_access_token())

        with mock.patch.object(
                views, 'flask', new=mock.Mock(session={'user_id': 1})):
            self.assertEqual(('token1', ''), views.google_access_token())

        with mock.patch.object(
                views, 'flask', new=mock.Mock(session={'user_id': 2})):
            self.assertEqual(('token2', ''), views.google_access_token())

if __name__ == '__main__':
    unittest.main()

