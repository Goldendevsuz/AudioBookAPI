from rest_framework.pagination import PageNumberPagination

class BookReviewPagination(PageNumberPagination):
    page_size = 3  # Limit to 3 items per page
