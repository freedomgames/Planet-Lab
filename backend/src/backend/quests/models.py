"""SQLAlchemy models for quests."""


import flask

import backend
db = backend.db


class Quest(db.Model):
    """Quests are groups of missions.  Mentors chose how to group
    quests into missions and learners complete quests mission by
    mission.
    """

    __tablename__ = 'quests'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    points = db.Column(db.Integer, nullable=False)

    user_id = db.Column(
            db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
