from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedSimpleRouter

from apps.book.views import BookViewSet, BookReviewViewSet, search_books, NewReleasesAPIView

# Root router for books
router = DefaultRouter()
router.register(r'', BookViewSet, basename='books')  # This handles /books/
# router.register(r'new-releases', NewReleasesAPIView.as_view(), basename='new-releases')

# Nested router for BookReviews related to a specific book
book_reviews_router = NestedSimpleRouter(router, r'', lookup='book')
book_reviews_router.register(r'reviews', BookReviewViewSet, basename='book-reviews')

urlpatterns = [
    path('search/', search_books, name='search_books'),
    path('new-releases/', NewReleasesAPIView.as_view(), name='new-releases'),
]
# Combine all routes
urlpatterns += router.urls + book_reviews_router.urls
