"""Test the common.models module."""


import unittest

import backend
import backend.common.models as models


class TestCreatedBy(unittest.TestCase):
    """Test the CreatedBy class."""

    def test_creator_url(self):
        """Test our creator_url mehtod."""

        class MockCreatedBy(models.CreatedBy):
            """Turn creator_id into a regular attribute."""
            def __init__(self, creator_id):
                self.c_id = creator_id

            @property
            def creator_id(self):
                """Turn creator_id into a regular attribute."""
                return self.c_id

        with backend.app.test_request_context():
            created_by = MockCreatedBy(None)
            self.assertEqual(created_by.creator_url, None)

            created_by = MockCreatedBy(2)
            self.assertEqual(created_by.creator_url, '/v1/users/2')


if __name__ == '__main__':
    unittest.main()

