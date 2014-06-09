"""Views for supporting mission resources."""


import flask.ext.restful as restful

import backend
import backend.missions.models as mission_models
import backend.common.resource as resource


class MissionBase(object):
    """Provide a common as_dict method."""

    view_fields = ['id', 'name', 'description', 'points', 'user_id']

    def as_dict(self, mission, user_id, mission_id):
        """Return a serializable dictionary representing the given mission."""
        resp = {field: getattr(mission, field) for field in self.view_fields}
        resp['url'] = backend.api.url_for(
                Mission, user_id=user_id, mission_id=mission_id)
        return resp


class Mission(MissionBase, resource.SimpleResource):
    """Resource for working with a single mission."""

    parser = resource.ProvidedParser()
    parser.add_argument('name', type=str)
    parser.add_argument('description', type=str)
    parser.add_argument('points', type=int)

    @staticmethod
    def query(user_id, mission_id):
        """Return the query to select the mission with the given ids."""
        return mission_models.Mission.query.filter_by(
                user_id=user_id, id=mission_id)


class MissionList(MissionBase, restful.Resource):
    """Resource for working with collections of missions."""

    parser = resource.ProvidedParser()
    parser.add_argument('name', type=str, required=True)
    parser.add_argument('description', type=str, required=True)
    parser.add_argument('points', type=int, required=True)

    def post(self, user_id):
        """Create a new mission and link it to its creator."""
        args = self.parser.parse_args()
        args['user_id'] = user_id
        mission = mission_models.Mission(**args)

        backend.db.session.add(mission)
        backend.db.session.commit()

        args['id'] = mission.id

        return args

    def get(self, user_id):
        """Return a list of missions linked to the given user_id."""
        missions = mission_models.Mission.query.filter_by(user_id=user_id).all()
        return {'missions': [self.as_dict(mission, user_id, mission.id) for
            mission in missions]}
