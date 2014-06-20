"""Views for supporting mission resources."""


import flask_restful
import flask_restful.reqparse as reqparse
import sqlalchemy.orm as orm

import backend
import backend.common.auth as auth
import backend.common.resource as resource
import backend.missions.models as mission_models


class MissionBase(object):
    """Provide a common as_dict method."""

    view_fields = ('id', 'name', 'description', 'points', 'user_id')
    quest_fields = (
            'id', 'name', 'description', 'icon_url', 'user_id')

    def as_dict(self, mission, mission_id):
        """Return a serializable dictionary representing the given mission."""
        resp = {field: getattr(mission, field) for field in self.view_fields}
        resp['url'] = backend.api.url_for(
                Mission, mission_id=mission_id)
        resp['quests'] = [{field: getattr(quest, field) for
            field in self.quest_fields} for quest in mission.quests]
        return resp


class Mission(MissionBase, resource.SimpleResource):
    """Resource for working with a single mission."""

    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str)
    parser.add_argument('description', type=str)
    parser.add_argument('points', type=int)

    @staticmethod
    def query(mission_id):
        """Return the query to select the mission with the given ids."""
        return mission_models.Mission.query.filter_by(
                id=mission_id).options(
                        orm.joinedload('quests'))


class MissionList(MissionBase, flask_restful.Resource):
    """Resource for working with collections of missions."""

    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True)
    parser.add_argument('description', type=str, required=True)
    parser.add_argument('points', type=int, required=True)

    def post(self):
        """Create a new mission and link it to its creator."""
        args = self.parser.parse_args()
        args['user_id'] = auth.current_user_id()
        mission = mission_models.Mission(**args)

        backend.db.session.add(mission)
        backend.db.session.commit()

        return self.as_dict(mission, mission.id)


class MissionUserList(MissionBase, flask_restful.Resource):
    """List missions linked to a user."""
    def get(self, user_id):
        """Return a list of missions linked to the given user_id."""
        missions = mission_models.Mission.query.filter_by(user_id=user_id).all()
        return {'missions': [self.as_dict(mission, mission.id) for
            mission in missions]}
