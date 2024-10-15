# apps/user/urls.py
from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedSimpleRouter

from .views import CustomUserViewSet, UserCategoryViewSet, UserBookViewSet, CustomTokenCreateView

# Root router - no need to register `users/` here, it's handled in the base urls
router = DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='users')  # This will handle /users/

# Nested router for UserCategories
categories_router = NestedSimpleRouter(router, r'users', lookup='user')  # Nested under /users/
categories_router.register(r'categories', UserCategoryViewSet, basename='user-categories')

# Nested router for UserBooks
books_router = NestedSimpleRouter(router, r'users', lookup='user')
books_router.register(r'books', UserBookViewSet, basename='user-books')

urlpatterns = [
    path('jwt/create/', CustomTokenCreateView.as_view(), name='jwt-create'),
]
# Combine all routes
urlpatterns += router.urls + categories_router.urls + books_router.urls
