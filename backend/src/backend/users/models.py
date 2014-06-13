"""SQLAlchemy models for users"""


import backend

db = backend.db
GOOGLE_OAUTH_TYPE = "google"


class User(db.Model):
    """A user account for either a learner or a mentor."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=True)
    description = db.Column(db.String, nullable=True)
    avatar_url = db.Column(db.String, nullable=True)

    oauth_id = db.Column(db.String, nullable=True)
    oauth_type = db.Column(
            db.Enum(GOOGLE_OAUTH_TYPE, name='oauth_types'),
            nullable=True)
    oauth_token = db.Column(db.String, nullable=True)

    missions = db.relationship("Mission", backref="user")
    quests = db.relationship("Quest", backref="user")
    organizations_created = db.relationship("Organization", backref="user")

    @property
    def url(self):
        """URL for the resource."""
        return backend.api.url_for(backend.user_views.User, user_id=self.id)

db.Index('ix_user_oauth', User.oauth_id, User.oauth_type)
