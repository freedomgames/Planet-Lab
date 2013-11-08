"""SQLAlchemy models for quests.  Quests are curricula linked to units."""


import flask

import backend
db = backend.db


class Quest(db.Model):
    """Quests are curricula organized in units with
    linked refresher questions.
    """

    __tablename__ = 'quests'

    create_fields = (
            'name', 'partner_name',
            'scientist_prep', 'activity_steps', 'field_notes',
            'image_name', 'video_url')
    viewable_fields = (
            'name', 'partner_name',
            'scientist_prep', 'activity_steps', 'field_notes',
            'image_name', 'video_url',
            'image_url', 'url')
    editable_fields = (
            'name', 'partner_name',
            'scientist_prep', 'activity_steps', 'field_notes',
            'image_name', 'video_url',
            'unit_id')

    id_ = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    partner_name = db.Column(db.String, nullable=False)

    scientist_prep = db.Column(db.Text, nullable=True)
    activity_steps = db.Column(db.Text, nullable=True)
    field_notes = db.Column(db.Text, nullable=True)

    image_name = db.Column(db.String, nullable=True)
    video_url = db.Column(db.String, nullable=True)

    unit_id = db.Column(db.Integer, db.ForeignKey('units.id_'))
    questions = db.relationship("QuestQuestion")

    @property
    def image_url(self):
        """Return the URL for the unit's uploaded image.  Returns None
        if the unit has no uploaded image.
        """
        if self.image_name:
            # Eventually we would want to do something like
            # filename=quests/'%s/%s' % (self.id_, self.image_name)
            # but for now we will keep things simple.
            return flask.url_for('static', filename=self.image_name)
        else:
            return None

    @property
    def url(self):
        """Return the URL to view this unit."""
        return flask.url_for(
                'quests.get_quest', unit_id=self.unit_id, quest_id=self.id_)

    def as_dict(self, with_questions=False):
        """Return the unit as a dictionary."""
        result = {field: getattr(self, field) for
                field in self.viewable_fields}
        result['id'] = self.id_

        if with_questions:
            result['questions'] = [question.as_dict() for
                    question in self.questions]
        return result
