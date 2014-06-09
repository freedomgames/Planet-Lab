"""Views for supporting quest resources."""


import flask
import flask.ext.restful as restful

import backend
import backend.missions.models as mission_models
import backend.quests.models as quest_models
import backend.users.models as user_models
import backend.common.resource as resource
import sqlalchemy


class QuestBase(object):
    """Provide a common as_dict method."""

    view_fields = (
            'id', 'name', 'description', 'icon_url', 'user_id', 'mission_id')

    def as_dict(self, quest, user_id, mission_id, quest_id):
        """Return a serializable dictionary representing the given quest."""
        resp = {field: getattr(quest, field) for field in self.view_fields}
        resp['url'] = backend.api.url_for(
                Quest, user_id=user_id, mission_id=mission_id, quest_id=quest_id)
        return resp


class Quest(QuestBase, resource.SimpleResource):
    """Resource for working with a single quest."""

    parser = resource.ProvidedParser()
    parser.add_argument('name', type=str)
    parser.add_argument('description', type=str)
    parser.add_argument('icon_url', type=str)

    @staticmethod
    def query(user_id, mission_id, quest_id):
        """Return the query to select the quest with the given ids."""
        subquery = backend.db.session.query(mission_models.Mission.id)
        subquery = subquery.filter_by(user_id=user_id, id=mission_id)
        subquery = subquery.subquery()

        query = quest_models.Quest.query
        query = query.filter_by(id=quest_id)
        query = query.filter(quest_models.Quest.mission_id.in_(subquery))

        return query


class QuestList(QuestBase, restful.Resource):
    """Resource for working with collections of quests."""

    parser = resource.ProvidedParser()
    parser.add_argument('name', type=str, required=True)
    parser.add_argument('description', type=str, required=True)
    parser.add_argument('icon_url', type=str)

    def post(self, user_id, mission_id):
        """Create a new quest and link it to its creator and mission."""
        # make sure the user_id and mission_id are actually linked
        query = mission_models.Mission.query.filter_by(
                user_id=user_id, id=mission_id)
        if not query.count():
            return flask.Response('', 404)
        else:
            args = self.parser.parse_args()
            args['user_id'] = user_id
            args['mission_id'] = mission_id
            quest = quest_models.Quest(**args)

            backend.db.session.add(quest)
            backend.db.session.commit()

            args['id'] = quest.id

            return args

    def get(self, user_id, mission_id):
        """Return a list of quests linked to the given user_id."""
        query = quest_models.Quest.query
        query = query.join(
                quest_models.Quest.mission, mission_models.Mission.user)
        query = query.filter(
                user_models.User.id == user_id,
                mission_models.Mission.id == mission_id)
        quests = query.all()

        return {'quests': [self.as_dict(quest, user_id, mission_id, quest.id) for
            quest in quests]}
