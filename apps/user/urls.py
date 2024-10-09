from rest_framework.routers import DefaultRouter

from .views import CustomUserViewSet, UserCategoryViewSet

# app_name = 'user_app'

router = DefaultRouter()
router.register(r'users', CustomUserViewSet)
router.register(r'usercategories', UserCategoryViewSet)
urlpatterns = router.urls
