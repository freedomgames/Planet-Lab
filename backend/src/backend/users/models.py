"""SQLAlchemy models for users"""


import backend

db = backend.db


class User(db.Model):
    """A user account for either a learner or a mentor."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    organization = db.Column(db.String, nullable=True)
    avatar_url = db.Column(db.String, nullable=True)

    missions = db.relationship("Mission", backref="user")
    quests = db.relationship("Quest", backref="user")
