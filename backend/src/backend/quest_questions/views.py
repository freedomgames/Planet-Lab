"""Views for supporting quest question resources."""


import flask

import backend
import backend.quest_questions.models as models


MESSAGE_FOR_400 = 'Invalid field given, must be one of %s.'
MESSAGE_FOR_404 = 'No question with quest id %s and question id %s found.'


quest_questions_bp = flask.Blueprint(
        'quest_questions', __name__,
        url_prefix='/units/<int:unit_id>/quests/<int:quest_id>/questions')


@quest_questions_bp.route('/', methods=('POST',))
def new_question(unit_id, quest_id):
    """Add a new question to the given quest."""
    data = {field: flask.request.json.get(field) for
            field in models.QuestQuestion.create_fields}
    data['quest_id'] = quest_id
    question = models.QuestQuestion(**data)

    backend.db.session.add(question)
    backend.db.session.commit()

    response = flask.jsonify(question.as_dict())
    response.status_code = 201
    return response


@quest_questions_bp.route('/<int:question_id>/', methods=('PUT',))
def update_quest(unit_id, quest_id, question_id):
    """Update the question with the given id."""
    update = flask.request.json

    if any(field not in models.QuestQuestion.editable_fields for
            field in update.iterkeys()):
        return flask.make_response(
                MESSAGE_FOR_400 % ', '.join(models.Quest.editable_fields),
                400)
    else:
        rows_updated = models.QuestQuestion.query.filter_by(
                quest_id=quest_id, id_=question_id).update(update)
        backend.db.session.commit()
        if not rows_updated:
            return flask.make_response(
                    MESSAGE_FOR_404 % (quest_id, question_id), 404)
        else:
            return flask.make_response('OK', 200)


@quest_questions_bp.route('/<int:question_id>/', methods=('DELETE',))
def delete_quest(unit_id, quest_id, question_id):
    """Delete the question with the given id."""
    rows_deleted = models.QuestQuestion.query.filter_by(
            quest_id=quest_id, id_=question_id).delete()
    backend.db.session.commit()
    if not rows_deleted:
        return flask.make_response(
                MESSAGE_FOR_404 % (quest_id, question_id), 404)
    else:
        return flask.make_response('OK', 200)
