"""Functions for working with S3."""

import boto

import backend

EXPIRES_IN = 10


def get_conn():
    """Return a boto connection object to S3."""
    return boto.connect_s3(
            aws_access_key_id=backend.app.config['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key=backend.app.config['AWS_SECRET_ACCESS_KEY'])


def get_bucket():
    """Return a boto bucket object for the app's S3 bucket."""
    return get_conn().get_bucket(
            backend.app.config['S3_BUCKET'], validate=False)


def s3_upload_signature(upload_path, mime_type):
    """Return the signature allowing an upload to the given upload path."""
    conn = get_conn()
    bucket = backend.app.config['S3_BUCKET']

    url = 'https://%s.s3.amazonaws.com/%s' % (bucket, upload_path)
    signed_request = conn.generate_url(
            EXPIRES_IN, 'PUT', bucket=bucket, key=upload_path, query_auth=True,
            headers={"x-amz-acl": "public-read", 'Content-Type': mime_type})

    return {'url': url, 'signed_request': signed_request}
