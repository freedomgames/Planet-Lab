"""Custom SQLAlchemy types."""


import datetime
import pytz
import sqlalchemy.types as types


class UTCDateTime(types.TypeDecorator):
    """Ensures that times are stored in UTC.  Raises a ValueError
    if a naive datetime object is attempted to be persisted.
    """

    impl = types.DateTime
    python_type = datetime.datetime

    def process_bind_param(self, value, _):
        """Convert the time to UTC, raising an error on naive
        datetime objects.
        """
        if value is not None:
            return value.astimezone(pytz.utc)

    def process_result_value(self, value, _):
        """Return the value as a non-naive datetime in UTC."""
        if value is not None:
            return value.replace(tzinfo=pytz.utc)
