"""Routes dealing with S3 uploads."""

import flask

import boto
import backend
import backend.common.auth as auth


EXPIRES_IN = 10

blueprint = flask.Blueprint('s3', __name__)


def get_s3_conn():
    """Return a boto connection object to S3."""
    access_key = backend.app.config['AWS_ACCESS_KEY_ID']
    secret_key = backend.app.config['AWS_SECRET_ACCESS_KEY']

    return boto.connect_s3(
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key)


def s3_upload_signature(upload_path, mime_type):
    """Return the signature allowing an upload to the given upload path."""
    conn = get_s3_conn()
    bucket = backend.app.config['S3_BUCKET']

    url = 'https://%s.s3.amazonaws.com/%s' % (bucket, upload_path)
    signed_request = conn.generate_url(
            EXPIRES_IN, 'PUT', bucket=bucket, key=upload_path, query_auth=True,
            headers={"x-amz-acl": "public-read", 'Content-Type': mime_type})

    return {'url': url, 'signed_request': signed_request}


@blueprint.route('/sign-avatar-upload')
def sign_avatar_upload():
    """Sign an avatar upload."""
    file_name = flask.request.args['file_name']
    mime_type = flask.request.args['mime_type']
    upload_path = 'avatars/%s/%s' % (auth.current_user_id(), file_name)
    return flask.jsonify(s3_upload_signature(upload_path, mime_type))


@blueprint.route('/sign-quest-upload')
def sign_quest_upload():
    """Sign an upload for quest assets."""
    file_name = flask.request.args['file_name']
    mime_type = flask.request.args['mime_type']
    quest_id = flask.request.args['quest_id']
    upload_path = 'quests/%s/%s' % (quest_id, file_name)
    return flask.jsonify(s3_upload_signature(upload_path, mime_type))
