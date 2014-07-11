"""SQLAlchemy models for quests."""

import sqlalchemy.dialects.postgresql as postgresql

import backend
import backend.common.models as models

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


class Tag(db.Model, models.CreatedBy):
    """Tags are associated with quests to aid their searchability."""

    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String, nullable=False, unique=True)

    @property
    def url(self):
        """Return the URL for this resource."""
        return backend.api.url_for(backend.quest_views.Tag, tag_id=self.id)


class QuestTags(db.Model):
    """Join table linking quests to tags."""

    __tablename__ = 'quest_tags'

    tag_id = db.Column(
            db.Integer, db.ForeignKey(
                'tags.id', onupdate='CASCADE', ondelete='CASCADE'),
            nullable=False, index=True, primary_key=True)
    quest_id = db.Column(
            db.Integer, db.ForeignKey(
                'quests.id', onupdate='CASCADE', ondelete='CASCADE'),
            nullable=False, index=True, primary_key=True)


class Quest(db.Model, models.CreatedBy):
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

    questions = db.relationship("Question", backref="quest")

    missions = db.relationship(
            "Mission", secondary=join_table, backref="quests")
    tags = db.relationship(
            "Tag", secondary=QuestTags.__table__, backref="quests")

    @property
    def url(self):
        """Return the URL for this resource."""
        return backend.api.url_for(
                backend.quest_views.Quest, quest_id=self.id)
