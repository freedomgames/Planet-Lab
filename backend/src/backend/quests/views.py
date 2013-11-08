"""Views for supporting quest resources."""


import json
import flask
import sqlalchemy

import backend
import backend.common.accepts as accepts
import backend.quests.models as models

MESSAGE_FOR_400 = 'Invalid field given, must be one of %s'
MESSAGE_FOR_404 = 'No quest with unit id %s and quest id %s found.'

quests_bp = flask.Blueprint(
        'quests', __name__, url_prefix='/units/<int:unit_id>/quests')


@quests_bp.route('/', methods=('POST',))
def new_quest(unit_id):
    """Add a new quest to the given unit."""
    data = {field: flask.request.json.get(field) for
            field in models.Quest.create_fields}
    data['unit_id'] = unit_id

    quest = models.Quest(**data)
    backend.db.session.add(quest)
    backend.db.session.commit()

    response = flask.jsonify(quest.as_dict())
    response.status_code = 201
    response.headers['Location'] = quest.url
    return response


@quests_bp.route('/', methods=('GET',))
def get_quests(unit_id):
    """Get all of the quests attached to the given unit."""
    quests = models.Quest.query.filter_by(unit_id=unit_id).all()

    if accepts.wants_json():
        return flask.Response(
                json.dumps([quest.as_dict() for quest in quests]),
                mimetype='application/json')
    else:
        return flask.render_template('quest_list.html', quests=quests)


@quests_bp.route('/<int:quest_id>/', methods=('GET',))
def get_quest(unit_id, quest_id):
    """Get the quest with the given id."""
    quest = models.Quest.query.options(
            sqlalchemy.orm.joinedload('questions')).filter_by(
                unit_id=unit_id, id_=quest_id).first()
    if quest is None:
        return flask.make_response(MESSAGE_FOR_404 % (unit_id, quest_id), 404)
    elif accepts.wants_json():
        return flask.jsonify(quest.as_dict(with_questions=True))
    else:
        return flask.render_template('quest.html', quest=quest)


@quests_bp.route('/<int:quest_id>/', methods=('PUT',))
def update_quest(unit_id, quest_id):
    """Update the quest with the given id."""
    update = flask.request.json

    if any(field not in models.Quest.editable_fields for
            field in update.iterkeys()):
        msg = MESSAGE_FOR_400 % ', '.join(models.Quest.editable_fields)
        return flask.make_response(msg, 400)
    else:
        rows_updated = models.Quest.query.filter_by(
                unit_id=unit_id, id_=quest_id).update(update)
        backend.db.session.commit()
        if not rows_updated:
            return flask.make_response(
                    MESSAGE_FOR_404 % (unit_id, quest_id), 404)
        else:
            return flask.make_response('OK', 200)


@quests_bp.route('/<int:quest_id>/', methods=('DELETE',))
def delete_quest(unit_id, quest_id):
    """Delete the quest with the given id."""
    rows_deleted = models.Quest.query.filter_by(
            unit_id=unit_id, id_=quest_id).delete()
    backend.db.session.commit()
    if not rows_deleted:
        return flask.make_response(MESSAGE_FOR_404 % (unit_id, quest_id), 404)
    else:
        return flask.make_response('OK', 200)
