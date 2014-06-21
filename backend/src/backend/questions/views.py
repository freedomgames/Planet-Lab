"""Views for supporting quest resources."""


import flask_restful
import flask_restful.reqparse as reqparse
import werkzeug.exceptions

import backend
import backend.common.resource as resource
import backend.quests.models as quest_models
import backend.questions.models as question_models


class QuestionBase(object):
    """Provide an as_dict method and a parser."""

    parser = reqparse.RequestParser()
    parser.add_argument('description', type=str, required=True)
    parser.add_argument(
            'question_type', type=str, required=True,
            choices=question_models.QUESTION_TYPES)

    view_fields = (
            'id', 'url', 'description', 'question_type',
            'quest_id', 'quest_url', 'creator_id', 'creator_url')

    def as_dict(self, question):
        """Return a serializable dictionary representing the given quest."""
        return {field: getattr(question, field) for field in self.view_fields}


class Question(QuestionBase, resource.SimpleResource):
    """Manipulate questions linked to a quest."""

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


class QuestionView(QuestionBase, resource.SimpleResource):
    """View a single quest by id."""

    @staticmethod
    def query(question_id):
        """Return the given question."""
        return question_models.Question.query.filter_by(id=question_id)

    def put(self, question_id):
        """Can only GET here -- other verbs available at the above resource."""
        raise werkzeug.exceptions.MethodNotAllowed

    def delete(self, question_id):
        """Can only GET here -- other verbs available at the above resource."""
        raise werkzeug.exceptions.MethodNotAllowed


class QuestionList(QuestionBase, resource.ManyToOneLink):
    """Resource for working with collections of questions."""

    parent_id_name = 'quest_id'
    child_link_name = 'questions'

    resource_type = question_models.Question
    parent_resource_type = quest_models.Quest


class AnswerParser(reqparse.RequestParser):
    """Special parser for answers, which have switching logic
    based on the question type.
    """
    def parse_args(self, *args, **kwargs):
        """Call the parent parse_args and ensure that the
        fields provided match up with the question_type.
        """
        parsed_args = super(AnswerParser, self).parse_args(*args, **kwargs)

        question_type = parsed_args['question_type']
        has_text = parsed_args['answer_text'] is not None
        has_url = parsed_args['answer_upload_url'] is not None

        if question_type == 'upload' and (not has_url or has_text):
            flask_restful.abort(400, message='If question_type is upload, '
                    'the answer_upload_url field must only be present.')
        elif question_type == 'text' and (not has_text or has_url):
            flask_restful.abort(400, message='If question_type is text, '
                    'the answer_text field must only be present.')
        else:
            return parsed_args


class AnswerBase(object):
    """Provide an as_dict method and a parser."""

    parser = AnswerParser()
    parser.add_argument(
            'question_type', type=str, required=True,
            choices=question_models.QUESTION_TYPES)
    parser.add_argument('answer_text', type=str)
    parser.add_argument('answer_upload_url', type=str)

    view_fields = (
            'id', 'url', 'question_type', 'answer_text', 'answer_upload_url',
            'question_id', 'question_url', 'creator_id', 'creator_url')

    def as_dict(self, answer):
        """Return a serializable dictionary representing the given quest."""
        return {field: getattr(answer, field) for field in self.view_fields}


class Answer(AnswerBase, resource.SimpleResource):
    """Manipulate answers linked to a question."""

    @staticmethod
    def query(question_id, answer_id):
        """Return the question linked to the given quest."""
        question_query = backend.db.session.query(
                question_models.Question.id).filter_by(id=question_id)
        answer_query = question_models.Answer.query.filter_by(
                id=answer_id).filter(
                        question_models.Answer.question_id.in_(
                            question_query.subquery()))
        return answer_query


class AnswerList(AnswerBase, resource.ManyToOneLink):
    """Resource for working with collections of answers."""

    parent_id_name = 'question_id'
    child_link_name = 'answers'

    resource_type = question_models.Answer
    parent_resource_type = question_models.Answer
