from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'', views.AuthorViewSet, basename='author')

urlpatterns = router.urls
