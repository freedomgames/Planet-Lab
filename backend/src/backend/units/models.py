"""SQLAlchemy models for units.  Units are collections of quests."""


import flask

import backend
db = backend.db


class Unit(db.Model):
    """A units - a collections of quests."""

    __tablename__ = 'units'

    create_fields = ('name', 'description', 'image_name')
    editable_fields = ('name', 'description', 'image_name')
    viewable_fields = ('name', 'description', 'image_url', 'url')

    id_ = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=True)
    image_name = db.Column(db.String, nullable=True)

    quests = db.relationship("Quest")

    @property
    def image_url(self):
        """Return the URL for the unit's uploaded image.  Returns None
        if the unit has no uploaded image.
        """
        if self.image_name:
            # Eventually we would want to do something like
            # filename='%s/%s' % (self.id_, self.image_name)
            # but for now we will keep things simple.
            return flask.url_for('static', filename=self.image_name)
        else:
            return None

    @property
    def url(self):
        """Return the URL to view this unit."""
        return flask.url_for('units.get_unit', unit_id=self.id_)

    def as_dict(self, with_quests=False):
        """Return the unit as a dictionary."""
        result = {field: getattr(self, field) for
                field in self.viewable_fields}
        result['id'] = self.id_

        if with_quests:
            result['quests'] = [quest.as_dict() for quest in self.quests]
        return result
