"""Views for supporting quest resources."""


import flask
import flask.ext.restful as restful

import backend
import backend.quests.models as quest_models
import backend.common.resource as resource


class QuestBase(restful.Resource):
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

    def as_dict(self, quest):
        """Return a serializable dictionary representing the given quest."""
        return {field: getattr(quest, field) for field in self.view_fields}


class Quest(QuestBase):
    """Resource for working with a single quest."""

    @staticmethod
    def query(user_id, quest_id):
        """Return the query to select the quest with the given ids."""
        return quest_models.Quest.query.filter_by(
                user_id=user_id, id=quest_id)

    def get(self, user_id, quest_id):
        """Return the quest with matching user and quest ids."""
        quest = self.query(user_id, quest_id).first()
        if quest is None:
            return flask.Response('', 404)
        else:
            return self.as_dict(quest)

    def put(self, user_id, quest_id):
        """Update a quest."""
        args = self.edit_parser.parse_args()
        rows_updated = self.query(user_id, quest_id).update(args)
        backend.db.session.commit()

        if not rows_updated:
            return flask.Response('', 404)
        else:
            return args

    def delete(self, user_id, quest_id):
        """Delete a quest."""
        rows_deleted = self.query(user_id, quest_id).delete()
        backend.db.session.commit()

        if not rows_deleted:
            return flask.Response('', 404)


class QuestList(QuestBase):
    """Resource for working with collections of quests."""

    def post(self, user_id):
        """Create a new quest and link it to its creator."""
        args = self.create_parser.parse_args()
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
