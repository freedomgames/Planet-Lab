"""Views for units resources."""


import json
import flask
import sqlalchemy

import backend
import backend.common.accepts as accepts
import backend.units.models as models


MESSAGE_FOR_400 = 'Invalid field given, must be one of %s.'
MESSAGE_FOR_404 = 'No unit with id %s found.'


units_bp = flask.Blueprint('units', __name__, url_prefix='/units')


@units_bp.route('/', methods=('POST',))
def new_unit():
    """Add a new unit to the database."""
    data = {field: flask.request.json.get(field) for
            field in models.Unit.create_fields}
    unit = models.Unit(**data)

    backend.db.session.add(unit)
    backend.db.session.commit()

    response = flask.jsonify(unit.as_dict())
    response.status_code = 201
    response.headers['Location'] = unit.url
    return response


@units_bp.route('/', methods=('GET',))
def list_units():
    """List all the units in the database."""
    units = models.Unit.query.all()
    if accepts.wants_json():
        return flask.Response(
                json.dumps([unit.as_dict() for unit in units]),
                mimetype='application/json')
    else:
        return flask.render_template('units_list.html', units=units)


@units_bp.route('/<int:unit_id>/', methods=('GET',))
def get_unit(unit_id):
    """Get the unit for the given id."""
    unit = models.Unit.query.options(
            sqlalchemy.orm.joinedload('quests')).get(unit_id)
    if unit is None:
        return flask.make_response(MESSAGE_FOR_404 % unit_id, 404)
    elif accepts.wants_json():
        return flask.jsonify(unit.as_dict(with_quests=True))
    else:
        return flask.render_template('unit.html', unit=unit)


@units_bp.route('/<int:unit_id>/', methods=('PUT',))
def update_unit(unit_id):
    """Update the unit for the given id."""
    update = flask.request.json

    if any(field not in models.Unit.editable_fields for
            field in update.iterkeys()):
        return flask.make_response(
                MESSAGE_FOR_400 % ', '.join(models.Unit.editable_fields),
                400)
    else:
        rows_updated = models.Unit.query.filter_by(id_=unit_id).update(update)
        backend.db.session.commit()
        if not rows_updated:
            return flask.make_response(MESSAGE_FOR_404 % unit_id, 404)
        else:
            return flask.make_response('OK', 200)


@units_bp.route('/<int:unit_id>/', methods=('DELETE',))
def delete_unit(unit_id):
    """Deletep the unit with the given id."""
    rows_deleted = models.Unit.query.filter_by(id_=unit_id).delete()
    backend.db.session.commit()
    if not rows_deleted:
        return flask.make_response(MESSAGE_FOR_404 % unit_id, 404)
    else:
        return flask.make_response('OK', 200)
