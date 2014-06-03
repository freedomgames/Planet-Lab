"""Views for supporting mission resources."""


import flask
import flask.ext.restful as restful

import backend
import backend.missions.models as mission_models
import backend.common.resource as resource


class MissionBase(restful.Resource):
    """Define a parser for other resources to use."""
    create_parser = resource.ProvidedParser()
    create_parser.add_argument('name', type=str, required=True)
    create_parser.add_argument('description', type=str, required=True)
    create_parser.add_argument('points', type=int, required=True)

    edit_parser = resource.ProvidedParser()
    edit_parser.add_argument('name', type=str)
    edit_parser.add_argument('description', type=str)
    edit_parser.add_argument('points', type=int)

    view_fields = ['id', 'name', 'description', 'points', 'user_id']

    def as_dict(self, mission):
        """Return a serializable dictionary representing the given mission."""
        resp = {field: getattr(mission, field) for field in self.view_fields}
        resp['url'] = backend.api.url_for(
                Mission, user_id=mission.user_id, mission_id=mission.id)
        return resp


class Mission(MissionBase):
    """Resource for working with a single mission."""

    @staticmethod
    def query(user_id, mission_id):
        """Return the query to select the mission with the given ids."""
        return mission_models.Mission.query.filter_by(
                user_id=user_id, id=mission_id)

    def get(self, user_id, mission_id):
        """Return the mission with matching user and mission ids."""
        mission = self.query(user_id, mission_id).first()
        if mission is None:
            return flask.Response('', 404)
        else:
            return self.as_dict(mission)

    def put(self, user_id, mission_id):
        """Update a mission."""
        args = self.edit_parser.parse_args()
        rows_updated = self.query(user_id, mission_id).update(args)
        backend.db.session.commit()

        if not rows_updated:
            return flask.Response('', 404)
        else:
            return args

    def delete(self, user_id, mission_id):
        """Delete a mission."""
        rows_deleted = self.query(user_id, mission_id).delete()
        backend.db.session.commit()

        if not rows_deleted:
            return flask.Response('', 404)


class MissionList(MissionBase):
    """Resource for working with collections of missions."""

    def post(self, user_id):
        """Create a new mission and link it to its creator."""
        args = self.create_parser.parse_args()
        args['user_id'] = user_id
        mission = mission_models.Mission(**args)

        backend.db.session.add(mission)
        backend.db.session.commit()

        args['id'] = mission.id

        return args

    def get(self, user_id):
        """Return a list of missions linked to the given user_id."""
        missions = mission_models.Mission.query.filter_by(user_id=user_id).all()
        return {'missions': [self.as_dict(mission) for mission in missions]}
