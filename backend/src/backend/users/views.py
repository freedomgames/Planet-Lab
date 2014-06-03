"""Views for users."""


import flask
import flask.ext.restful as restful
import flask.ext.restful.reqparse as reqparse

import backend
import backend.users.models as user_models


class UserBase(restful.Resource):
    """Define a parser for other resources to use."""
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True)
    parser.add_argument('organization', type=str)
    parser.add_argument('avatar_url', type=str)


class User(UserBase):
    """Views for a single user resource."""

    view_fields = ['id', 'name', 'organization', 'avatar_url']

    def get(self, id_):
        """Return a single user by id."""
        user = user_models.User.query.get(id_)
        if user is None:
            return flask.Response('', 404)
        else:
            return {field: getattr(user, field) for field in self.view_fields}

    def put(self, id_):
        """Update a user."""
        args = self.parser.parse_args()
        rows_updated = user_models.User.query.filter_by(id=id_).update(args)
        backend.db.session.commit()

        if not rows_updated:
            return flask.Response('', 404)
        else:
            return args

    def delete(self, id_):
        """Delete a user."""
        rows_deleted = user_models.User.query.filter_by(id=id_).delete()
        backend.db.session.commit()

        if not rows_deleted:
            return flask.Response('', 404)


class UserList(UserBase):
    """Views for user creation."""

    def post(self):
        """Create a new user and return its id."""
        args = self.parser.parse_args()
        user = user_models.User(**args)

        backend.db.session.add(user)
        backend.db.session.commit()

        args['id'] = user.id

        return args
