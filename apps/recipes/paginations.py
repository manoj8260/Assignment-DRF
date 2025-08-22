from rest_framework import pagination
from rest_framework.response import Response

class CusttomPagination(pagination.PageNumberPagination):
    page_size_query_param = 'page_size'
    page_query_param = 'page-num'
    max_page_size = 2
    page_size =2
    


    def get_paginated_response(self, data):
        return Response(
            {
                'previous' : self.get_previous_link(),
                'next' : self.get_next_link(),
                'page_size' : self.page_size ,
                'count' : self.page.paginator.count,
                'result' : data
                
            }
        )