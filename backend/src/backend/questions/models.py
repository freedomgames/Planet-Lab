"""SQLAlchemy models for questions and quest completions."""

import backend
import backend.common.models as models

db = backend.db

QUESTION_TYPES = ('upload', 'text', 'multiple_choice')


class Answer(db.Model):
    """An answer to a question.  Answers are submitted by learners and
    evaluated by mentors.
    """
    __tablename__ = 'answers'

    id = db.Column(db.Integer, primary_key=True, nullable=False)

    question_type = db.Column(
            db.Enum(*QUESTION_TYPES, name='question_types'), nullable=False)
    answer_text = db.Column(db.String, nullable=True)
    answer_upload_url = db.Column(db.String, nullable=True)
    answer_multiple_choice = db.Column(
            db.Integer, db.ForeignKey(
                'multiple_choices.id', onupdate='CASCADE', ondelete='SET NULL'),
            index=True)

    creator_id = db.Column(
            db.Integer, db.ForeignKey('users.id', ondelete='cascade'),
            nullable=False, index=True)
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

    @property
    def creator_url(self):
        """Return the URL for this resource."""
        return backend.api.url_for(
                backend.user_views.User, user_id=self.creator_id)


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

    answers = db.relationship("Answer", backref="question")
    answered_by = db.relationship(
            "User", secondary=Answer.__table__)
    multiple_choices = db.relationship(
            "MultipleChoice", backref="question",
            order_by='MultipleChoice.order')

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


class MultipleChoice(db.Model, models.CreatedBy):
    """A multiple choice option linked to a question."""

    __tablename__ = 'multiple_choices'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    answer = db.Column(db.String, nullable=False)
    is_correct = db.Column(db.Boolean, default=False, nullable=False)
    order = db.Column(db.Integer, nullable=False, index=True)

    question_id = db.Column(
            db.Integer, db.ForeignKey(
                'questions.id', onupdate='CASCADE', ondelete='CASCADE'),
            nullable=False, index=True)
    answered_with = db.relationship(
            "Answer", backref="multiple_choice")

    @property
    def url(self):
        """Return the URL for this resource."""
        return backend.api.url_for(
                backend.question_views.MultipleChoice,
                question_id=self.question_id, multiple_choice_id=self.id)

    @property
    def question_url(self):
        """Return the URL for this resource."""
        return backend.api.url_for(
                backend.question_views.QuestionView,
                question_id=self.question_id)
