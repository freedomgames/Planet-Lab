"""Views for supporting mission resources."""


import flask_restful
import sqlalchemy.orm as orm

import backend.common.resource as resource
import backend.missions.models as mission_models


class MissionBase(object):
    """Provide a common as_dict method and a parser."""

    parser = resource.RequestParser()
    parser.add_argument('name', type=str, required=True)
    parser.add_argument('description', type=str, required=True)
    parser.add_argument('points', type=int, required=True)

    view_fields = (
            'id', 'url', 'name', 'description', 'points',
            'creator_id', 'creator_url')
    quest_fields = (
            'id', 'url', 'name', 'summary', 'icon_url',
            'creator_id', 'creator_url')

    def as_dict(self, mission):
        """Return a serializable dictionary representing the given mission."""
        resp = {field: getattr(mission, field) for field in self.view_fields}
        resp['quests'] = [{field: getattr(quest, field) for
            field in self.quest_fields} for quest in mission.quests]
        return resp


class Mission(MissionBase, resource.SimpleResource):
    """Resource for working with a single mission."""

    @staticmethod
    def query(mission_id):
        """Return the query to select the mission with the given ids."""
        return mission_models.Mission.query.filter_by(
                id=mission_id).options(
                        orm.joinedload('quests'))


class MissionList(MissionBase, resource.SimpleCreate):
    """Resource for working with collections of missions."""

    resource_type = mission_models.Mission


class MissionUserList(MissionBase, flask_restful.Resource):
    """List missions linked to a user."""
    def get(self, user_id):
        """Return a list of missions linked to the given user_id."""
        missions = mission_models.Mission.query.filter_by(
                creator_id=user_id).all()
        return {'missions': [self.as_dict(mission) for
            mission in missions]}
