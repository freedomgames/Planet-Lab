"""Views for supporting organization resources."""


import sqlalchemy.orm as orm

import backend.common.resource as resource
import backend.organizations.models as organization_models


class OrganizationBase(object):
    """Provide a common as_dict method and a parser."""

    parser = resource.RequestParser()
    parser.add_argument('name', type=str, required=True)
    parser.add_argument('description', type=str, required=True)
    parser.add_argument('icon_url', type=str)

    view_fields = ('id', 'url', 'name', 'description', 'icon_url',
            'creator_id', 'creator_url')
    user_fields = ('id', 'url', 'name', 'avatar_url')

    def as_dict(self, organization):
        """Return a serializable dictionary representing the given org."""
        resp = {field: getattr(organization, field) for
                field in self.view_fields}
        resp['members'] = [{field: getattr(user, field) for
            field in self.user_fields} for
            user in organization.members]
        return resp


class Organization(OrganizationBase, resource.SimpleResource):
    """Resource for working with a single organization."""

    @staticmethod
    def query(organization_id):
        """Return the query to select the organization with the given id."""
        return organization_models.Organization.query.filter_by(
                id=organization_id).options(orm.joinedload('members'))


class OrganizationList(OrganizationBase, resource.SimpleCreate):
    """Resource for working with collections of organizations."""

    resource_type = organization_models.Organization


class OrganizationUserLink(resource.ManyToManyLink):
    """Many-to-many links between users and organizations."""

    left_id_name = organization_models.join_table.c.organization_id
    right_id_name = organization_models.join_table.c.user_id
    join_table = organization_models.join_table
