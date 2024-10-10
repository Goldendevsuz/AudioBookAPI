from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookPageViewSet

router = DefaultRouter()
router.register(r'books/(?P<book_id>[^/.]+)/pages', BookPageViewSet, basename='book-pages')

urlpatterns = [
    path('', include(router.urls)),
]
