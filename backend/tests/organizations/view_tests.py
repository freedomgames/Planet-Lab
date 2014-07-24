"""Tests for organization endpoints."""


import json
import unittest

import backend
import harness


class OrganizationTest(harness.TestHarness):
    """Tests for organization endpoints."""

    @harness.with_sess(user_id=1)
    def test_crud(self):
        """Basic CRUD tests."""
        # create a user
        harness.create_user(name='snakes')

        # no quest yet, so 404
        resp = self.app.get("/v1/organizations/1")
        self.assertEqual(resp.status_code, 404)

        # create an org
        resp = self.post_json(
                self.url_for(backend.organization_views.OrganizationList),
                {"name": "hotel", "description": "cat hotel house"})
        self.assertEqual(resp.status_code, 200)

        # and get it back
        resp = self.app.get("/v1/organizations/1")
        self.assertEqual(json.loads(resp.data), {
            "description": "cat hotel house",
            "icon_url": None,
            "id": 1,
            "members": [],
            "name": "hotel",
            "url": "/v1/organizations/1",
            "creator_url": "/v1/users/1",
            "creator_id": 1})

        # edit
        resp = self.put_json('/v1/organizations/1', {
            'name': 'hotel', 'description': 'cat hotel house',
            'icon_url': 'rubber'})
        self.assertEqual(resp.status_code, 200)

        # and get it back
        resp = self.app.get("/v1/organizations/1")
        self.assertEqual(json.loads(resp.data), {
            "description": "cat hotel house",
            "icon_url": 'rubber',
            "id": 1,
            "members": [],
            "name": "hotel",
            "url": "/v1/organizations/1",
            "creator_url": "/v1/users/1",
            "creator_id": 1})

        # delete
        resp = self.app.delete("/v1/organizations/1")
        self.assertEqual(resp.status_code, 200)

        # and it's gone
        resp = self.app.get("/v1/organizations/1")
        self.assertEqual(resp.status_code, 404)

        resp = self.put_json('/v1/organizations/1', {
            'name': 'hotel', 'description': 'cat hotel house',
            'icon_url': 'rubber'})
        self.assertEqual(resp.status_code, 404)

        resp = self.app.delete("/v1/organizations/1")
        self.assertEqual(resp.status_code, 404)

    @harness.with_sess(user_id=1)
    def test_links(self):
        """Test linking users and organizations together."""

        # create the resources
        harness.create_user(name='snakes', avatar_url='snakes.png')
        harness.create_user(name='rakes', avatar_url='rakes.png')

        resp = self.post_json(
                self.url_for(backend.organization_views.OrganizationList),
                {"name": "mouse", "description": "nip"})
        self.assertEqual(resp.status_code, 200)

        resp = self.post_json(
                self.url_for(backend.organization_views.OrganizationList),
                {"name": "blouse", "description": "blip"})
        self.assertEqual(resp.status_code, 200)

        # no links yet
        resp = self.app.get("/v1/organizations/1")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(json.loads(resp.data)['members'], [])

        resp = self.app.get("/v1/organizations/2")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(json.loads(resp.data)['members'], [])

        # create some links
        resp = self.app.put("/v1/organizations/1/users/1")
        self.assertEqual(resp.status_code, 200)

        resp = self.app.put("/v1/organizations/1/users/2")
        self.assertEqual(resp.status_code, 200)

        resp = self.app.put("/v1/organizations/2/users/2")
        self.assertEqual(resp.status_code, 200)

        # see the links on the organizations
        resp = self.app.get("/v1/organizations/1")
        self.assertEqual(json.loads(resp.data)['members'], [
            {"id": 1, "name": "snakes",
                "url": "/v1/users/1", "avatar_url": 'snakes.png'},
            {"id": 2, "name": "rakes",
                "url": "/v1/users/2", "avatar_url": 'rakes.png'}])

        resp = self.app.get("/v1/organizations/2")
        self.assertEqual(json.loads(resp.data)['members'], [
            {"id": 2, "name": "rakes",
                "url": "/v1/users/2", "avatar_url": 'rakes.png'}])

        # and on the users
        resp = self.app.get("/v1/users/1")
        self.assertEqual(json.loads(resp.data)['organizations'], [
            {'id': 1, 'name': 'mouse', 'icon_url': None,
                'url': '/v1/organizations/1'}])

        resp = self.app.get("/v1/users/2")
        self.assertEqual(json.loads(resp.data)['organizations'], [
            {'id': 1, 'name': 'mouse', 'icon_url': None,
                'url': '/v1/organizations/1'},
            {'id': 2, 'name': 'blouse', 'icon_url': None,
                'url': '/v1/organizations/2'}])

        # check idempotency
        resp = self.app.put("/v1/organizations/1/users/1")
        self.assertEqual(resp.status_code, 200)

        resp = self.app.get("/v1/organizations/1")
        self.assertEqual(json.loads(resp.data)['members'], [
            {"id": 1, "name": "snakes",
                "url": "/v1/users/1", "avatar_url": 'snakes.png'},
            {"id": 2, "name": "rakes",
                "url": "/v1/users/2", "avatar_url": 'rakes.png'}])

        resp = self.app.get("/v1/organizations/2")
        self.assertEqual(json.loads(resp.data)['members'], [
            {"id": 2, "name": "rakes",
                "url": "/v1/users/2", "avatar_url": 'rakes.png'}])

        # delete a link
        resp = self.app.delete("/v1/organizations/1/users/2")
        self.assertEqual(resp.status_code, 200)

        # and it's gone
        resp = self.app.get("/v1/organizations/1")
        self.assertEqual(json.loads(resp.data)['members'], [
            {"id": 1, "name": "snakes",
                "url": "/v1/users/1", "avatar_url": 'snakes.png'}])

        resp = self.app.get("/v1/organizations/2")
        self.assertEqual(json.loads(resp.data)['members'], [
            {"id": 2, "name": "rakes",
                "url": "/v1/users/2", "avatar_url": 'rakes.png'}])


if __name__ == '__main__':
    unittest.main()
