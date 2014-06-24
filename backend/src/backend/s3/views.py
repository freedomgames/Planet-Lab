"""Routes dealing with S3 uploads."""

import base64
import hashlib
import hmac
import time
import urllib

import flask

import backend
import backend.common.auth as auth


blueprint = flask.Blueprint('s3', __name__)


def s3_upload_signature(upload_path, mime_type):
    """Return the signature allowing an upload to the given upload path."""
    access_key = backend.app.config['AWS_ACCESS_KEY_ID']
    bucket = backend.app.config['S3_BUCKET']
    secret_key = backend.app.config['AWS_SECRET_ACCESS_KEY']

    expires = int(time.time() + 10)
    amz_headers = "x-amz-acl:public-read"

    put_request = "PUT\n\n%s\n%d\n%s\n/%s/%s" % (
            mime_type, expires, amz_headers, bucket, upload_path)

    signature = base64.encodestring(
            hmac.new(secret_key, put_request, hashlib.sha1).digest())
    signature = urllib.quote_plus(signature.strip())

    url = 'https://%s.s3.amazonaws.com/%s' % (bucket, upload_path)
    request = '%s?AWSAccessKeyId=%s&Expires=%d&Signature=%s' % (
            url, access_key, expires, signature)

    return {'signed_request': request, 'url': url}


@blueprint.route('/sign-avatar-upload')
def sign_avatar_upload():
    """Sign an avatar upload."""
    object_name = flask.request.args.get('s3_object_name')
    mime_type = flask.request.args.get('s3_object_type')

    upload_path = 'avatars/%s/%s' % (auth.current_user_id(), object_name)

    return flask.jsonify(s3_upload_signature(upload_path, mime_type))
