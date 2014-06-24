"""Tests for the s3 module."""

import mock
import unittest

import backend.s3.views as views

class S3Test(unittest.TestCase):
    """Tests for the s3 module."""

    @mock.patch.object(views.time, 'time', new=lambda: 10)
    def test_s3_upload_signature(self):
        """Test the s3_upload_signature function."""
        self.assertEqual(
                views.s3_upload_signature('avatar/1.png', 'image/png'),
                {'signed_request': 'https://bucket.s3.amazonaws.com/'
                'avatar/1.png?AWSAccessKeyId=key&Expires=20&'
                'Signature=egV1xrhN1pmw6njWiC6e%2FPecWLs%3D',
                'url': 'https://bucket.s3.amazonaws.com/avatar/1.png'})


if __name__ == '__main__':
    unittest.main()
