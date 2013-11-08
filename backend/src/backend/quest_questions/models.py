"""SQLAlchemy models for quests questions.
Quests questsions are question and answer pairs linked to a quest.
"""


import backend
db = backend.db


class QuestQuestion(db.Model):
    """Quests questsions are question and answer pairs linked
    to a quest.
    """

    __tablename__ = 'quest_questions'

    create_fields = ('question', 'answer')
    viewable_fields = ('question', 'answer', 'quest_id')
    editable_fields = ('question', 'answer', 'quest_id')

    id_ = db.Column(db.Integer, primary_key=True, nullable=False)
    question = db.Column(db.String, nullable=False)
    answer = db.Column(db.String, nullable=False)

    quest_id = db.Column(db.Integer, db.ForeignKey('quests.id_'))

    def as_dict(self):
        """Return the question as a dictionary."""
        result = {field: getattr(self, field) for
                field in self.viewable_fields}
        result['id'] = self.id_
        return result
