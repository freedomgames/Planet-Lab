"""Common tools for building restful resources."""


import flask
import flask_restful
import flask_restful.reqparse as reqparse
import sqlalchemy
import sqlalchemy.orm as orm

import backend
import backend.common.auth as auth


NOTHING = object()


class ProvidedParser(reqparse.RequestParser):
    """A subclass which allows us to discriminate between lack of
    values from a caller and default values for keys.

    That is, if a parser is created like so:

    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str)
    parser.add_argument('description', type=str)

    parser.parse_args() may return
    {"name": "sam", "description": None}

    whether the caller provided either
    {"name": "sam"} or {"name": "sam", "description": null}

    We remove this ambiguity by returning
    {"name": "sam"} in the first case and
    {"name": "sam", "description": None} in the second

    If a default value is given in and add_argument() call, that
    field will always be present whether it was supplied or not.
    """

    def add_argument(self, *args, **kwargs):
        """If not given by the caller, add a default value of 'nothing'
        to a field so we can tell if a user has provided a value for it.
        """
        if 'default' not in kwargs:
            kwargs['default'] = NOTHING
        super(ProvidedParser, self).add_argument(*args, **kwargs)

    def parse_args(self):
        """Return the dictionary from parse_args() without
        entries which were given no value by the caller.
        """
        args = super(ProvidedParser, self).parse_args()
        return {key: value for key, value in args.iteritems() if
                value is not NOTHING}


class SimpleResource(flask_restful.Resource):
    """Base class defining the simplest common set of CRUD endpoints
    for working with single resources.
    """
    # Child classes need to define a reqparse.RequestParser instance
    # for the parser attribute to be used when parsing PUT requests.
    parser = None

    @staticmethod
    def query(*args, **kwargs):
        """Needs to be implemented by child classes.  Should return
        a query to select the row being operated upon by the GET,
        PUT and DELETE verbs.
        """
        raise NotImplementedError

    @staticmethod
    def as_dict(*args, **kwargs):
        """Needs to be implemented by child classes.  Given an object,
        returns a serializable dictionary representing that object to
        be returned on GET's.
        """
        raise NotImplementedError

    def get(self, *args, **kwargs):
        """Return a serialization of the resource or a 404."""
        resource = self.query(*args, **kwargs).first()
        if resource is None:
            return flask.Response('', 404)
        else:
            return self.as_dict(resource, *args, **kwargs)

    def put(self, *args, **kwargs):
        """Update a resource."""
        update = self.parser.parse_args()
        if not update:
            return flask.Response('', 400)
        else:
            rows_updated = self.query(*args, **kwargs).update(
                    update, synchronize_session=False)
            backend.db.session.commit()

            if not rows_updated:
                return flask.Response('', 404)
            else:
                return args

    def delete(self, *args, **kwargs):
        """Delete a quest."""
        rows_deleted = self.query(*args, **kwargs).delete(
                synchronize_session=False)
        backend.db.session.commit()

        if not rows_deleted:
            return flask.Response('', 404)


class ManyToOneLink(flask_restful.Resource):
    """Resource dealing with creating and listing a resource linked
    to one single other resource.
    """
    # child classes need to override all of these
    parent_id_name = None
    child_link_name = None
    resource_type = lambda *args, **kwargs: None
    parent_resource_type = None
    parser = None

    @staticmethod
    def as_dict(*args, **kwargs):
        """Needs to be implemented by child classes.  Given an object,
        returns a serializable dictionary representing that object to
        be returned on GET's.
        """
        raise NotImplementedError


    def post(self, parent_id):
        """Create a new resource and link it to its creator and parent."""
        args = self.parser.parse_args()
        args['creator_id'] = auth.current_user_id()
        args[self.parent_id_name] = parent_id
        new_resource = self.resource_type(**args)

        try:
            backend.db.session.add(new_resource)
            backend.db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            # tried to link to a non-existant parent
            return flask.Response('', 404)
        else:
            return self.as_dict(new_resource, parent_id, new_resource.id)

    def get(self, parent_id):
        """Return children linked to a given parent."""
        parent = self.parent_resource_type.query.filter_by(
                id=parent_id).options(
                        orm.joinedload(self.child_link_name)).first()
        if parent is None:
            return flask.Response('', 404)
        else:
            return {self.child_link_name: [
                self.as_dict(child, parent_id, child.id) for
                child in getattr(parent, self.child_link_name)]}


class ManyToManyLink(flask_restful.Resource):
    """Resource dealing with many-to-many links between collections."""

    left_id_name = None
    right_id_name = None
    join_table = None

    def put(self, left_id, right_id):
        """Create a link between the two given ids in the join table."""

        insert = self.join_table.insert().values({
            self.left_id_name: left_id,
            self.right_id_name: right_id})
        try:
            backend.db.session.execute(insert)
            backend.db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            # We hit a unique constraint for this combination
            # of ids, so we happily let the insert fail.
            pass

    def delete(self, left_id, right_id):
        """Delete a link between the two given ids in the join table."""
        delete = self.join_table.delete().where(sqlalchemy.and_(
            self.left_id_name == left_id, self.right_id_name == right_id))

        res = backend.db.session.execute(delete)
        backend.db.session.commit()

        if not res.rowcount:
            return flask.Response('', 404)
