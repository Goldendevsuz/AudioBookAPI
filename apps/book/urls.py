from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'', views.BookViewSet, basename='book')
urlpatterns = router.urls
