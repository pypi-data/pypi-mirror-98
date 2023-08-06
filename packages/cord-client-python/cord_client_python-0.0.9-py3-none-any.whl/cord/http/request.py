import json

from cord.http.query_methods import QueryMethods


class Request(object):
    """
    Request object. Takes query parameters and prepares them for execution.
    """
    def __init__(self,
                 query_method,
                 db_object_type,
                 uid,
                 headers,
                 timeout,
                 connect_timeout,
                 payload,
                 ):
        self.http_method = QueryMethods.POST
        self.data = json.dumps({'query_type': db_object_type.__name__.lower(),
                                'query_method': query_method,
                                'values': {
                                    'uid': uid,
                                    'payload': payload,
                                }})
        self.headers = headers
        self.timeout = timeout
        self.connect_timeout = connect_timeout

    def __str__(self):
        return "Request({}, {}, {}, {})".format(
            self.http_method,
            self.data,
            self.headers,
            self.timeout,
            self.connect_timeout,
        )

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.__dict__ == other.__dict__