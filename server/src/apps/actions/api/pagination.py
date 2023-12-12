from rest_framework.pagination import PageNumberPagination


class PortfolioPagination(PageNumberPagination):
    page_size = 16


class ReviewPagination(PageNumberPagination):
    page_size = 16
