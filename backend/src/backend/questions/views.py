"""Views for supporting quest resources."""


import backend
import backend.common.resource as resource
import backend.quests.models as quest_models
import backend.questions.models as question_models


class QuestionBase(object):
    """Provide an as_dict method."""

    view_fields = (
            'id', 'url', 'description', 'question_type',
            'quest_id', 'quest_url', 'creator_id', 'creator_url')

    def as_dict(self, question, quest_id, question_id):
        """Return a serializable dictionary representing the given quest."""
        return {field: getattr(question, field) for field in self.view_fields}


class Question(QuestionBase, resource.SimpleResource):
    """Manipulate questions linked to a quest."""

    parser = resource.ProvidedParser()
    parser.add_argument('description', type=str)
    parser.add_argument(
            'question_type', type=str, choices=question_models.QUESTION_TYPES)

    @staticmethod
    def query(quest_id, question_id):
        """Return the question linked to the given quest."""
        quest_query = backend.db.session.query(
                quest_models.Quest.id).filter_by(id=quest_id)
        question_query = question_models.Question.query.filter_by(
                id=question_id).filter(
                        question_models.Question.quest_id.in_(
                            quest_query.subquery()))
        return question_query


class QuestionList(QuestionBase, resource.ManyToOneLink):
    """Resource for working with collections of questions."""

    parent_id_name = 'quest_id'
    child_link_name = 'questions'

    resource_type = question_models.Question
    parent_resource_type = quest_models.Quest

    parser = resource.ProvidedParser()
    parser.add_argument('description', type=str, required=True)
    parser.add_argument(
            'question_type', type=str, required=True,
            choices=question_models.QUESTION_TYPES)
