"""Views for supporting quest resources."""


import flask.ext.restful as restful

import backend
import backend.quests.models as quest_models
import backend.common.resource as resource


class QuestBase(object):
    """Provide a common as_dict method."""

    view_fields = ['id', 'name', 'description', 'points', 'user_id']

    def as_dict(self, quest):
        """Return a serializable dictionary representing the given quest."""
        resp = {field: getattr(quest, field) for field in self.view_fields}
        resp['url'] = backend.api.url_for(
                Quest, user_id=quest.user_id, quest_id=quest.id)
        return resp


class Quest(QuestBase, resource.SimpleResource):
    """Resource for working with a single quest."""

    parser = resource.ProvidedParser()
    parser.add_argument('name', type=str)
    parser.add_argument('description', type=str)
    parser.add_argument('points', type=int)

    @staticmethod
    def query(user_id, quest_id):
        """Return the query to select the quest with the given ids."""
        return quest_models.Quest.query.filter_by(
                user_id=user_id, id=quest_id)


class QuestList(QuestBase, restful.Resource):
    """Resource for working with collections of quests."""

    parser = resource.ProvidedParser()
    parser.add_argument('name', type=str, required=True)
    parser.add_argument('description', type=str, required=True)
    parser.add_argument('points', type=int, required=True)

    def post(self, user_id):
        """Create a new quest and link it to its creator."""
        args = self.parser.parse_args()
        args['user_id'] = user_id
        quest = quest_models.Quest(**args)

        backend.db.session.add(quest)
        backend.db.session.commit()

        args['id'] = quest.id

        return args

    def get(self, user_id):
        """Return a list of quests linked to the given user_id."""
        quests = quest_models.Quest.query.filter_by(user_id=user_id).all()
        return {'quests': [self.as_dict(quest) for quest in quests]}
