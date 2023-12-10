from datetime import datetime
from json import loads
from urllib.parse import parse_qs


# class Filter(object):
#     def __init__(self, query: dict = None):
#         self.query = query if query else dict()
#
#     def filtering(self, searching: dict):
#         for key, value in searching.items():
#             self.query[f"{key}"] = value
#
#         return self.query
#
#     def filtering_with_params(self, params):
#         filling = dict()
#
#         if 'search' in params:
#             filling = self.filtering(searching=dict(params))
#
#         return filling


class Filter:
    def __init__(self, query: dict = None):
        self.query = query or {}

    def filtering(self, searching: dict):
        self.query.update(**searching)

    def filter_with_date(self, date_state):
        date_filter, now = dict(), datetime.now()

        if date_state == 'today':
            date_filter.update(
                created_at__gte=now.replace(hour=0, minute=0, second=0, microsecond=0),
                created_at__lt=now.replace(hour=23, minute=59, second=59, microsecond=0)
            )
        elif type(date_state) is dict:
            date_filter.update(created_at__gte=date_state['from'], created_at__lt=date_state['to'])

        self.query.update(date_filter)

    def filtering_with_params(self, params):
        params = dict(params)

        if 'search' in params:
            if params['search']:
                searching = loads(params['search'])
                self.filtering(searching=searching)

        if 'date_state' in params:
            self.filter_with_date(date_state=params['date_state'])

        return self.query
