"""Views for users."""


import flask.ext.restful as restful
import flask.ext.restful.reqparse as reqparse

import backend
import backend.common.resource as resource
import backend.users.models as user_models



class User(resource.SimpleResource):
    """Views for a single user resource."""

    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True)
    parser.add_argument('organization', type=str)
    parser.add_argument('avatar_url', type=str)

    view_fields = ['id', 'name', 'organization', 'avatar_url']

    def as_dict(self, user, user_id):
        """Return a serializable dictionary representing the given user."""
        return {field: getattr(user, field) for field in self.view_fields}

    @staticmethod
    def query(user_id):
        """Return the query to select the user with the given id."""
        return user_models.User.query.filter_by(id=user_id)


class UserList(restful.Resource):
    """Views for user creation."""

    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True)
    parser.add_argument('organization', type=str)
    parser.add_argument('avatar_url', type=str)

    def post(self):
        """Create a new user and return its id."""
        args = self.parser.parse_args()
        user = user_models.User(**args)

        backend.db.session.add(user)
        backend.db.session.commit()

        args['id'] = user.id

        return args
