"""Views for supporting quest resources."""


import flask
import flask_restful
import flask_restful.reqparse as reqparse
import sqlalchemy.orm as orm
import sqlalchemy.exc

import backend
import backend.common.auth as auth
import backend.common.resource as resource
import backend.common.s3 as s3
import backend.missions.models as mission_models
import backend.quests.models as quest_models


DUPE_TAG_MSG = 'A tag with this name already exists.'

class QuestBase(object):
    """Provide a common as_dict method and a parser."""

    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True)
    parser.add_argument('summary', type=str, required=True)

    parser.add_argument(
            'inquiry_questions', type=lambda x: map(str, list(x)))
    parser.add_argument('pbl_description', type=str)
    parser.add_argument('mentor_guide', type=str)

    parser.add_argument('min_grade_level', type=int)
    parser.add_argument('max_grade_level', type=int)

    parser.add_argument('hours_required', type=int)
    parser.add_argument('minutes_required', type=int)

    parser.add_argument(
            'video_links', type=lambda x: map(str, list(x)))
    parser.add_argument('icon_url', type=str)

    view_fields = (
            'id', 'url', 'name', 'summary', 'icon_url', 'inquiry_questions',
            'pbl_description', 'mentor_guide', 'min_grade_level',
            'max_grade_level', 'hours_required', 'minutes_required',
            'video_links', 'creator_id', 'creator_url')
    tag_fields = ('id', 'url', 'name')

    def as_dict(self, quest):
        """Return a serializable dictionary representing the given quest."""
        resp = {field: getattr(quest, field) for field in self.view_fields}
        resp['tags'] = [{
            field: getattr(tag, field) for field in self.tag_fields} for
            tag in quest.tags]
        return resp


class Quest(QuestBase, resource.SimpleResource):
    """Resource for working with a single quest."""

    @staticmethod
    def query(quest_id):
        """Return the query to select the quest with the given ids."""
        return quest_models.Quest.query.filter_by(id=quest_id).options(
                orm.joinedload('tags'))


class QuestList(QuestBase, flask_restful.Resource):
    """Resource for working with collections of quests."""

    def post(self):
        """Create a new quest and link it to its creator and mission."""
        args = self.parser.parse_args()
        args['creator_id'] = auth.current_user_id()
        quest = quest_models.Quest(**args)

        backend.db.session.add(quest)
        backend.db.session.commit()

        return self.as_dict(quest)


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


class QuestStaticAsset(flask_restful.Resource):
    """Handle individual assets attached to a quest."""

    @staticmethod
    def get(quest_id, file_name):
        """Return a signed request to upload the given file name to
        the given quest and the URL for the resource upon its upload.
        """
        mime_type = flask.request.args['mime_type']
        upload_path = 'quests/%s/%s' % (quest_id, file_name)
        return s3.s3_upload_signature(upload_path, mime_type)

    @staticmethod
    def delete(quest_id, file_name):
        """Delete the given asset."""
        bucket = s3.get_bucket()
        key = 'quests/%s/%s' % (quest_id, file_name)
        bucket.delete_key(key)


class QuestStaticAssets(flask_restful.Resource):
    """List the assets uploaded to S3 for a given quest."""

    @staticmethod
    def get(quest_id):
        """List the assets uploaded to S3 for a given quest."""
        bucket = s3.get_bucket()
        prefix = 'quests/%s/' % quest_id
        prefix_len = len(prefix)
        # The prefix itself may appear as a key, so we filter
        # it out leaving only its children.
        keys = [key for key in bucket.list(prefix=prefix) if
                len(key.key) != prefix_len]
        return {'assets': [{
            'url': key.generate_url(0, query_auth=False),
            'file_name': key.key[prefix_len:]} for key in keys]}


class TagBase(object):
    """Provide a common as_dict method and a parser."""

    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True)

    view_fields = ('id', 'url', 'name', 'creator_id', 'creator_url')

    def as_dict(self, tag):
        """Return a serializable dictionary representing the given quest."""
        return {field: getattr(tag, field) for field in self.view_fields}


class Tag(TagBase, resource.SimpleResource):
    """Resource for working with a single tag."""

    @staticmethod
    def query(tag_id):
        """Return the query to select the quest with the given ids."""
        return quest_models.Tag.query.filter_by(id=tag_id)

    def put(self, *args, **kwargs):
        """Handle duplicate names elegantly."""
        try:
            return super(Tag, self).put(*args, **kwargs)
        except sqlalchemy.exc.IntegrityError:
            flask_restful.abort(400, message=DUPE_TAG_MSG)

class TagList(TagBase, resource.SimpleCreate):
    """Resource for working with collections of tags."""

    resource_type = quest_models.Tag

    def post(self, *args, **kwargs):
        """Handle duplicate names elegantly."""
        try:
            return super(TagList, self).post(*args, **kwargs)
        except sqlalchemy.exc.IntegrityError:
            flask_restful.abort(400, message=DUPE_TAG_MSG)

    def get(self):
        """Return all available tags."""
        tags = self.resource_type.query.all()
        return {'tags': [self.as_dict(tag) for tag in tags]}


class QuestTagLink(resource.ManyToManyLink):
    """Many-to-many links between quests and tags."""

    left_id_name = quest_models.QuestTags.__table__.c.quest_id
    right_id_name = quest_models.QuestTags.__table__.c.tag_id
    join_table = quest_models.QuestTags.__table__
