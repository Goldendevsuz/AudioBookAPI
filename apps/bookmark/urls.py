from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import EbookBookmarkViewSet, AudiobookBookmarkViewSet

router = DefaultRouter()
router.register(r'ebook-bookmarks', EbookBookmarkViewSet, basename='ebook-bookmark')
router.register(r'audiobook-bookmarks', AudiobookBookmarkViewSet, basename='audiobook-bookmark')

urlpatterns = [
    path('', include(router.urls)),
]
