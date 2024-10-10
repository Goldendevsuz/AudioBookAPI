# apps/user/urls.py

from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedSimpleRouter

from .views import CustomUserViewSet, UserCategoryViewSet, UserBookViewSet

# Root router - no need to register `users/` here, it's handled in the base urls
router = DefaultRouter()
router.register(r'', CustomUserViewSet, basename='users')  # This will handle /users/

# Nested router for UserCategories
categories_router = NestedSimpleRouter(router, r'', lookup='user')  # Nested under /users/
categories_router.register(r'categories', UserCategoryViewSet, basename='user-categories')

# Nested router for UserBooks
books_router = NestedSimpleRouter(router, r'', lookup='user')
books_router.register(r'books', UserBookViewSet, basename='user-books')

# Combine all routes
urlpatterns = router.urls + categories_router.urls + books_router.urls
