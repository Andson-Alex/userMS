from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination


class MyPageNumberPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'size'
    max_page_size = 40
    page_query_param = 'page'


class MyLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 20
    limit_query_param = 'limit'
    offset_query_param = 'offset'
    max_limit = 50


class MyCursorPagination(CursorPagination):
    cursor_query_param = 'cursor'
    page_size = 20
    ordering = '-created'
    page_size_query_param = 'size'
    max_page_size = 50
