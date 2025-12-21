from django.conf import settings
from rest_framework.pagination import CursorPagination

class CustomCursorPagination(CursorPagination):
    ordering = "-id"
    page_size = settings.DEFAULT_PAGINATION_PAGE_SIZE