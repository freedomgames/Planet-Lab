"""Common functionality for DB models."""


import sqlalchemy.ext.declarative as declarative

import backend

db = backend.db


class CreatedBy(object):
    """Mixin to provide a creator_id field and a creator_url propery."""

    @declarative.declared_attr
    def creator_id(_):
        """The creator_id column.  Columns from mixins need to be
        declared with the declared_attr decorator.
        """
        #pylint: disable=E0213,R0201
        return db.Column(
            db.Integer, db.ForeignKey(
                'users.id', onupdate='CASCADE', ondelete='SET NULL'),
            index=True)

    @property
    def creator_url(self):
        """Return the url for the resource's creator."""
        if self.creator_id is not None:
            return backend.api.url_for(
                    backend.user_views.User, user_id=self.creator_id)
