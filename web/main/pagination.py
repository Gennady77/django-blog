from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination


class BasePageNumberPagination(PageNumberPagination):
    page_size: int = 5
    page_query_param: str = 'page'
    max_page_size: int = 100
    page_size_query_param: str = 'page_size'

class BaseLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 5
    max_limit = 100

class BaseCursorPagination(CursorPagination):
    page_size = 5
