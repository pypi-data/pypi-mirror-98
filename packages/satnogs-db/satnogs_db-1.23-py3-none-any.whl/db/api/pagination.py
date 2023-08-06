"""
Custom pagination classes for REST framework
"""
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class LinkedHeaderPageNumberPagination(PageNumberPagination):
    """
    This overrides the default PageNumberPagination so that it only
    returns the results as an array, not the pagination controls
    (eg number of results, etc)
    """
    page_size = 25

    def get_paginated_response(self, data):
        next_url = self.get_next_link()
        previous_url = self.get_previous_link()

        if next_url is not None and previous_url is not None:
            link = '<{next_url}>; rel="next", <{previous_url}>; rel="prev"'
        elif next_url is not None:
            link = '<{next_url}>; rel="next"'
        elif previous_url is not None:
            link = '<{previous_url}>; rel="prev"'
        else:
            link = ''
        link = link.format(next_url=next_url, previous_url=previous_url)
        headers = {'Link': link} if link else {}
        return Response(data, headers=headers)
