"""SQLAlchemy models for users"""


import flask_user

import backend

db = backend.db


DEFAULT_AVATAR_URL = 'http://s3.amazonaws.com/%s/default-avatar.jpg' % (
        backend.app.config['S3_BUCKET'])


class User(db.Model, flask_user.UserMixin):
    """A user account for either a learner or a mentor."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=False, index=True)
    username = db.Column(db.String, nullable=False, unique=True, index=True)
    password = db.Column(db.String, nullable=False, default='', index=True)

    name = db.Column(db.String, nullable=True)
    email = db.Column(db.String, nullable=True)
    description = db.Column(db.String, nullable=True)
    avatar_url = db.Column(
            db.String, nullable=False, default=DEFAULT_AVATAR_URL)

    answers = db.relationship("Answer", backref="creator")
    questions = db.relationship("Question", backref="creator")
    missions = db.relationship("Mission", backref="user")
    quests = db.relationship("Quest", backref="user")
    organizations_created = db.relationship("Organization", backref="user")

    @property
    def url(self):
        """URL for the resource."""
        return backend.api.url_for(backend.user_views.User, user_id=self.id)
