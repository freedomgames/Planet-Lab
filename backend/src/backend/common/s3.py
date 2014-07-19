"""Functions for working with S3."""

import base64
import boto
import datetime
import json
import hashlib
import hmac
import pytz

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


def s3_upload_signature(key, mime_type):
    """Return the form data used to POST a file to S3 from the browser."""
    bucket = backend.app.config['S3_BUCKET']
    base_url = 'https://%s.s3.amazonaws.com/' % bucket

    now = datetime.datetime.utcnow().replace(tzinfo=pytz.utc, microsecond=0)
    expires = (now + datetime.timedelta(hours=1)).isoformat()
    # Python's isformat method uses the +00:00 format for the UTC
    # timezone, but Amazon insists upon the alternate 'Z' format
    expires = expires[:-6] + '.000Z'

    policy = {
        "expiration": expires,
        "conditions": [
            ['eq', "$key", key],
            {"bucket": bucket},
            {"acl": "public-read"},
            ['eq', '$Content-Type', mime_type],
            {'success_action_status' : '201'}
        ]
    }
    policy = base64.b64encode(json.dumps(policy).encode('utf-8'))

    signature = hmac.new(
            backend.app.config['AWS_SECRET_ACCESS_KEY'],
            policy.encode('utf-8'),
            hashlib.sha1)
    signature = base64.b64encode(signature.digest())

    return {
            'file_name': key,
            's3_url': base_url + key,
            'upload_args' : {
                'url': base_url,
                'method': 'POST',
                'data': {
                    'key' : key,
                    'acl' : 'public-read',
                    'Content-Type' : mime_type,
                    'Policy': policy,
                    'AWSAccessKeyId': backend.app.config['AWS_ACCESS_KEY_ID'],
                    'success_action_status' : '201',
                    'Signature' : signature
                }
            }
        }
