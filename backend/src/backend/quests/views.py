"""Views for supporting quest resources."""


import flask
import flask_restful
import flask_restful.reqparse as reqparse
import sqlalchemy.orm as orm

import backend
import backend.common.auth as auth
import backend.common.resource as resource
import backend.missions.models as mission_models
import backend.quests.models as quest_models


class QuestBase(object):
    """Provide a common as_dict method and a parser."""

    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True)
    parser.add_argument('description', type=str, required=True)
    parser.add_argument('icon_url', type=str)

    view_fields = (
            'id', 'url', 'name', 'description', 'icon_url',
            'creator_id', 'creator_url')

    def as_dict(self, quest):
        """Return a serializable dictionary representing the given quest."""
        resp = {field: getattr(quest, field) for field in self.view_fields}
        return resp


class Quest(QuestBase, resource.SimpleResource):
    """Resource for working with a single quest."""

    @staticmethod
    def query(quest_id):
        """Return the query to select the quest with the given ids."""
        return quest_models.Quest.query.filter_by(id=quest_id)


class QuestList(QuestBase, flask_restful.Resource):
    """Resource for working with collections of quests."""

    def post(self):
        """Create a new quest and link it to its creator and mission."""
        args = self.parser.parse_args()
        args['creator_id'] = auth.current_user_id()
        quest = quest_models.Quest(**args)

        backend.db.session.add(quest)
        backend.db.session.commit()

        args['id'] = quest.id

        return args


class QuestUserList(QuestBase, flask_restful.Resource):
    """Resource for working with collections of quests linked to users."""

    def get(self, user_id):
        """Return a list of quests linked to the given user_id."""
        query = quest_models.Quest.query.filter_by(creator_id=user_id)
        quests = query.all()

        return {'quests': [self.as_dict(quest) for quest in quests]}


class QuestMissionLink(resource.ManyToManyLink):
    """Many-to-many links between quests and missions."""

    left_id_name = quest_models.join_table.c.mission_id
    right_id_name = quest_models.join_table.c.quest_id
    join_table = quest_models.join_table


class QuestMissionLinkList(QuestBase, flask_restful.Resource):
    """List quests linked to a given mission."""

    def get(self, mission_id):
        """List quests linked to a given mission."""
        mission = mission_models.Mission.query.filter_by(
                id=mission_id).options(
                        orm.joinedload('quests')).first()
        if mission is None:
            return flask.Response('', 404)
        else:
            return {'quests': [self.as_dict(quest) for
                quest in mission.quests]}
