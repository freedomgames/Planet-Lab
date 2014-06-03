"""Common tools for building restful resources."""


import flask.ext.restful.reqparse as reqparse


NOTHING = object()


class ProvidedParser(reqparse.RequestParser):
    """A subclass which allows us to discriminate between lack of
    values from a caller and default values for keys.

    That is, if a parser is created like so:

    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str)
    parser.add_argument('description', type=str)

    parser.parse_args() may return
    {"name": "sam", "description": None}

    whether the caller provided either
    {"name": "sam"} or {"name": "sam", "description": null}

    We remove this ambiguity by returning
    {"name": "sam"} in the first case and
    {"name": "sam", "description": None} in the second

    If a default value is given in and add_argument() call, that
    field will always be present whether it was supplied or not.
    """

    def add_argument(self, *args, **kwargs):
        """If not given by the caller, add a default value of 'nothing'
        to a field so we can tell if a user has provided a value for it.
        """
        if 'default' not in kwargs:
            kwargs['default'] = NOTHING
        super(ProvidedParser, self).add_argument(*args, **kwargs)

    def parse_args(self):
        """Return the dictionary from parse_args() without
        entries which were given no value by the caller.
        """
        args = super(ProvidedParser, self).parse_args()
        return {key: value for key, value in args.iteritems() if
                value is not NOTHING}
