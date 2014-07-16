"""Views for supporting quest resources."""


import flask
import flask_restful
import sqlalchemy.exc
import sqlalchemy.orm as orm
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
    parser = resource.RequestParser()
    parser.add_argument('description', type=str, required=True)
    parser.add_argument(
            'question_group', type=str, required=True,
            choices=question_models.QUESTION_GROUPS)
    if with_question_type:
        parser.add_argument(
                'question_type', type=str, required=True,
                choices=question_models.QUESTION_TYPES)
    return parser


class QuestionBase(object):
    """Provide an as_dict method."""

    view_fields = (
            'id', 'url', 'description', 'question_type', 'question_group',
            'quest_id', 'quest_url', 'creator_id', 'creator_url')
    multiple_choice_fields = (
            'id', 'url', 'answer', 'is_correct', 'order',
            'question_id', 'question_url', 'creator_id', 'creator_url')

    def as_dict(self, question):
        """Return a serializable dictionary representing the given quest."""
        resp = {field: getattr(question, field) for field in self.view_fields}
        resp['multiple_choices'] = [{field: getattr(choice, field) for
            field in self.multiple_choice_fields} for
            choice in question.multiple_choices]
        return resp


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
        question_query = question_query.options(
                orm.joinedload('multiple_choices'))
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


def parse_question_groups(arg):
    """Parse the question_group query string into a list of
    question_groups and assert that each is a valid group.
    """
    question_groups = str(arg).split(',')
    assert all(question_group in question_models.QUESTION_GROUPS
                for question_group in question_groups), 'invalid question group'
    return question_groups


class QuestionList(QuestionBase, resource.ManyToOneLink):
    """Resource for working with collections of questions."""

    parser = make_parser(with_question_type=True)

    parent_id_name = 'quest_id'
    child_link_name = 'questions'

    resource_type = question_models.Question
    parent_resource_type = quest_models.Quest

    def get(self, parent_id):
        """Retrieve all questions linked to the given quest,
        optionally filtering them by question_group.
        """
        parser = resource.RequestParser()
        parser.add_argument('question_group', type=parse_question_groups)
        question_groups = parser.parse_args()['question_group']

        if question_groups is None:
            return super(QuestionList, self).get(parent_id)
        else:
            parent_count = self.parent_resource_type.query.filter_by(
                    id=parent_id).count()
            if not parent_count:
                return flask.Response('', 404)
            else:
                child_query = self.resource_type.query.filter_by(
                        quest_id=parent_id)
                if len(question_groups) == 1:
                    child_query = child_query.filter_by(
                            question_group=question_groups[0])
                else:
                    child_query = child_query.filter(
                            self.resource_type.question_group.in_(
                                question_groups))
                children = child_query.all()
                return {self.child_link_name: [
                    self.as_dict(child) for child in children]}


class AnswerBase(object):
    """Provide an as_dict method and a parser."""

    parser = resource.RequestParser()
    parser.add_argument('answer_text', type=str)
    parser.add_argument('answer_upload_url', type=str)
    parser.add_argument('answer_multiple_choice', type=int)

    view_fields = (
            'id', 'url', 'question_type', 'answer_text', 'answer_upload_url',
            'answer_multiple_choice', 'question_id',
            'question_url', 'creator_id', 'creator_url')

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
        has_mc = answer['answer_multiple_choice'] is not None

        if question_type == 'upload' and (not has_url or has_text or has_mc):
            flask_restful.abort(
                    400, message='If question_type is upload, the '
                    'answer_upload_url field must only be present.')
        elif question_type == 'text' and (not has_text or has_url or has_mc):
            flask_restful.abort(
                    400, message='If question_type is text, the '
                    'answer_text field must only be present.')
        elif question_type == 'multiple_choice' and (
                not has_mc or has_text or has_url):
            flask_restful.abort(
                    400, message='If question_type is multiple_choice, the '
                    'answer_multiple_choice field must only be present.')


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
        try:
            return super(Answer, self).put(
                    question_id=question_id, answer_id=answer_id)
        except sqlalchemy.exc.IntegrityError:
            # Tried to link a multiple choice answer to a bad choice
            return flask.Response('', 404)


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


class MultipleChoiceBase(object):
    """Provide an as_dict method and a parser."""

    parser = resource.RequestParser()
    parser.add_argument('answer', type=str, required=True)
    parser.add_argument('is_correct', type=bool, required=True)
    parser.add_argument('order', type=int, required=True)

    view_fields = (
            'id', 'url', 'answer', 'is_correct', 'order',
            'question_id', 'question_url', 'creator_id', 'creator_url')

    def as_dict(self, answer):
        """Return a serializable dictionary representing the given quest."""
        return {field: getattr(answer, field) for field in self.view_fields}


class MultipleChoice(MultipleChoiceBase, resource.SimpleResource):
    """Manipulate answers linked to a question."""

    @staticmethod
    def query(question_id, multiple_choice_id):
        """Return the question linked to the given quest."""
        question_query = backend.db.session.query(
                question_models.Question.id).filter_by(id=question_id)
        multiple_choice_query = question_models.MultipleChoice.query.filter_by(
                id=multiple_choice_id).filter(
                        question_models.MultipleChoice.question_id.in_(
                            question_query.subquery()))
        return multiple_choice_query


class MultipleChoiceList(MultipleChoiceBase, resource.ManyToOneLink):
    """Resource for working with collections of multiple choices."""

    parent_id_name = 'question_id'
    child_link_name = 'multiple_choices'

    resource_type = question_models.MultipleChoice
    parent_resource_type = question_models.Question

    def create_resource(self, args):
        """Make sure the parent question is the correct type to allow
        for multiple choice answers.
        """
        parent_id = args[self.parent_id_name]
        question_type_row = backend.db.session.query(
                question_models.Question.question_type).filter_by(
                        id=parent_id).first()
        if question_type_row is None:
            flask_restful.abort(404)
        else:
            question_type = question_type_row[0]
            if question_type != 'multiple_choice':
                flask_restful.abort(
                        400, message='Tried to link a multiple choice answer '
                        'to a non-multiple choice question')
            else:
                return super(MultipleChoiceList, self).create_resource(args)
