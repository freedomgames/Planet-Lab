"""SQLAlchemy models for missions."""


import backend
db = backend.db


join_table = db.Table('user_organizations', db.Model.metadata,
    db.Column(
        'organization_id', db.Integer,
        db.ForeignKey('organizations.id'), index=True),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), index=True),
    db.UniqueConstraint('organization_id', 'user_id')
)
db.Index(
        'ix_user_org_id_combo',
        join_table.c.organization_id,
        join_table.c.user_id)


class Organization(db.Model):
    """Organizations are groups of people.  Missions may also be linked
    to organizations.
    """
    __tablename__ = 'organizations'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    icon_url = db.Column(db.String, nullable=True)

    creator_id = db.Column(
            db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    members = db.relationship(
            "User", secondary=join_table, backref="organizations")

    @property
    def url(self):
        """URL for the resource."""
        return backend.api.url_for(
                backend.organization_views.Organization,
                organization_id=self.id)

    @property
    def creator_url(self):
        """Return the URL for this resource."""
        return backend.api.url_for(
                backend.user_views.User, user_id=self.creator_id)
