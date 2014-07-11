"""Views for supporting quest resources."""


import flask_restful
import flask_restful.reqparse as reqparse
import werkzeug.exceptions

import backend
import backend.common.resource as resource
import backend.quests.models as quest_models
import backend.questions.models as question_models


def make_parser(with_question_type=False):
    """Return a parser for the Question resource.
    Allows question_type to be an argument depending on the
    value of with_question_type.
    """
    parser = reqparse.RequestParser()
    parser.add_argument('description', type=str, required=True)
    if with_question_type:
        parser.add_argument(
                'question_type', type=str, required=True,
                choices=question_models.QUESTION_TYPES)
    return parser


class QuestionBase(object):
    """Provide an as_dict method."""

    view_fields = (
            'id', 'url', 'description', 'question_type',
            'quest_id', 'quest_url', 'creator_id', 'creator_url')

    def as_dict(self, question):
        """Return a serializable dictionary representing the given quest."""
        return {field: getattr(question, field) for field in self.view_fields}


class Question(QuestionBase, resource.SimpleResource):
    """Manipulate questions linked to a quest."""

    parser = make_parser()

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

    @staticmethod
    def put(*args, **kwargs):
        """Can only GET here -- other verbs available at the above resource."""
        raise werkzeug.exceptions.MethodNotAllowed

    @staticmethod
    def delete(*args, **kwargs):
        """Can only GET here -- other verbs available at the above resource."""
        raise werkzeug.exceptions.MethodNotAllowed


class QuestionList(QuestionBase, resource.ManyToOneLink):
    """Resource for working with collections of questions."""

    parser = make_parser(with_question_type=True)

    parent_id_name = 'quest_id'
    child_link_name = 'questions'

    resource_type = question_models.Question
    parent_resource_type = quest_models.Quest


class AnswerBase(object):
    """Provide an as_dict method and a parser."""

    parser = reqparse.RequestParser()
    parser.add_argument('answer_text', type=str)
    parser.add_argument('answer_upload_url', type=str)

    view_fields = (
            'id', 'url', 'question_type', 'answer_text', 'answer_upload_url',
            'question_id', 'question_url', 'creator_id', 'creator_url')

    def as_dict(self, answer):
        """Return a serializable dictionary representing the given quest."""
        return {field: getattr(answer, field) for field in self.view_fields}


def get_question_type(question_id):
    """Retrieve the question type for the question with the given id.
    Return None if the question_id does not exist.
    """
    question_type_row = backend.db.session.query(
            question_models.Question.question_type).filter_by(
                    id=question_id).first()
    if question_type_row is None:
        return None
    else:
        return question_type_row[0]


def assert_answer_matches_question(question_type, answer):
    """We need to make sure the answer type matches the question
    type -- e.g. if the question type is a text response, make
    sure the answer is a text response rather than a file upload.
    Aborts with a 400 error if the types do not match.
    """
    if question_type is None:
        flask_restful.abort(404)
    else:
        has_text = answer['answer_text'] is not None
        has_url = answer['answer_upload_url'] is not None

        if question_type == 'upload' and (not has_url or has_text):
            flask_restful.abort(
                    400, message='If question_type is upload, the '
                    'answer_upload_url field must only be present.')
        elif question_type == 'text' and (not has_text or has_url):
            flask_restful.abort(
                    400, message='If question_type is text, the '
                    'answer_text field must only be present.')


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

    def put(self, question_id, answer_id):
        """Check that the answer type matches the question type
        before updating the answer.
        """
        question_type = get_question_type(question_id)
        assert_answer_matches_question(question_type, self.parser.parse_args())
        return super(Answer, self).put(
                question_id=question_id, answer_id=answer_id)


class AnswerList(AnswerBase, resource.ManyToOneLink):
    """Resource for working with collections of answers."""

    parent_id_name = 'question_id'
    child_link_name = 'answers'

    resource_type = question_models.Answer
    parent_resource_type = question_models.Question

    def build_args(self, parent_id):
        """Check that the answer type matches the question type
        before creating the answer.  Add the question type from the
        parent question into the answer's arguments.
        """
        args = super(AnswerList, self).build_args(parent_id)
        question_type = get_question_type(parent_id)
        assert_answer_matches_question(question_type, args)
        args['question_type'] = question_type
        return args
