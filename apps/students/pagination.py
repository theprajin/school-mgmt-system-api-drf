from rest_framework.pagination import PageNumberPagination


class DefaultStudentPagination(PageNumberPagination):
    page_size = 15
