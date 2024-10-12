from django.db.models import Count, Avg
from django.utils import timezone
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Book, BookReview, LatestSearch
from .pagination import BookReviewPagination
from .serializers import BookSerializer, BookReviewSerializer
from ..author.models import Author


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    search_fields = ['title', 'author__name', 'categories__name', 'summary', 'tags__name']

    def create(self, request, *args, **kwargs):
        author_name = request.data.get('author_name')

        if not author_name:
            return Response({'error': 'Author name is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            author = Author.objects.get(name=author_name)
        except Author.DoesNotExist:
            return Response({'error': 'Author not found.'}, status=status.HTTP_404_NOT_FOUND)

        book_data = {
            'title': request.data.get('title'),
            'author': author,
            'rate': request.data.get('rate'),
            'pages_count': request.data.get('pages_count'),
            'release_date': request.data.get('release_date'),
            'poster_url': request.data.get('poster_url'),
            'cover_url': request.data.get('cover_url')
        }

        book = Book.objects.create(**book_data)

        tags = request.data.get('tags', [])
        book.tags.add(*tags)

        return Response(BookSerializer(book).data, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        author_name = request.data.get('author_name')

        if author_name:
            try:
                author = Author.objects.get(name=author_name)
                instance.author = author
            except Author.DoesNotExist:
                return Response({'error': 'Author not found.'}, status=status.HTTP_404_NOT_FOUND)

        book_data = {
            'title': request.data.get('title', instance.title),
            'rate': request.data.get('rate', instance.rate),
            'pages_count': request.data.get('pages_count', instance.pages_count),
            'release_date': request.data.get('release_date', instance.release_date),
            'poster_url': request.data.get('poster_url', instance.poster_url),
            'cover_url': request.data.get('cover_url', instance.cover_url)
        }

        for attr, value in book_data.items():
            setattr(instance, attr, value)

        instance.save()

        tags = request.data.get('tags', [])
        instance.tags.set(tags)

        return Response(BookSerializer(instance).data, status=status.HTTP_200_OK)


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


class NewReleasesAPIView(APIView):
    def get(self, request):
        # Fetch the latest released books by release_date
        latest_books = Book.objects.filter(release_date__lte=timezone.now()).order_by('-release_date')[:5]
        serializer = BookSerializer(latest_books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TrendingBooksAPIView(APIView):
    def get(self, request, *args, **kwargs):
        # Fetch books based on reviews
        trending_books = Book.objects.annotate(
            reviews_count=Count('reviews'),
            avg_rating=Avg('reviews__rating')
        ).filter(
            reviews_count__gte=1
        ).order_by('-reviews_count', '-avg_rating')[:5]

        # Collect book IDs that are already selected to prevent duplicates
        trending_book_ids = [book.id for book in trending_books]

        # If fewer than 5 books found, fetch more based on search history
        if len(trending_books) < 5:
            additional_books = Book.objects.annotate(
                search_count=Count('latestsearch')
            ).filter(
                search_count__gte=1
            ).exclude(id__in=trending_book_ids)  # Exclude books already in trending_books
            additional_books = additional_books.order_by('-search_count')[:5 - len(trending_books)]

            # Add these books to trending_books
            trending_books = list(trending_books) + list(additional_books)
            trending_book_ids += [book.id for book in additional_books]  # Update IDs

        # If still fewer than 5 books, fallback to recently added books (by release date)
        if len(trending_books) < 5:
            fallback_books = Book.objects.exclude(id__in=trending_book_ids).order_by('-release_date')[
                             :5 - len(trending_books)]
            trending_books = list(trending_books) + list(fallback_books)

        # Prepare the response data
        data = [{
            "title": book.title,
            "author": book.author.name,
            "cover": book.cover_url,
            "rating": getattr(book, 'avg_rating', None),
            "reviews_count": getattr(book, 'reviews_count', 0),
            "search_count": getattr(book, 'search_count', 0)
        } for book in trending_books]

        return Response(data)
