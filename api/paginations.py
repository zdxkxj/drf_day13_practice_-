from rest_framework.pagination import PageNumberPagination
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.pagination import CursorPagination


class MyPageNumberPagination(PageNumberPagination):

    page_size = 3

    max_page_size = 5

    page_size_query_param = "page_size"

    page_query_param = "page"



class MyLimitPagination(LimitOffsetPagination):

    default_limit = 3

    limit_query_param = "limit"

    offset_query_param = "offset"

    max_limit = 5



class MyCoursePagination(CursorPagination):
    cursor_query_param = 'cursor'
    page_size = 3
    page_size_query_param = "page_size"
    max_page_size = 5
    ordering = "-price"
