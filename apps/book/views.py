from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter
from .models import Book, BookReview, LatestSearch
from .pagination import BookReviewPagination
from .serializers import BookSerializer, BookReviewSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    search_fields = ['title', 'author__name', 'categories__name', 'summary']

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


def update_latest_search(user, search_results):
    latest_books = search_results[:20]

    # Store the books in LatestSearch model
    for book in latest_books:
        if not LatestSearch.objects.filter(user=user, book=book).exists():
            LatestSearch.objects.create(user=user, book=book)

    # Limit to 20 most recent entries
    latest_searches = LatestSearch.objects.filter(user=user).order_by('-created')[:20]
    return latest_searches


@extend_schema(
    parameters=[
        OpenApiParameter(name='q', description='Search term for books', required=False, type=str)
    ],
    responses={
        200: 'Search Results and Latest Search Response'  # You can refine this with a proper response schema
    }
)
@api_view(['GET'])
def search_books(request):
    search_term = request.query_params.get('q', '')

    # Initialize search results and latest searches
    search_results_data = []
    latest_searches_data = []

    if search_term:
        # Fetch dynamic search results (you can adjust the filter based on your needs)
        search_results = Book.objects.filter(title__icontains=search_term)

        # Format the search results to return in the response (limit to 5 results)
        search_results_data = [{
            'title': book.title,
            'author': book.author.name,
            'cover_url': book.cover_url
        } for book in search_results[:5]]  # Only return the top 5 search results

        # Update latest search based on the results if the user is authenticated
        if request.user.is_authenticated:
            latest_searches = update_latest_search(request.user, search_results)

            # Format the latest search results
            latest_searches_data = [{
                'title': search.book.title,
                'author': search.book.author.name,
                'cover_url': search.book.cover_url
            } for search in latest_searches]

    return Response({
        'search_results': search_results_data,
        'latest_searches': latest_searches_data
    })