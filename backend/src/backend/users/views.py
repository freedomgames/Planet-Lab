"""Views for users."""


import flask.ext.restful as restful
import flask.ext.restful.reqparse as reqparse

import backend
import backend.common.resource as resource
import backend.users.models as user_models


class UserBase(object):
    """Provide a shared as_dict method."""

    view_fields = ('id', 'name', 'avatar_url', 'url')
    organization_fields = ('id', 'url', 'name', 'icon_url')

    def as_dict(self, user, user_id):
        """Return a serializable dictionary representing the given user."""
        resp = {field: getattr(user, field) for field in self.view_fields}
        resp['organizations'] = [{field: getattr(organization, field) for
            field in self.organization_fields} for
            organization in user.organizations]
        return resp


class User(UserBase, resource.SimpleResource):
    """Views for a single user resource."""

    parser = resource.ProvidedParser()
    parser.add_argument('name', type=str)
    parser.add_argument('avatar_url', type=str)

    @staticmethod
    def query(user_id):
        """Return the query to select the user with the given id."""
        return user_models.User.query.filter_by(id=user_id)


class UserList(UserBase, restful.Resource):
    """Views for user creation."""

    parser = resource.ProvidedParser()
    parser.add_argument('name', type=str, required=True)
    parser.add_argument('avatar_url', type=str)

    def post(self):
        """Create a new user and return its id."""
        args = self.parser.parse_args()
        user = user_models.User(**args)

        backend.db.session.add(user)
        backend.db.session.commit()

        return self.as_dict(user, user.id)
