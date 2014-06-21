"""SQLAlchemy models for questions and quest completions."""

import datetime
import pytz

import backend
import backend.common.custom_types as custom_types

db = backend.db

QUESTION_TYPES = ('upload', 'text', 'multiple_choice')


class Question(db.Model):
    """Quests are linked to assessment questions, which learners
    answer to complete quests.
    """
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    description = db.Column(db.String, nullable=False)
    question_type = db.Column(
            db.Enum(*QUESTION_TYPES, name='question_types'),
            nullable=False)

    quest_id = db.Column(
            db.Integer, db.ForeignKey('quests.id', ondelete='cascade'),
            nullable=False, index=True)
    creator_id = db.Column(
            db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)

    @property
    def url(self):
        """Return the URL for this resource."""
        return backend.api.url_for(
                backend.question_views.Question,
                quest_id=self.quest_id, question_id=self.id)

    @property
    def quest_url(self):
        """Return the URL for this resource."""
        return backend.api.url_for(
                backend.quest_views.Quest, quest_id=self.quest_id)

    @property
    def creator_url(self):
        """Return the URL for this resource."""
        return backend.api.url_for(
                backend.user_views.User, user_id=self.creator_id)
