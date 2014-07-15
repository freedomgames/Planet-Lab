"""Views for users."""


import flask
import flask_restful

import backend.common.resource as resource
import backend.common.s3 as s3
import backend.users.models as user_models


class UserBase(object):
    """Provide a shared as_dict method and a parser."""

    parser = resource.RequestParser()
    parser.add_argument('name', type=str)
    parser.add_argument('email', type=str)
    parser.add_argument('description', type=str)
    parser.add_argument('avatar_url', type=str)

    view_fields = ('id', 'name', 'avatar_url', 'url')
    organization_fields = ('id', 'url', 'name', 'icon_url')

    def as_dict(self, user):
        """Return a serializable dictionary representing the given user."""
        resp = {field: getattr(user, field) for field in self.view_fields}
        resp['organizations'] = [{field: getattr(organization, field) for
            field in self.organization_fields} for
            organization in user.organizations]
        return resp


class User(UserBase, resource.SimpleResource):
    """Views for a single user resource."""

    @staticmethod
    def query(user_id):
        """Return the query to select the user with the given id."""
        return user_models.User.query.filter_by(id=user_id)

class UserAvatar(flask_restful.Resource):
    """Handle signing of avatar upload requests."""

    @staticmethod
    def get(user_id, file_name):
        """Return a signed request to upload the given file name to
        as the given user's avatar.
        """
        mime_type = flask.request.args['mime_type']
        upload_path = 'avatars/%s/%s' % (user_id, file_name)
        return s3.s3_upload_signature(upload_path, mime_type)
