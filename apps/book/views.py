from rest_framework import viewsets, permissions
from drf_spectacular.utils import extend_schema, OpenApiParameter

from .models import Book, BookReview
from .pagination import BookReviewPagination
from .serializers import BookSerializer, BookReviewSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

# @extend_schema(
#     parameters=[
#         OpenApiParameter(name='book_pk', location=OpenApiParameter.PATH, required=True, type=int),
#     ]
# )
class BookReviewViewSet(viewsets.ModelViewSet):
    queryset = BookReview.objects.all()
    serializer_class = BookReviewSerializer
    pagination_class = BookReviewPagination  # Use the local pagination class

    def get_queryset(self):
        book_id = self.kwargs.get('book_pk')
        queryset = BookReview.objects.filter(book_id=book_id)

        # You can further customize the queryset here
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # Automatically assign the logged-in user
