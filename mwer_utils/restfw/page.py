from rest_framework.pagination import PageNumberPagination


class PageNumberMonitorPagination(PageNumberPagination):
    max_page_size = 20
    page_size_query_param = "number"
    page_query_param = "page"


class PageNumberCountPagination(PageNumberPagination):
    max_page_size = 30
    page_size_query_param = "page_size"
    page_query_param = "page"
