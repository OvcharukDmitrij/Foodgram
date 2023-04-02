from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    """Кастомный пагинатор для изменения строкового значения
    параметра запроса."""

    page_size_query_param = 'limit'
