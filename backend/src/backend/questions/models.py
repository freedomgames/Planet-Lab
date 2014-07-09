"""SQLAlchemy models for questions and quest completions."""

import sqlalchemy

import backend
import backend.common.models as models


db = backend.db

QUESTION_GROUPS = ('review_quiz', 'lab_report', 'closing_questions')
QUESTION_TYPES = ('upload', 'text', 'multiple_choice')


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
    answer_multiple_choice = db.Column(
            db.Integer, db.ForeignKey(
                'multiple_choices.id', onupdate='CASCADE', ondelete='SET NULL'),
            index=True)

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

# Make sure the answer to a multiple choice question is a valid choice
# for that question.
sqlalchemy.event.listen(Answer.__table__, 'after_create', sqlalchemy.DDL("""
CREATE OR REPLACE FUNCTION check_valid_mc_answer()
  RETURNS trigger
  LANGUAGE 'plpgsql'
  STABLE
AS '
BEGIN
  PERFORM NULL
  FROM multiple_choices
  WHERE id=NEW.answer_multiple_choice AND question_id=NEW.question_id;

  IF FOUND THEN
    RETURN NEW;
  ELSE
    RAISE EXCEPTION ''Invalid multiple choice id %% given for question %%'',
      NEW.answer_multiple_choice, NEW.question_id
      USING ERRCODE = ''23000'';
  END IF;
END';

CREATE TRIGGER multiple_choice_answer BEFORE INSERT OR UPDATE ON answers
FOR EACH ROW
WHEN (NEW.answer_multiple_choice IS NOT NULL)
EXECUTE PROCEDURE check_valid_mc_answer();"""))


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
    question_group = db.Column(
            db.Enum(*QUESTION_GROUPS, name='question_group'),
            nullable=False, index=True)

    quest_id = db.Column(
            db.Integer, db.ForeignKey('quests.id', ondelete='cascade'),
            nullable=False, index=True)

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
