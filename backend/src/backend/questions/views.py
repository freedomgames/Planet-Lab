"""Views for supporting quest resources."""


import flask
import flask_restful
import sqlalchemy.exc
import sqlalchemy.orm as orm

import backend
import backend.common.auth as auth
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


class QuestionList(QuestionBase, flask_restful.Resource):
    """Resource for working with collections of questions."""

    parser = resource.ProvidedParser()
    parser.add_argument('description', type=str, required=True)
    parser.add_argument(
            'question_type', type=str, required=True,
            choices=question_models.QUESTION_TYPES)

    def post(self, quest_id):
        """Create a new question and link it to its creator and quest."""
        args = self.parser.parse_args()
        args['creator_id'] = auth.current_user_id()
        args['quest_id'] = quest_id
        question = question_models.Question(**args)

        try:
            backend.db.session.add(question)
            backend.db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            # tried to link to a non-existant quest
            return flask.Response('', 404)
        else:
            return self.as_dict(question, quest_id, question.id)

    def get(self, quest_id):
        """Return questions linked to a given quest."""
        quest = quest_models.Quest.query.filter_by(
                id=quest_id).options(
                        orm.joinedload('questions')).first()
        if quest is None:
            return flask.Response('', 404)
        else:
            return {'questions': [
                self.as_dict(question, quest_id, question.id) for
                question in quest.questions]}
