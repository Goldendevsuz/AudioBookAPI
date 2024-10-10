from rest_framework import viewsets, pagination
from rest_framework.response import Response
from .models import BookPage
from .serializers import BookPageSerializer

class BookPagePagination(pagination.PageNumberPagination):
    page_size = 1

class BookPageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BookPage.objects.all()
    serializer_class = BookPageSerializer
    pagination_class = BookPagePagination

    def get_queryset(self):
        book_id = self.kwargs.get('book_id')
        return self.queryset.filter(book_id=book_id)
