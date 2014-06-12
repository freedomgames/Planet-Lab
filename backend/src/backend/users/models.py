"""SQLAlchemy models for users"""


import backend

db = backend.db


class User(db.Model):
    """A user account for either a learner or a mentor."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    avatar_url = db.Column(db.String, nullable=True)

    missions = db.relationship("Mission", backref="user")
    quests = db.relationship("Quest", backref="user")
    organizations_created = db.relationship("Organization", backref="user")

    @property
    def url(self):
        """URL for the resource."""
        return backend.api.url_for(backend.user_views.User, user_id=self.id)
