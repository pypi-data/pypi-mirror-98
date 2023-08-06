from __future__ import unicode_literals

from datetime import date, datetime
from functools import wraps
from urllib.parse import quote_plus, urlencode

# parts of URL to be omitted
SKIP_IN_PATH = (None, "", b"", [], ())


def _escape(value):
    """
    Escape a single value of a URL string or a query parameter. If it is a list
    or tuple, turn it into a comma-separated string first.
    """

    # make sequences into comma-separated stings
    # if isinstance(value, (list, tuple)):
    #     value = ",".join(value)

    # dates and datetimes into isoformat
    if isinstance(value, (date, datetime)):
        value = value.isoformat()

    # make bools into true/false strings
    elif isinstance(value, bool):
        value = str(value).lower()

    # don't decode bytestrings
    elif isinstance(value, bytes):
        return value

    # encode strings to utf-8
    # if isinstance(value, string_types):
    #     return value.encode("utf-8")

    if isinstance(value, (list, tuple)):
        return value
    return str(value)


def _make_path(*parts):
    """
    Create a URL string from parts, omit all `None` values and empty strings.
    Convert lists and tuples to comma separated values.
    """
    return "/" + "/".join(
        # preserve ',' and '*' in url for nicer URLs in logs
        quote_plus(_escape(p), b",*")
        for p in parts
        if p not in SKIP_IN_PATH
    )


# parameters that apply to all methods
GLOBAL_PARAMS = ("pretty", "human", "error_trace", "format", "filter_path")


def query_params(*query_params):
    """
    Decorator that pops all accepted parameters from method's kwargs and puts
    them in the params argument.
    """

    def _wrapper(func):
        @wraps(func)
        def _wrapped(*args, **kwargs):
            params = {}
            if "params" in kwargs:
                params = kwargs.pop("params").copy()
            for p in query_params + GLOBAL_PARAMS:
                if p in kwargs:
                    v = kwargs.pop(p)
                    if v is not None:
                        params[p] = _escape(v)

            # don't treat ignore and request_timeout as other params to avoid escaping
            for p in ("ignore", "request_timeout"):
                if p in kwargs:
                    params[p] = kwargs.pop(p)
            return func(*args, params=params, **kwargs)

        return _wrapped

    return _wrapper


def dict_to_url_params(params):
    return "?%s" % urlencode(params)


class NamespacedClient(object):
    def __init__(self, client):
        self.client = client
        if self.client.token is not None:
            self.auth = {'Authorization': f'Bearer {self.client.token}'}
        else:
            self.auth = None