"""Views for supporting quest resources."""


import flask
import flask.ext.restful as restful

import backend
import backend.missions.models as mission_models
import backend.quests.models as quest_models
import backend.common.resource as resource
import sqlalchemy
import sqlalchemy.orm as orm


class QuestBase(object):
    """Provide a common as_dict method."""

    view_fields = (
            'id', 'name', 'description', 'icon_url', 'user_id')

    def as_dict(self, quest, user_id, quest_id):
        """Return a serializable dictionary representing the given quest."""
        resp = {field: getattr(quest, field) for field in self.view_fields}
        resp['url'] = backend.api.url_for(
                Quest, user_id=user_id, quest_id=quest_id)
        return resp


class Quest(QuestBase, resource.SimpleResource):
    """Resource for working with a single quest."""

    parser = resource.ProvidedParser()
    parser.add_argument('name', type=str)
    parser.add_argument('description', type=str)
    parser.add_argument('icon_url', type=str)

    @staticmethod
    def query(user_id, quest_id):
        """Return the query to select the quest with the given ids."""
        return quest_models.Quest.query.filter_by(user_id=user_id, id=quest_id)


class QuestList(QuestBase, restful.Resource):
    """Resource for working with collections of quests."""

    parser = resource.ProvidedParser()
    parser.add_argument('name', type=str, required=True)
    parser.add_argument('description', type=str, required=True)
    parser.add_argument('icon_url', type=str)

    def post(self, user_id):
        """Create a new quest and link it to its creator and mission."""
        args = self.parser.parse_args()
        args['user_id'] = user_id
        quest = quest_models.Quest(**args)

        backend.db.session.add(quest)
        backend.db.session.commit()

        args['id'] = quest.id

        return args

    def get(self, user_id):
        """Return a list of quests linked to the given user_id."""
        query = quest_models.Quest.query.filter_by(user_id=user_id)
        quests = query.all()

        return {'quests': [self.as_dict(quest, user_id, quest.id) for
            quest in quests]}


class QuestMissionLink(restful.Resource):
    """Many-to-many links between quests and missions."""

    def put(self, user_id, mission_id, quest_id):
        """Create a link between the mission and quest."""
        # Make sure the user_id and mission_id exist and are linked together
        query = backend.db.session.query(mission_models.Mission.id)
        query = query.filter_by(user_id=user_id, id=mission_id)

        if not query.count():
            return flask.Response('', 404)
        else:
            # We want to do an 'insert into ... where not exists' so we
            # can atomically do an insert-if-not-exists thing.
            select = sqlalchemy.select([
                sqlalchemy.literal(mission_id),
                sqlalchemy.literal(quest_id)]).where(~ sqlalchemy.exists(
                    [quest_models.join_table.c.mission_id]).where(
                        sqlalchemy.and_(
                            quest_models.join_table.c.mission_id == mission_id,
                            quest_models.join_table.c.quest_id == quest_id)))
            insert = quest_models.join_table.insert().from_select(
                    ["mission_id", "quest_id"], select)
            backend.db.session.execute(insert)
            backend.db.session.commit()


    def delete(self, user_id, mission_id, quest_id):
        """Delete the link between mission and quest."""
        # Make sure the user_id and mission_id exist and are linked together
        query = backend.db.session.query(mission_models.Mission.id)
        query = query.filter_by(user_id=user_id, id=mission_id)

        if not query.count():
            return flask.Response('', 404)
        else:
            delete = quest_models.join_table.delete().where(sqlalchemy.and_(
                quest_models.join_table.c.mission_id == mission_id,
                quest_models.join_table.c.quest_id == quest_id))
            backend.db.session.execute(delete)
            backend.db.session.commit()


class QuestMissionLinkList(QuestBase, restful.Resource):
    """List quests linked to a given mission."""

    def get(self, user_id, mission_id):
        """List quests linked to a given mission."""
        mission = mission_models.Mission.query.filter_by(
                user_id=user_id, id=mission_id).options(
                        orm.joinedload('quests')).first()
        if mission is None:
            return flask.Response('', 404)
        else:
            return {'quests': [self.as_dict(quest, user_id, quest.id) for
                quest in mission.quests]}
