"""SQLAlchemy models for quests."""

import sqlalchemy.dialects.postgresql as postgresql

import backend

db = backend.db


join_table = db.Table('mission_quests', db.Model.metadata,
    db.Column(
        'mission_id', db.Integer, db.ForeignKey('missions.id'), index=True),
    db.Column('quest_id', db.Integer, db.ForeignKey('quests.id'), index=True),
    db.UniqueConstraint('mission_id', 'quest_id')
)
db.Index(
        'ix_mission_quests_id_combo',
        join_table.c.mission_id, join_table.c.quest_id)


class Quest(db.Model):
    """Quests are activities within a mission.  Mentors create quests
    and link them to missions.  Learners complete quests.
    """
    __tablename__ = 'quests'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    summary = db.Column(db.String, nullable=False)

    inquiry_questions = db.Column(
            postgresql.ARRAY(db.String), nullable=False, default=[])
    pbl_description = db.Column(db.String, nullable=True)
    mentor_guide = db.Column(db.String, nullable=True)

    min_grade_level = db.Column(db.Integer, nullable=True)
    max_grade_level = db.Column(db.Integer, nullable=True)

    hours_required = db.Column(db.Integer, nullable=True)
    minutes_required = db.Column(db.Integer, nullable=True)

    video_links = db.Column(
            postgresql.ARRAY(db.String), nullable=False, default=[])
    icon_url = db.Column(db.String, nullable=True)

    creator_id = db.Column(
            db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)

    questions = db.relationship("Question", backref="quest")

    missions = db.relationship(
            "Mission", secondary=join_table, backref="quests")

    @property
    def url(self):
        """Return the URL for this resource."""
        return backend.api.url_for(
                backend.quest_views.Quest, quest_id=self.id)

    @property
    def creator_url(self):
        """Return the URL for this resource."""
        return backend.api.url_for(
                backend.user_views.User, user_id=self.creator_id)
