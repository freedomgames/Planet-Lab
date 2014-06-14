"""SQLAlchemy models for missions."""


import flask

import backend
db = backend.db


class Quest(db.Model):
    """Quests are activities within a mission.  Mentors create quests
    and link them to missions.  Learners complete quests.
    """

    __tablename__ = 'quests'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    icon_url = db.Column(db.String, nullable=True)

    user_id = db.Column(
            db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    mission_id = db.Column(
            db.Integer, db.ForeignKey('missions.id'), nullable=False, index=True)
