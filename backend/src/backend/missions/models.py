"""SQLAlchemy models for missions."""


import backend
db = backend.db


class Mission(db.Model):
    """Missions are groups of quests.  Mentors chose how to group
    quests into missions and learners complete missions quest by quest.
    """

    __tablename__ = 'missions'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    points = db.Column(db.Integer, nullable=False)

    user_id = db.Column(
            db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)

    @property
    def url(self):
        """Return the url for the resource."""
        return backend.api.url_for(
                backend.mission_views.Mission, mission_id=self.id)
