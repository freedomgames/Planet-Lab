"""SQLAlchemy models for questions and quest completions."""

import backend
import backend.common.models as models

db = backend.db

QUESTION_TYPES = ('upload', 'text')


class Answer(db.Model, models.CreatedBy):
    """An answer to a question.  Answers are submitted by learners and
    evaluated by mentors.
    """
    __tablename__ = 'answers'

    id = db.Column(db.Integer, primary_key=True, nullable=False)

    question_type = db.Column(
            db.Enum(*QUESTION_TYPES, name='question_types'), nullable=False)
    answer_text = db.Column(db.String, nullable=True)
    answer_upload_url = db.Column(db.String, nullable=True)

    question_id = db.Column(
            db.Integer, db.ForeignKey('questions.id', ondelete='cascade'),
            nullable=False, index=True)

    @property
    def url(self):
        """Return the URL for this resource."""
        return backend.api.url_for(
                backend.question_views.Answer,
                question_id=self.question_id, answer_id=self.id)

    @property
    def question_url(self):
        """Return the URL for this resource."""
        return backend.api.url_for(
                backend.question_views.QuestionView,
                question_id=self.question_id)


class Question(db.Model, models.CreatedBy):
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

    answers = db.relationship("Answer", backref="question")
    answered_by = db.relationship(
            "User", secondary=Answer.__table__)

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
